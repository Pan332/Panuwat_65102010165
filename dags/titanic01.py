from datetime import timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
import csv
import pandas as pd
from datetime import datetime
from airflow.hooks.mysql_hook import MySqlHook

def upload_data():
    df = pd.read_csv('/my_tmp/tested.csv')
    mysql_hook = MySqlHook(mysql_conn_id='mydb', schema='homestead')
    engine = mysql_hook.get_sqlalchemy_engine()
    df.to_sql(con=engine, name='titanic', if_exists='replace')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
}

with DAG(
    'titanic',
    default_args=default_args,
    schedule_interval="* * * * *",
    start_date=days_ago(2),
    catchup=False,
    tags=['airflow_tab']
) as dag:
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    insert_data_task = PythonOperator(
        task_id='read_db',
        python_callable=upload_data
    )

    start >> insert_data_task >> end