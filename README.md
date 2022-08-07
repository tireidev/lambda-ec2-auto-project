# lambda-ec2-auto-project
AWS LambdaよりEC2を自動起動、自動停止させるプログラムを開発する。

# ローカル環境での実行
## 前提
- ローカル環境(Windows10)で開発することを想定する。
- 「lambda_developers.json」ポリシーを作成し、ローカル環境で利用するIAMユーザに付与すること
- ローカル環境にpython3.10.6がインストールされている
- ローカル環境にBoto3ライブラリがインストールする

## コマンド使用方法
自動起動の場合は「auto_ec2_start」配下に遷移し、
自動停止の場合は「auto_ec2_stop」配下に遷移し、
以下のコマンドを実行する。
```
python lambda_function.py 
```

# Lambda関数の作成手順
自動起動の場合は「auto_ec2_start」配下に遷移し、
自動停止の場合は「auto_ec2_stop」配下に遷移し、
README.mdを参照する。

# ライセンス
MIT.
