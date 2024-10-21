import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from flask import request, jsonify
from nonebot.adapters.onebot.v11 import Bot, Message
import random

# 初始化 NoneBot
nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

# 定义需要艾特的 QQ 号
qq_numbers = [
    624973652,
    360042998,
    1736817841,
    2442699315,
    734497349,
    408923363
]

def qqbot(data):
    group_id = data.get('group_id')
    sender_qq = data.get('sender_qq')

    if not group_id or not sender_qq:
        return {"status": "error", "message": "缺少必要的参数。"}

    # 获取群成员列表
    bot = nonebot.get_bot()
    group_members = bot.call_api('get_group_member_list', group_id=group_id)
    group_member_ids = {member['user_id'] for member in group_members}

    # 过滤出需要艾特的 QQ 号
    qq_numbers_in_group = [qq for qq in qq_numbers if qq in group_member_ids and str(qq) != sender_qq]

    if not qq_numbers_in_group:
        return {"status": "error", "message": "群里没有需要@的人。"}

    # 构建消息
    messages = [
        "妇愁者集结！🚀",
        "今晚有无？🌙",
        "集合！📢",
        "集？🤔"
    ]

    message = Message()
    message.append("📢 ")
    for qq in qq_numbers_in_group:
        message.append(f"[CQ:at,qq={qq}] ")
    message.append(random.choice(messages))

    # 发送消息
    bot.call_api('send_group_msg', group_id=group_id, message=message)

    return {"status": "success"}