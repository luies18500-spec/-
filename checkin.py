#!/usr/bin/env python3
"""红企云 AI 聚合平台自动签到脚本"""

import os
import sys
import requests

BASE_URL = "https://cloud.hongqiye.com"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def login(session: requests.Session, username: str, password: str) -> int | None:
    """登录并返回用户 ID，失败返回 None"""
    resp = session.post(
        f"{BASE_URL}/api/user/login",
        json={"username": username, "password": password},
        headers={"User-Agent": USER_AGENT},
        timeout=30,
    )
    data = resp.json()
    if not data.get("success"):
        print(f"登录失败：{data.get('message')}")
        return None
    user_id = data["data"]["id"]
    print(f"登录成功，用户 ID: {user_id}")
    return user_id


def checkin(session: requests.Session, user_id: int) -> bool:
    resp = session.post(
        f"{BASE_URL}/api/user/checkin",
        headers={
            "User-Agent": USER_AGENT,
            "New-Api-User": str(user_id),
        },
        timeout=30,
    )
    data = resp.json()
    if data.get("success"):
        quota = data.get("data", {}).get("quota_awarded", "")
        print(f"签到成功！{'获得额度 ' + str(quota) if quota else ''}")
        return True

    msg = data.get("message", "")
    if "已签到" in msg or "already" in msg.lower():
        print(f"今日已签到：{msg}")
        return True

    print(f"签到失败：{msg}")
    return False


def main():
    username = os.environ.get("HONGQIYE_USERNAME")
    password = os.environ.get("HONGQIYE_PASSWORD")

    if not username or not password:
        print("请设置 HONGQIYE_USERNAME 和 HONGQIYE_PASSWORD 环境变量")
        sys.exit(1)

    session = requests.Session()

    user_id = login(session, username, password)
    if user_id is None:
        sys.exit(1)

    if not checkin(session, user_id):
        sys.exit(1)


if __name__ == "__main__":
    main()
