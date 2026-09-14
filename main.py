# -*- coding: utf-8 -*-
"""
晚睡提醒 - 微信模板消息定时推送
精简版：只发送固定提醒，无天气、生日等额外字段
"""
import os
import logging

from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("goodnight")

APP_ID = os.getenv("APP_ID", "")
APP_SECRET = os.getenv("APP_SECRET", "")
TEMPLATE_ID = os.getenv("TEMPLATE_ID", "")

# 支持多个 openid，用英文逗号分隔
USER_IDS = [uid.strip() for uid in os.getenv("USER_ID", "").split(",") if uid.strip()]

# 固定提醒文案（不超过 20 字）
MESSAGE = "不早了，早点休息，晚安。"


def main():
    if not all([APP_ID, APP_SECRET, TEMPLATE_ID]):
        log.error("缺少必要配置：APP_ID / APP_SECRET / TEMPLATE_ID")
        return
    if not USER_IDS:
        log.error("缺少必要配置：USER_ID")
        return

    try:
        client = WeChatClient(APP_ID, APP_SECRET)
        wm = WeChatMessage(client)

        data = {
            "first": {"value": MESSAGE, "color": "#173177"},
        }

        for user_id in USER_IDS:
            try:
                res = wm.send_template(user_id, TEMPLATE_ID.strip(), data)
                log.info("推送给 %s 成功: %s", user_id, res)
            except Exception as e:
                log.error("推送给 %s 失败: %s", user_id, e, exc_info=True)

    except Exception as e:
        log.error("推送过程中发生错误: %s", e, exc_info=True)


if __name__ == "__main__":
    main()