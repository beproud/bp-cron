# bp-cron

* BeProudで定期実行するタスクをまとめたい

## モチベーション

* Google Apps Script でいろいろ定期実行するものが増えてきた
* Apps Script 書くのが単純にだるい
* 権限でひっかかったりする
* 手元のエディタで書きたい
* dateutilとか便利なライブラリを使いたい

## 元ネタ

* https://project.beproud.jp/redmine/issues/51850

## 環境構築

```bash
$ pyvenv-3.5 env
$ . env/bin/activate
(env) $ pip install -r requirements.txt
(env) $ cp settings.py.sample settings.py
(env) $ vi settings.py
(env) $ python run.py
```