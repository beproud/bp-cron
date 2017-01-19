import logging

logger = logging.getLogger(__name__)

# Google アカウントと Slack username の対応表
GACCOUNT_SLACK_DICT = {
    'ae35@beproud.jp': 'ae35',
    'altnight@beproud.jp': 'altnight',
    'atsushi.mominoki@beproud.jp': 'momi',
    'emi.sakata@beproud.jp': 'eskapi',
    'hajime.nakagami@beproud.jp': 'nakagami',
    'haru@beproud.jp': 'haru',
    'haruo.sato@beproud.jp': 'haru',
    'hiroki.kiyohara@beproud.jp': 'hirokiky',
    'hiroomi.takeguchi@beproud.jp': 'kk6',
    'kyoka@beproud.jp': 'kyoka',
    'marippe@beproud.jp': 'marippe',
    'masaya.shinki@beproud.jp': 'masaya',
    'mizuki.kurose@beproud.jp': 'cafistar',
    'monjudoh@beproud.jp': 'monjudoh',
    'natsu@beproud.jp': 'natsu',
    'ri.inghui@beproud.jp': 'cactusman',
    'shinsuke.sato@beproud.jp': 'shin',
    'takahiro.tsuboi@beproud.jp': 'opapy',
    'takanori.suzuki@beproud.jp': 'takanory',
    'takayuki.shimizukawa@beproud.jp': 'shimizukawa',
    'tell-k@beproud.jp': 'tell-k',
    'yasuyuki.kato@beproud.jp': 'crohaco',
    'yasuyuki.ogawa@beproud.jp': 'yyyk',
    'yoshitaka.nakamura@beproud.jp': 'ray',
    'yosuke.tomita@beproud.jp': 'tommy',
    'yuki.hieda@beproud.jp': 'hydden',
    'mitsuki.sugiya@beproud.jp': 'omega',
    'shinji.sato@beproud.jp': 'esuji',
    'naoki.okada@beproud.jp': 'okadan',
    'koichiro.nishikawa@beproud.jp': 'wan',
    'kazuko.ohmura@beproud.jp': 'kameko',
    'takayuki.hirai@beproud.jp': 'xiao',
    'hiroyuki.furihata@beproud.jp': 'furi',
    'susumu.ishigami@beproud.jp': 'susumuis',
}


def gaccount_to_slack(google_account, mention=True):
    """
    google account(XXXX@beproud.jp) を slack の username に変換する

    :param google_account: Googleアカウント
    :param mention: Trueの場合にusernameの前に '@' を付けて返す
    """
    logger.debug('gaccount_to_slack: %s', google_account)
    username = GACCOUNT_SLACK_DICT.get(google_account, google_account)
    username = username.replace('@beproud.jp', '')
    if mention:
        username = '@' + username
    return username
