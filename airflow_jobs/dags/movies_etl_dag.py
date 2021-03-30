__author__ = 'Soonam Kalyan'

"""
The main DAG that does the analysis for high profit movies  before inserting into the db
    Steps Involved:
    1) Downloads the dump
    2) Calculate the high profit
    3) Insert the top 1000 movies (with highest ratio) postgre
"""

from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator

from scripts.MovieXmlDumpToCsv import *
from scripts.MoviesAnalyticProcessing import *
from airflow.utils.dates import days_ago

# Global Variables
DATA_DIR = '/usr/local/app/data/'
RPT_TABLE_NAME = 'movie_report'
FILTERED_WIKI_FILE_NAME = 'filtered-wiki.csv'
WIKI_DUMP_FILE_NAME = 'enwiki-latest-abstract.xml.gz'

default_args = {
    'owner': 'Soonam',
    'email': ['kalyan_soonam@yahoo.co.in'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'start_date': days_ago(1),
    'retry_delay': timedelta(minutes=5),
    'provide_context': False,
    'depends_on_past': False,
}

with DAG(
        dag_id="movies_etl_dag",
        schedule_interval='@hourly',
        default_args=default_args,
        catchup=False) as dag:

    dummy_task_to_start = DummyOperator(
        task_id='dummy_task_to_start')

    # 1. Ensure we start everything fresh
    clean_up_task = BashOperator(
        task_id='clean_up_task',
        bash_command="cd /usr/local/app/data/ && rm -rf *")

    # 2. Download the movie dump from wiki
    download_movie_dump_task = BashOperator(
        task_id='download_movie_dump_task',
        bash_command="wget -nv https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz \-O /usr/local/app/data/enwiki-latest-abstract.xml.gz")

    # 3. Convert movie dump to csv
    convert_xml_to_csv = PythonOperator(
        python_callable=convert_xml_to_csv,
        task_id='convert_xml_to_csv',
        op_kwargs={
            'dump_wiki_xml_file': WIKI_DUMP_FILE_NAME,
            'filter_wiki_csv_file': FILTERED_WIKI_FILE_NAME,
            'local_data_path': DATA_DIR
        })

    # 4. Process and insert the processed data to db
    do_final_process = PythonOperator(
        python_callable=process,
        task_id='do_final_process',
        op_kwargs={
            'filter_wiki_csv_file': FILTERED_WIKI_FILE_NAME,
            'movies_metadata_file': 'movies_metadata.csv',
            'local_data_path': DATA_DIR,
            'rpt_table_name': RPT_TABLE_NAME
        }
    )

dummy_task_to_start >> clean_up_task >> download_movie_dump_task >> convert_xml_to_csv >> do_final_process
