#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
from player import player, PLAYER_LIST

conn = sqlite3.connect('playerInfo.db')
c = conn.cursor()


def init():
    cursor = c.execute("SELECT * from playerInfo")
    for row in cursor:
        player_obj = player(short_steamID=row[0],
                            long_steamID=row[1],
                            nickname=row[2],
                            last_DOTA2_match_ID=row[4])
        player_obj.DOTA2_score = row[4]
        PLAYER_LIST.append(player_obj)


def update_DOTA2_match_ID(short_steamID, last_DOTA2_match_ID):
    c.execute("UPDATE playerInfo SET last_DOTA2_match_ID='{}' "
              "WHERE short_steamID={}".format(last_DOTA2_match_ID,
                                              short_steamID))
    conn.commit()


def update_Player_NickName(short_steamID, nickname):
    c.execute("UPDATE playerInfo SET nickname='{}' "
              "WHERE short_steamID={}".format(nickname,
                                              short_steamID))
    conn.commit()


def insert_info(short_steamID, long_steamID, nickname, last_DOTA2_match_ID):
    c.execute(
        "INSERT INTO playerInfo (short_steamID, long_steamID, nickname, last_DOTA2_match_ID) "
        "VALUES ({}, {}, '{}', '{}')".format(short_steamID, long_steamID,
                                             nickname, last_DOTA2_match_ID))
    conn.commit()


def is_player_stored(short_steamID: int) -> bool:
    c.execute("SELECT * FROM playerInfo WHERE short_steamID=={}".format(
        short_steamID))
    if len(c.fetchall()) == 0:
        return False
    return True


def get_playing_game(short_steamID):
    ret = c.execute(
        "SELECT gamename, last_update FROM playerInfo WHERE long_steamID={}".
        format(short_steamID)).fetchone()
    # print(
    #     "SELECT gamename, last_update FROM playerInfo WHERE long_steamID={}".
    #     format(short_steamID))
    return (ret[0], ret[1]) if ret else ('', 0)


def update_playing_game(short_steamID, gamename, timestamp):
    # print(
    #     "UPDATE playerInfo SET gamename=\"{}\", last_update={} WHERE long_steamID={}"
    #     .format(gamename, timestamp, short_steamID))
    c.execute(
        "UPDATE playerInfo SET gamename=\"{}\", last_update={} WHERE long_steamID={}"
        .format(gamename, timestamp, short_steamID))
    conn.commit()
