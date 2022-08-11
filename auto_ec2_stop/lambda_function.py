# ========================================================== #
# [処理名]
# EC2インスタンス自動停止処理
# ========================================================== #

# ライブラリ定義
import boto3

# EC2インスタンス操作用
region = 'ap-northeast-1'
ec2_client = boto3.client('ec2', region_name=region)

# ========================================================== #
# [処理名] fetch_instances_filter_tag_stoppable
# タグ「Stoppable」が「true」のインスタンス情報を取得
# 
# [引数]
# なし
# 
# [戻り値]
# 変数名「instances_filter_tag_stoppable」
# タグが「Stoppable」のインスタンス情報
# ========================================================== #
def fetch_filter_tag_stoppable_instances():
    # タグが「Stoppable」のものを選択
    instances_filter_tag_stoppable = ec2_client.describe_instances(
        Filters=[{ 'Name': 'tag:Stoppable', 'Values':  ['True', 'true'] }]
    )

    return instances_filter_tag_stoppable
    
# ========================================================== #
# [処理名] make_list_stoppable_instances_id
# タグ「Stoppable」が「true」のインスタンスIDのリスト作成
# 
# [引数]
# なし
# 
# [戻り値]
# 変数名「instances_id_list」
# タグ「Stoppable」が「true」のインスタンスIDのリスト
# ========================================================== #
def make_list_stoppable_instances_id():
    instances_filter_tag_stoppable = fetch_filter_tag_stoppable_instances()
    instances_id_list = [val_instances['InstanceId'] for val_reservations in instances_filter_tag_stoppable['Reservations'] for val_instances in val_reservations['Instances']]
    return instances_id_list

# ========================================================== #
# [処理名]stopEC2instances()
# EC2インスタンスの起動処理

# [引数]
# 変数名「instances_id_list」
# タグ「Stoppable」が「true」のインスタンスIDのリスト
# 
# [戻り値]
# なし
# ========================================================== #
def stopEC2instances(instances_id_list):
    ec2_client.stop_instances(InstanceIds=instances_id_list)

# ========================================================== #
# [処理名]lambda_handler
# Lambdaメイン処理

# [引数]
# なし
# 
# [戻り値]
# なし
# ========================================================== #
def lambda_handler(event, context):

    # タグ「Startble」が「true」のインスタンスIDのリスト作成
    instances_id_list = make_list_stoppable_instances_id()

    # EC2インスタンスの停止処理
    stopEC2instances(instances_id_list)


# デバック用
# Lambdaで実行する際はコメントアウトすること
# event = None
# context = None
# lambda_handler(event, context)