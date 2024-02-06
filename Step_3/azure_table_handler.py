import os
import json

from datetime import datetime
from azure.data.tables import TableServiceClient
from azure.data.tables import TableEntity
from dotenv import load_dotenv

load_dotenv()

# Azure Storage アカウントの接続文字列
connect_str = os.getenv("AZURE_STORAGE_CONNECT_STR")

# テーブルサービスクライアントの作成
table_service = TableServiceClient.from_connection_string(conn_str=connect_str)


def register_patient(pat_id, name):

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


def get_patient_name(pat_id):

    # 使用するテーブル名
    table_name = "Patient"

    # テーブルが存在しない場合は作成
    table_client = table_service.create_table_if_not_exists(table_name=table_name)

    filter_query = "PartitionKey eq '"+pat_id+"'"
    entities = table_client.query_entities(query_filter=filter_query)
    
    for entity in entities:
        return json.loads(str(entity).replace("'", '"'))['Name']


def register_reservation(pat_id, reserve_datetime_str):

    # 使用するテーブル名
    table_name = "Reservation"

    # テーブルが存在しない場合は作成
    table_client = table_service.create_table_if_not_exists(table_name=table_name)

    # 書き込むエンティティの作成
    entity = TableEntity()
    entity['PartitionKey'] = pat_id
    entity['RowKey'] = pat_id
    entity['DateTime'] = reserve_datetime_str

    # エンティティをテーブルに書き込む
    table_client.upsert_entity(entity=entity)
    print("Entity successfully written to the table.")


def get_reservation(pat_id):

    # 使用するテーブル名
    table_name = "Reservation"

    # テーブルが存在しない場合は作成
    table_client = table_service.create_table_if_not_exists(table_name=table_name)

    filter_query = "PartitionKey eq '"+pat_id+"'"
    entities = table_client.query_entities(query_filter=filter_query)
    
    for entity in entities:
        return json.loads(str(entity).replace("'", '"'))['DateTime']


def is_exists_reservation(pat_id):

    # 使用するテーブル名
    table_name = "Reservation"

    # テーブルが存在しない場合は作成
    table_client = table_service.create_table_if_not_exists(table_name=table_name)

    filter_query = "PartitionKey eq '"+pat_id+"'"
    entities = table_client.query_entities(query_filter=filter_query)

    if len(list(entities)) == 0:
        return False
    
    return True


def delete_reservation(pat_id):

    # 使用するテーブル名
    table_name = "Reservation"

    # テーブルが存在しない場合は作成
    table_client = table_service.create_table_if_not_exists(table_name=table_name)
    table_client.delete_entity(partition_key=pat_id, row_key=pat_id)

    print("Entity successfully deleted from the table.")



def main():
    register_patient('pat_0001', 'ヤマダタロウ')
    print(get_patient_name('pat_0001'))

    register_reservation('pat_0001', datetime(2024, 2, 5, 15, 35).strftime("%Y/%m/%d %H:%M"))
    print(get_reservation('pat_0001'))

    print(is_exists_reservation('pat_0001'))
    delete_reservation('pat_0001')
    print(is_exists_reservation('pat_0001'))

    pass


if __name__ == "__main__":
   main()