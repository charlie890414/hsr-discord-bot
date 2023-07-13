import pickle
import re

import requests


def redeem(cookie: str, gift_code: str) -> requests.Response:
    url = f"https://sg-hkrpg-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey?t=1688894915625&lang=zh-tw&game_biz=hkrpg_global&uid=801259839&region=prod_official_asia&cdkey={gift_code}"

    headers = {"cookie": cookie}

    rsp = requests.get(url, headers=headers)
    return rsp


def exact_gift_codes(msg: str) -> list:
    gift_syntax = r"[A-Z0-9]{8,16}"
    pattern = re.compile(gift_syntax)

    result = pattern.findall(msg)
    return result


def set_user_cookie(uid: str, cookie: str) -> None:
    total_user = get_all_users_cookie()

    total_user[uid] = cookie

    with open("user.pickle", "wb") as f:
        pickle.dump(total_user, f)


def get_all_users_cookie() -> dict:
    try:
        with open("user.pickle", "rb") as f:
            return pickle.load(f)
    except EOFError:
        return {}


def get_user_cookie(uid: str) -> str | None:
    total_user = get_all_users_cookie()
    return total_user.get(uid, None)
