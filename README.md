# dota2_monitor_wechaty_bot_python
A python dota2 monitor wechat bot based on wechaty

## 介绍
这是使用Python编写的，基于[Wechaty](https://github.com/wechaty/wechaty)的微信机器人，能够监视微信群内群友们steam游戏状态以及播报dota2战报。  
使用免费的Wechaty网页版本的机器人，如果有其他需求可以参考Wechaty文档，购买有偿版本的微信机器人。  
参考QQ版dota2监视机器人编写，如有QQ版机器人需求，详见[Dota2和CSGO机器人](https://github.com/greenhaha/dota2_csgo_watcher_bot)和[基于mirai的dota2战报机器人](https://github.com/Inv0k3r/DOTA2_Bot)。  
~~本着能用就行的态度，所以会有些看起来比较奇怪的地方，比如有两个config文件。~~


## 安装
1.Clone本仓库 & [wechaty代码](https://github.com/wechaty/wechaty-getting-started)：  
```sh
    git clone https://github.com/ExpctING/dota2_monitor_wechaty_bot_python
```

2.安装代码所需依赖
```sh
    cd dota2_monitor_wechaty_bot_python/
    pip install -r requirements.txt
```
3.Clone[Wechaty](https://github.com/wechaty/wechaty-getting-started)到目录下：
```sh
    cd dota2_monitor_wechaty_bot_python/
    git clone https://github.com/wechaty/wechaty-getting-started
```
4.安装Wechaty所需的Node.js和Docker：  
>参考 https://github.com/wechaty/wechaty-getting-started

## 开始使用
1.获取并设置steam api key:  
从 https://steamcommunity.com/dev/apikey 获取自己的api key。  
将api key写入config.py文件内。

2.设置被监视人员账号信息:
在config.py文件内写入成员的昵称和数字id。

3.设置战报发送微信群：  
在config.ini文件内写入微信群名称。
>ps:目前只支持一个微信群，微信群修改名称bot会自动更新配置文件  
~~无需上线修改群名称，有时候XDM就是喜欢改群名称玩，动不动就XX击剑群的~~

4.启动Wechaty网页版客户端：
```sh
    cd dota2_monitor_wechaty_bot_python/
    chmod -x ./startwechaty.sh
    ./startwechaty.sh
```

5.启动Python机器人：  
```sh
    cd dota2_monitor_wechaty_bot_python/
    screen python bot.py
```
6.微信小号扫码登录
>为了保护账号安全，请自备一个微信小号

## 功能
>向Bot账号或者Bot所在群发送指令  

1./help: 
请求帮助文本。  

2./steamon (/steamoff):  
开启（关闭）steam游戏监视模式（默认开启）  
监视被视奸者的游戏状态 ~~杜绝小黄油吃独食~~。  

3./status:  
查询当前监视模式状态。

4.ding：  
Bot回复dong，用以检查bot是否正在运行。