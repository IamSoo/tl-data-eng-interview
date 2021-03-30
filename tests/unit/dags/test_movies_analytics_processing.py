import pytest
import pandas as pd;
from airflow_jobs.dags.scripts.MoviesAnalyticProcessing import *;


@pytest.mark.parametrize("budget,revenue,expected", [
    (30, 10,3),
    (20, 2,10),
])
def test_calculateRatio(budget, revenue, expected):
    actual = calculateRatio(budget, revenue)
    assert actual == expected


@pytest.fixture(scope="session")
def date_df():
    return pd.DataFrame(data = [['2020-10-02']], columns='release_date')

@pytest
def updateReleaseDate():
    df = updateReleaseDate(date_df)
    assert df[['year']] == '2020'
