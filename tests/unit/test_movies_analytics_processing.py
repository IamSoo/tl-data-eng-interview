import pytest
import pandas as pd
from airflow_jobs.dags.scripts.MoviesAnalyticProcessing import update_release_date, calculate_ratio


@pytest.mark.parametrize("budget,revenue,expected", [
    (30, 10, 3),
    (20, 2, 10),
])
def test_calculate_ratio(budget, revenue, expected):
    actual = calculate_ratio(budget, revenue)
    assert actual == expected


def test_update_release_date():
    data = [['2020-10-02', 'Avatar2'], ['2008-10-02', '3 Idiots']]
    date_df = pd.DataFrame(data=data, columns=['release_date', 'movie'])
    df = update_release_date(date_df)
    assert df.loc[0, 'year'] == '2020'

