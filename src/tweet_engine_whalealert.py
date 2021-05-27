import os
from imageai.Detection.Custom import CustomObjectDetection
import urllib
import time

from constants import ELON_TWITTER_ACCOUNT_ID, FIRSTSQUAWK_TWITTER_ACCOUNT_ID, DELTAONE_TWITTER_ACCOUNT_ID, \
    WHALEALERT_TWITTER_ACCOUNT_ID
from discord_sender import send_msg_to_discord


# Return path to a given file based on current directory
from telegram_sender import send_to_telegram

# Keywords to detect
keywords = ["#eth", "#btc", "#usdt", "#usdc", "#busd"]


def tweet_engine_whalealert_helper(status):
    status_lower = status.text.lower()
    if status.user.id_str == WHALEALERT_TWITTER_ACCOUNT_ID and any(tweet in status_lower for tweet in keywords):
        if not "from unknown wallet to unknown wallet" in status_lower:
            threshold = 19000000
            if ("minted" in status_lower):
                threshold = 9500000
            str_usd_val = status_lower[status_lower.find("(")+1:status_lower.find(")")-4]
            str_usd_val = str_usd_val.replace(",", "")
            usd_val = float(str_usd_val)
            if (usd_val >= threshold):
                msg = f"Whale Alert tweeted: \"{status.text}\" - on {time.ctime()}. Tweet: https://twitter.com/twitter/statuses/{status.id}"
                print(msg)
                send_to_telegram("@SamwiseOnChainBot", msg)
                send_msg_to_discord(msg)

def tweet_engine_whalealert(status):
    try:
        tweet_engine_whalealert_helper(status)
    except Exception as e:
        print(e)
