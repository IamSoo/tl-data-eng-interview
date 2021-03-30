import pytest
from airflow import DAG;

@pytest.fixture(scope='session')
def test_dag_existance():
    dag = DAG(dag_id='movies_etl_dag')
    assert dag.exists
    assert dag.task_ids == {'dummy_task_to_start', 'download_movie_dump_task', 'convert_xml_to_csv', 'do_final_process', 'rds_dump'}