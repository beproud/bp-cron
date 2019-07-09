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

* node.js
* Python3
* Docker

```bash
$ python3.7 -m venv env
$ . env/bin/activate
(env) $ pip install -r requirements.txt
(env) $ npm install
(env) $ cp src/settings.py.sample src/settings.py
(env) $ vi src/settings.py
(env) $ touch src/config/user.ini
```

## Makefile

* 主要なコマンドはMakefileにしているので適宜のぞいてください。

```bash
$ make
Please use `make <target>' where <target> is one of
  deploy             to deploy lambda app.
  remove             to remove lambda app.
  test_app           to exeute lambda application tests
  test               to exeute all tests.
  create_credentials to create credentials.pickle.
  black              to exeute auto format python codes by black.
  flake8             to exeute flake8 to python codes.
  help               to show this help messages.
```

## 必要な Google API を有効にする

以下の手順で、bp-cron の中で使用する Google API を有効にする。

1. Google API の [Projects](https://console.developers.google.com/iam-admin/projects "Projects") を開く(BeProudアカウントでアクセスする)
2. プロジェクトを作成→適当な名前(例: `bp-cron`)を指定して「作成」
3. Google API を有効にする
  - `Google Calendar API` を検索して選択→「有効にする」
  - `Google Drive API` を検索して選択→「有効にする」
4. 「認証情報」メニュー→「OAuth同意画面」タブ→以下を入力して「保存」
  - メールアドレス: 自分のメールアドレス
  - ユーザーに表示するサービス名: `bp-cron`
5. 「認証情報を作成」→「OAuth クライアント ID」→「その他」を選択→「作成」
6. OAuth クライアント IDがダイアログで表示されるので「OK」をクリックして閉じる
7. 右端のダウンロードボタンをクリックして、 `client_secret_XXXX.json` をダウンロードする
8. ファイル名を `client_secret.json` に変更する

## credentials を生成

- `make create_credentials` を実行するとブラウザが開いて API の許可を求めます。
- BeProudのGoogleアカウントでAPI許可します。
- 成功すると `credentials.pickle` という証明書ファイルが生成されます。

```bash
(env) $ make create_credentials
直近の5件のイベントを表示
: (ここにGoogleカレンダーのイベントが表示される)
(env) $ ls ./src/utils/credential.pickle
./src/utils/credential.pickle
```

### ローカル環境でのタスクの実行方法

```bash
$sls invoke local --function <Lambda function name>
```

### インフラ構成図

* https://tracery.jp/s/646a036e4b5a417799b28f59fb6d5919

### 本番環境デプロイ

```bash
make deploy
```
