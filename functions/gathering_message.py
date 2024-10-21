import requests  # 新增：导入 requests 库
import random  # 新增：导入 random 库

def gathering_message(data):
    initiator = data.get('initiator')
    gathering_phrase = data.get('gathering_phrase')

    print(f"接收到的发起人: '{initiator}'")  # 新增：记录接收到的发起人

    # 发起人昵称与 QQ 号的映射
    initiator_mapping = {
        "奎哥": "624973652",
        "杰哥": "360042998",
        "漓江": "1736817841",
        "醉神": "2442699315",
        "e佬": "734497349",
        "瓦尼拉": "408923363"
    }

    # 验证发起人是否有效
    if initiator not in initiator_mapping:  # 更新：检查传入的昵称是否在映射的键中
        print(f"无效的发起人: {initiator}")  # 新增：记录无效发起人的日志
        return {"error": "Invalid initiator"}, 400

    if gathering_phrase is None:
        print("缺少 gathering_phrase")  # 新增：记录缺少 gathering_phrase 的情况
        return {"error": "gathering_phrase is required"}, 400

    # 根据发起人发送信息
    qq_number = initiator_mapping[initiator]  # 更新：根据昵称获取 QQ 号
    print(f"发起人 QQ 号: {qq_number}, 昵称: {initiator}")  # 新增：记录有效发起人的日志

    # 获取群组中其他成员的 QQ 号（假设有 get_group_members 函数）
    group_members = ["624973652", "360042998", "1736817841", "2442699315", "734497349", "408923363"]  # 更新：示例群组成员
    other_members = [member for member in group_members if member != qq_number]  # 排除发起人

    if not other_members:  # 新增：检查是否有其他成员
        print("没有其他成员可以艾特")  # 新增：记录没有其他成员的情况
        return {"error": "No other members to mention"}, 400

    # 生成随机表情符号
    emojis = ["📣", "💥", "🔥", "💖"]  # 更新：定义包含喇叭、爆炸、火和心形的表情符号列表
    random_emoji = random.choice(emojis)  # 新增：选择一个随机表情符号

    # 生成艾特信息
    mentions = ' '.join([f"[CQ:at,qq={member}]" for member in other_members])
    message = f"{random_emoji} {mentions} {gathering_phrase}"  # 更新：将随机表情符号添加到消息前面

    # 发送信息的请求
    response = requests.post("http://192.168.11.4:8081/send_msg", data={
        "message": message,
        "group_id": "976037945"
    })

    if response.status_code == 200:  # 新增：检查请求是否成功
        print("消息发送成功")  # 新增：记录成功发送的情况
        return {"success": "Message sent successfully"}, 200
    else:
        print(f"消息发送失败: {response.text}")  # 新增：记录发送失败的情况
        return {"error": "Failed to send message"}, response.status_code
