from pathlib import Path
import pytest
from dateutil.parser import parse
from airflow.models import DagBag, DAG, TaskInstance, Variable
from json import load

@pytest.fixture(scope='session')
def dag_path() -> Path:
    return Path(__file__).resolve().parent.parent / 'airflow_jobs' / 'dags'