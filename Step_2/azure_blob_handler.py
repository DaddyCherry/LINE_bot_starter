import os

from azure.data.tables import TableServiceClient
from azure.data.tables import TableEntity
from dotenv import load_dotenv

load_dotenv()

# Azure Storage アカウントの接続文字列
connect_str = os.getenv("AZURE_STORAGE_CONNECT_STR")

# テーブルサービスクライアントの作成
table_service = TableServiceClient.from_connection_string(conn_str=connect_str)

# 使用するテーブル名
table_name = "YourTableName"

# テーブルが存在しない場合は作成
table_client = table_service.create_table_if_not_exists(table_name=table_name)

# 書き込むエンティティの作成
entity = TableEntity()
entity['PartitionKey'] = 'sample_partition'
entity['RowKey'] = 'sample_row_01'
entity['SampleProperty'] = 'Sample Value'

# エンティティをテーブルに書き込む
table_client.upsert_entity(entity=entity)

print("Entity successfully written to the table.")
