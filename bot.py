#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import asyncio
import configparser
from typing import Optional

from wechaty import (
    Contact,
    Message,
    Wechaty,
    ScanStatus,
    Room,
)

from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
from player import PLAYER_LIST, player
from DBOper import is_player_stored, insert_info, update_DOTA2_match_ID
from common import steam_id_convert_32_to_64, update_DOTA2
import DOTA2
from steam import gaming_status_watcher, gaming_status_store


class MyBot(Wechaty):
    def __init__(self):
        super().__init__()
        self.rootDir = os.path.abspath('.')

        self.cfg = configparser.ConfigParser()
        self.cfg.read(self.rootDir + '/config.ini', encoding="utf-8")

        self.steamWatch = True

        self.helpinfo = ('1./status查询机器状态\n'
                         '2.ding-dong!\n'
                         '3./steamon or /steamoff 开启/关闭steam状态视奸机器人')

    async def on_scan(self,
                      status: ScanStatus,
                      qr_code: Optional[str] = None,
                      data: Optional[str] = None):
        contact = self.Contact.load(self.contact_id)
        print(f'user <{contact}> scan status: {status.name} , '
              f'qr_code: {qr_code}')

    async def on_login(self, contact: Contact):
        # print('Here is on_login func')
        print(f'user: {contact} has login')

    async def on_ready(self, contact: Contact):
        """do sth after login"""
        # print('Here is on_ready func')

    async def on_room_topic(self, room: Room, new_topic: str, old_topic: str,
                            changer: Contact, date: datetime):
        await room.say('Room topic changed from ' + old_topic + ' to ' +
                       new_topic + '.')
        if (old_topic == self.cfg.get('Wechat', 'roomname')):
            self.cfg.set('Wechat', 'roomname', new_topic)
            self.cfg.write(open(self.rootDir + '/config.ini', 'w'))
            await room.say('Room topic updated.')

    async def on_message(self, msg: Message):

        # listen for message event

        if msg.is_self():
            print('This msg if from myself')
            return

        text: Optional[str] = msg.text()

        if text[0] == '/':
            if text == '/help':
                await msg.say(self.helpinfo)
                return

            elif text == '/steamon':
                self.steamWatch = True
                await msg.say('Steam状态视奸机器人启动.')
                return

            elif text == '/steamoff':
                self.steamWatch = False
                await msg.say('Steam状态视奸机器人关闭.')
                return

            elif text == '/status':
                sendmsg = 'Steam状态视奸机器人：'
                if self.steamWatch:
                    sendmsg += "True"
                else:
                    sendmsg += "False"
                await msg.say(sendmsg)
                return

        elif text == '不是':
            await msg.say('不是，你为什么要说不是？')

            return

        elif text == 'ding':
            await msg.say("dong")

            return


def init():
    # 读取配置文件
    player_list = config.PLAYER_LIST
    # 读取玩家信息
    for i in player_list:
        nickname = i[0]
        short_steamID = i[1]
        print("{}信息读取完毕, ID:{}".format(nickname, short_steamID))
        long_steamID = steam_id_convert_32_to_64(short_steamID)
        gaming_status_store(short_steamID)

        try:
            last_DOTA2_match_ID = DOTA2.get_last_match_id_by_short_steamID(
                short_steamID)
        except DOTA2.DOTA2HTTPError:
            last_DOTA2_match_ID = "-1"

        # 如果数据库中没有这个人的信息, 则进行数据库插入
        if not is_player_stored(short_steamID):
            # 插入数据库
            insert_info(short_steamID, long_steamID, nickname,
                        last_DOTA2_match_ID)
            # gaming_status_store(short_steamID)
        # 如果有这个人的信息则更新其最新的比赛信息
        else:
            update_DOTA2_match_ID(short_steamID, last_DOTA2_match_ID)
        # 新建一个玩家对象, 放入玩家列表
        temp_player = player(short_steamID=short_steamID,
                             long_steamID=long_steamID,
                             nickname=nickname,
                             last_DOTA2_match_ID=last_DOTA2_match_ID)

        PLAYER_LIST.append(temp_player)


async def tick(bot: MyBot):
    # print("Here is tick func")
    sendmsg = []
    if bot.steamWatch:
        msg = gaming_status_watcher()
        if isinstance(msg, str):
            sendmsg.append(msg)

    # 格式: { match_id1: [player1, player2, player3], match_id2: [player1, player2]}
    result = update_DOTA2()
    for match_id in result:
        msg = DOTA2.generate_match_message(match_id=match_id,
                                           player_list=result[match_id])
        if isinstance(msg, str):
            sendmsg.append(msg)

    if not sendmsg:
        return

    room: Optional[Room] = await bot.Room.find(
        bot.cfg.get('Wechat', 'roomname'))
    if (room is None):
        print("Conversation isn't found!!!!!!!!!!!!!!")
        return
    await room.ready()

    for msg in sendmsg:
        await room.say(msg)


async def main():
    # Setting environment
    os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT'] = '127.0.0.1:8080'
    os.environ[
        'WECHATY_PUPPET_SERVICE_TOKEN'] = '6f237852-128a-467c-ba4b-02b3a830b674'

    global bot
    bot = MyBot()

    if init() != -1:
        print("初始化完成, 开始更新比赛信息")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(tick, 'interval', seconds=60, args=[bot])

    scheduler.start()
    await bot.start()


if __name__ == '__main__':
    asyncio.run(main())
