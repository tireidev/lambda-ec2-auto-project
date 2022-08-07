# Lambda関数作成手順(EC2起動の場合)
1. ポリシーを作成する
```
aws iam create-policy --policy-name [ポリシー名] --policy-document file://policy.json
例) aws iam create-policy --policy-name lambda_policy_start_ec2 --policy-document file://policy.json
```

2. ロールを作成する
```
aws iam create-role --role-name [ロール名] --assume-role-policy-document file://role.json
例) aws iam create-role --role-name lambda_role_start_ec2 --assume-role-policy-document file://role.json
```

3. ロールにポリシーを適用する
```
aws iam attach-role-policy --role-name [ロール名] --policy-arn [policy-arn]
```

4. zipファイルを作成する
```
zip -r auto_ec2_start.zip lambda_function.py config.ini 
```

5. Lambda関数を作成する
```
aws lambda create-function \
--region ap-northeast-1 \
--function-name auto_ec2_start \
--zip-file fileb://auto_ec2_start.zip \
--role [role-arn] \
--handler lambda_function.lambda_handler \
--runtime python3.9 \
--memory-size 128
--timeout 900
```