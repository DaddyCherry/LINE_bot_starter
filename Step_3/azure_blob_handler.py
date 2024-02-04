import os
import json

from azure.data.tables import TableServiceClient
from azure.data.tables import TableEntity
from dotenv import load_dotenv

load_dotenv()

# Azure Storage アカウントの接続文字列
connect_str = os.getenv("AZURE_STORAGE_CONNECT_STR")

# テーブルサービスクライアントの作成
table_service = TableServiceClient.from_connection_string(conn_str=connect_str)


def write_entity_to_patient_table(pat_id, name):

    # 使用するテーブル名
    table_name = "Patient"

    # テーブルが存在しない場合は作成
    table_client = table_service.create_table_if_not_exists(table_name=table_name)

    # 書き込むエンティティの作成
    entity = TableEntity()
    entity['PartitionKey'] = pat_id
    entity['RowKey'] = pat_id
    entity['Name'] = name

    # エンティティをテーブルに書き込む
    table_client.upsert_entity(entity=entity)
    print("Entity successfully written to the table.")


def get_name_from_patient_table(pat_id):

    # 使用するテーブル名
    table_name = "Patient"

    # テーブルが存在しない場合は作成
    table_client = table_service.create_table_if_not_exists(table_name=table_name)

    filter_query = "PartitionKey eq '"+pat_id+"'"
    entities = table_client.query_entities(query_filter=filter_query)
    
    for entity in entities:
        return json.loads(str(entity).replace("'", '"'))['Name']
        # return str(entity).Name
        # return json.loads(str(entity))['Name']


def main():
    write_entity_to_patient_table('pat_0001', 'ヤマダタロウ')
    print(get_name_from_patient_table('pat_0001'))
    pass


if __name__ == "__main__":
   main()