# ========================================================== #
# [処理名]
# EC2インスタンス自動起動処理
# ========================================================== #

# ライブラリ定義
import boto3
import time
import configparser

# EC2インスタンス操作用
region = 'ap-northeast-1'
ec2_client = boto3.client('ec2', region_name=region)
sns_client = boto3.client('sns', region_name=region)

# ========================================================== #
# [処理名] fetch_instances_filter_tag_startble
# タグ「Startble」が「true」のインスタンス情報を取得
# 
# [引数]
# なし
# 
# [戻り値]
# 変数名「instances_filter_tag_stable」
# タグが「Startble」のインスタンス情報
# ========================================================== #
def fetch_filter_tag_startble_instances():
    # タグが「Startble」のものを選択
    instances_filter_tag_startble = ec2_client.describe_instances(
        Filters=[{ 'Name': 'tag:Startble', 'Values':  ['True', 'true'] }]
    )

    return instances_filter_tag_startble
    
# ========================================================== #
# [処理名] make_list_startble_instances_id
# タグ「Startble」が「true」のインスタンスIDのリスト作成
# 
# [引数]
# なし
# 
# [戻り値]
# 変数名「instances_id_list」
# タグ「Startble」が「true」のインスタンスIDのリスト
# ========================================================== #
def make_list_startble_instances_id():
    instances_filter_tag_startble = fetch_filter_tag_startble_instances()
    instances_id_list = [val_instances['InstanceId'] for val_reservations in instances_filter_tag_startble['Reservations'] for val_instances in val_reservations['Instances']]
    return instances_id_list

# ========================================================== #
# [処理名] make_list_startble_instances()
# タグ「Startble」が「true」のインスタンスのタグのName、パブリックIPアドレスのリスト作成
# 
# [引数]
# なし
#
# [戻り値]
# 変数名「instances_name_publicip_list」
# タグ「Startble」が「true」のインスタンスのタグのName、パブリックIPアドレスのリスト
# ========================================================== #
def make_list_startble_instances_name_publicip():

    # インスタンスのタグのName、パブリックIPアドレスを格納するために利用
    instances_name_publicip_list = []

    # パブリックIPアドレスが発番されるため再取得する
    instances_filter_tag_startble = fetch_filter_tag_startble_instances()

    for reservation in instances_filter_tag_startble['Reservations']:
        for instance in reservation['Instances']:
            
            # インスタンスのタグのName、パブリックIPアドレスを取得しリストへ格納
            tags = dict([(tag['Key'], tag['Value']) for tag in instance['Tags']])
            tags_name_and_publicip = dict(Name=tags['Name'],PublicIpAddress=instance['PublicIpAddress'])
            instances_name_publicip_list.append(tags_name_and_publicip)
    
    return instances_name_publicip_list

# ========================================================== #
# [処理名]startEC2instances()
# EC2インスタンスの起動処理

# [引数]
# 変数名「instances_id_list」
# タグ「Startble」が「true」のインスタンスIDのリスト
# 
# [戻り値]
# なし
# ========================================================== #
def startEC2instances(instances_id_list):
    ec2_client.start_instances(InstanceIds=instances_id_list)


# ========================================================== #
# [処理名]sendMail()
# メール送信処理
# タグの「Name」とパブリックIPアドレスを送信する

# [引数]
# 変数名「instances_name_publicip_list」
# タグ「Startble」が「true」のインスタンスのタグのName、パブリックIPアドレスのリスト
# 
# [戻り値]
# なし
# ========================================================== #
def sendMail(instances_name_publicip_list):
    
    config_ini = configparser.ConfigParser()
    config_ini.read('config.ini', encoding='utf-8')
    topicarn = config_ini['DEFAULT']['TopicArn']

    TOPICARN = topicarn
    SUBJECT = "Lambda(python) -> 起動したEC2インスタンスを通知します"
    message = ""
    
    for val in instances_name_publicip_list:
        instance_name = val['Name']
        public_ipaddress = val['PublicIpAddress']
        message += "{} のパブリックIPアドレスは {} です。\n".format(instance_name, public_ipaddress)
    
    params = {
    'TopicArn': TOPICARN,
    'Subject': SUBJECT,
    'Message': message
    }

    sns_client.publish(**params)

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
    instances_id_list = make_list_startble_instances_id()

    if len(instances_id_list) == 0 : print("タグ「Startble」が「true」のインスタンスIDがございません"); return

    # EC2インスタンスの起動処理
    startEC2instances(instances_id_list)

    # パブリックIPアドレスが発番されるまで一時停止
    time.sleep(30)

    # タグ「Startble」が「true」のインスタンスのタグのName、パブリックIPアドレスのリスト作成
    instances_name_publicip_list = make_list_startble_instances_name_publicip()

    # メール送信処理
    sendMail(instances_name_publicip_list)

# デバック用
# コミットする際はコメントアウトすること
# event = None
# context = None
# lambda_handler(event, context)