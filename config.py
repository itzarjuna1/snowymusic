#
# Copyright (C) 2021-2022 by TheAloneteam@Github, < https://github.com/TheAloneTeam >.
#
# This file is part of < https://github.com/TheAloneTeam/TheAloneMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TheAloneTeam/TheAloneMusic/blob/master/LICENSE >
# All rights reserved.

import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID", "34594672"))
API_HASH = getenv("API_HASH", "a008e5018b8662e872be5a8670db4840")

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN", "")

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://knight4563:knight4563@cluster0.a5br0se.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 600))

# Set this to true if you want post ads automatically
ADS_MODE = getenv("ADS_MODE", true)

# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID", "-1003228624224"))

DEBUG_IGNORE_LOG = True
# Get this value from  on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", 7651303468))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/itzarjuna1/snowymusic",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/dark_musictm")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/snowy_hometown")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", None))


# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))


# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes


# Get your pyrogram v2 session from @StringFatherBot on Telegram
STRING1 = getenv("STRING_SESSION", "")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}


START_IMG_URL = getenv(
    "START_IMG_URL",
    "https://files.catbox.moe/r1k8hb.jpg",
)
PING_IMG_URL = getenv(
    "PING_IMG_URL",
    "https://files.catbox.moe/96taq6.png",
)
PLAYLIST_IMG_URL = "https://files.catbox.moe/96taq6.png"
STATS_IMG_URL = "https://files.catbox.moe/96taq6.png"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/96taq6.png"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/96taq6.png"
STREAM_IMG_URL = "https://files.catbox.moe/96taq6.png"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/96taq6.png"
YOUTUBE_IMG_URL = "https://files.catbox.moe/96taq6.png"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/96taq6.png"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/96taq6.png"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/96taq6.png"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
