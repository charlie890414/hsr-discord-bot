from core.utils import exact_gift_codes, redeem


def test_redeem():
    rsp = redeem("", "")

    assert rsp.status_code == 200
    assert rsp.text == '{"data":null,"message":"請先登入帳號","retcode":-1071}'


def test_exact():
    msg = "7B6B7GBZTVTB\nMSPT7HAZTCTX\n5TPBPGAGBDAK\n\n↑:Stellar_Jade: 100+100+100星瓊，截止時間 : 2023-07-09 12:00:(UTC+8)\n※此為限量兌換碼，兌完為止。\n\n在下面官網或遊戲內「左上角手機」→「...」→「兌換碼」兌換:kurukuru_seseren: https://hsr.hoyoverse.com/gift"

    result = exact_gift_codes(msg)

    expect = ["7B6B7GBZTVTB", "MSPT7HAZTCTX", "5TPBPGAGBDAK"]

    assert expect == result
