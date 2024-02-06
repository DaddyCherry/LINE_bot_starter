import os
import datetime

from azure.data.tables import TableServiceClient
from azure.data.tables import TableEntity
from dotenv import load_dotenv

load_dotenv()

# Azure Storage アカウントの接続文字列
connect_str = os.getenv("AZURE_STORAGE_CONNECT_STR")

# テーブルサービスクライアントの作成
table_service = TableServiceClient.from_connection_string(conn_str=connect_str)


def write_entity_to_shift_table(emp_id, rec_type):

    # 使用するテーブル名
    table_name = "ShiftRecords"

    # テーブルが存在しない場合は作成
    table_client = table_service.create_table_if_not_exists(table_name=table_name)

    # 書き込むエンティティの作成
    entity = TableEntity()
    entity['PartitionKey'] = emp_id
    entity['RowKey'] = emp_id + '_' + rec_type
    entity['Date'] = datetime.datetime.now().strftime('%Y-%m-%d')
    entity['Time'] = datetime.datetime.now().strftime('%H:%M:%S')
    entity['RecType'] = rec_type

    # エンティティをテーブルに書き込む
    table_client.upsert_entity(entity=entity)
    print("Entity successfully written to the table.")



def main():
    write_entity_to_shift_table('emp_0001', 'IN')
    write_entity_to_shift_table('emp_0001', 'OUT')
    write_entity_to_shift_table('emp_0002', 'IN')
    write_entity_to_shift_table('emp_0002', 'OUT')
    pass


if __name__ == "__main__":
   main()