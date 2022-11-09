# - *- coding: utf- 8 - *-
import configparser

config = configparser.ConfigParser()
config.read("settings.ini", encoding='UTF-8')

BOT_TOKEN = config["bot_settings"]["token"]
admins = config["bot_settings"]["admin_id"]


if "," in admins:
    adminList = admins.split(",")
    n = []

    for each in adminList:
        n.append(int(each))
    adminList = n
else:
    if len(admins) >= 1:
        adminList = [int(admins)]
    else:
        adminList = []
        print("[!] Вы не указали админ ID")
        exit(0)

knownUsers = {}
userStep = {}
username_list = {}
dtd = {}
antispam = {}
