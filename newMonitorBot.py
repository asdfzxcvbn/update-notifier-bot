#!/usr/bin/python3
import os
from requests import get
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from json import load, dump

TOKEN = ""     # <-- put your bot token here (string)
COUNTRY = ""   # <-- put your alpha-2 country code here (string)
MY_ID = 123    # <-- put your telegram id here (int)

STORE = f"https://itunes.apple.com/lookup?country={COUNTRY}&bundleId="
req_headers = {
    "User-Agent": "FreshRSS/1.11.2 (Linux; https://freshrss.org) like Googlebot",
    "cache-control": "private, max-age=0, no-cache"
}

def start(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != MY_ID:
        update.message.reply_text("only certain people can use this bot.")
        return
    update.message.reply_text("command: /monitor <appname> <bundleid> (where <appname> is ONE WORD with no spaces/symbols)")

def new_monitor(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != MY_ID:
        update.message.reply_text("only certain people can use this bot.")
        return
    args = context.args
    if len(args) != 2:
        update.message.reply_text("command: /monitor <appname> <bundleid> (where <appname> is ONE WORD with no spaces/symbols)")
        return

    try:
        x = get(f"{STORE}{args[1]}", headers=req_headers).json()
        current_ver = x["results"][0]["version"].strip()
    except KeyError:
        update.message.reply_text("invalid bundle id specified.")
        return

    with open(os.path.expanduser("~/.zxcvbn/monitor.json"), "r") as apps:
        monitored = load(apps)
    monitored[args[0]] = args[1]
    with open(os.path.expanduser("~/.zxcvbn/monitor.json"), "w") as apps:
        dump(monitored, apps)

    with open(os.path.expanduser("~/.zxcvbn/files.json"), "r") as version_files_dict:
        version_files = load(version_files_dict)
    version_files[args[0]] = f"{os.path.expanduser('~/.zxcvbn/')}{args[0]}.txt"
    with open(os.path.expanduser("~/.zxcvbn/files.json"), "w") as version_files_dict:
        dump(version_files, version_files_dict)

    with open(os.path.expanduser(f"~/.zxcvbn/{args[0]}.txt"), "w") as vfile:
        vfile.write(current_ver)

    update.message.reply_text(f"{args[0]} is now being monitored.")
    


if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("monitor", new_monitor))

    updater.start_polling()
    updater.idle

