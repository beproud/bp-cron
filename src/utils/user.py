import logging

logger = logging.getLogger(__name__)

# Google アカウントと Slack username の対応表
GACCOUNT_SLACK_DICT = {
    "ae35@beproud.jp": "ae35",
    "altnight@beproud.jp": "altnight",
    "atsushi.mominoki@beproud.jp": "momi",
    "charles.henry.heckroth@beproud.jp": "checkroth",
    "hajime.nakagami@beproud.jp": "nakagami",
    "haru@beproud.jp": "haru",
    "haruo.sato@beproud.jp": "haru",
    "hiroki.kiyohara@beproud.jp": "hirokiky",
    "hiroomi.takeguchi@beproud.jp": "kk6",
    "hirona.yogo@beproud.jp": "hirona",
    "james.van.dyne@beproud.jp": "james",
    "kaoru.furuta@beproud.jp": "furuta",
    "kyoka@beproud.jp": "kyoka",
    "kashun.yoshida@beproud.jp": "kashew_nuts",
    "matthias.lambrecht@beproud.jp": "matsu",
    "marippe@beproud.jp": "marippe",
    "monjudoh@beproud.jp": "monjudoh",
    "mitsuhiko.kai@beproud.jp": "kai",
    "natsu@beproud.jp": "natsu",
    "naotaka.yokoyama@beproud.jp": "nao_y",
    "ri.inghui@beproud.jp": "cactusman",
    "shinsuke.sato@beproud.jp": "shin",
    "shintaro.kutsumi@beproud.jp": "923",
    "shohei.shibuya@beproud.jp": "shibuya",
    "takahiro.tsuboi@beproud.jp": "opapy",
    "takanori.suzuki@beproud.jp": "takanory",
    "takayuki.shimizukawa@beproud.jp": "shimizukawa",
    "tell-k@beproud.jp": "tell-k",
    "tsutomu.saito@beproud.jp": "tsutomu",
    "tatsuya.matoba@beproud.jp": "mtb_beta",
    "yasuyuki.kato@beproud.jp": "crohaco",
    "yasuyuki.ogawa@beproud.jp": "yyyk",
    "yoshitaka.nakamura@beproud.jp": "ray",
    "yosuke.tomita@beproud.jp": "tommy",
    "yuki.hieda@beproud.jp": "hydden",
    "koichiro.nishikawa@beproud.jp": "wan",
    "kazuko.ohmura@beproud.jp": "kameko",
    "takayuki.hirai@beproud.jp": "xiao",
    "hiroyuki.furihata@beproud.jp": "furi",
    "susumu.ishigami@beproud.jp": "susumuis",
    "yui.ohsaki@beproud.jp": "nana",
    "daiki.hirayama@beproud.jp": "hirayama",
    "satomi.konekuni@beproud.jp": "konie",
    "yuji.imamura@beproud.jp": "imaxyz",
    "hajime.kawanishi@beproud.jp": "hajimo",
}


def gaccount_to_slack(google_account, mention=True):
    """
    google account(XXXX@beproud.jp) を slack の username に変換する

    :param google_account: Googleアカウント
    :param mention: Trueの場合にusernameの前に '@' を付けて返す
    """
    logger.info(f"gaccount_to_slack: {google_account}")
    username = GACCOUNT_SLACK_DICT.get(google_account, google_account)
    username = username.replace("@beproud.jp", "")
    if mention:
        username = "@" + username
    return username
