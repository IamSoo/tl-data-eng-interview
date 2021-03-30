__author__ = 'Soonam Kalyan'

"""
The main class that does the analysis for the movies before inserting into the db
"""

import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None  # default='warn'
from .DbConnection import DbConnection

reqd_col_list = ['id', 'title', 'budget', 'revenue', 'production_companies', 'release_date']

# budget / revenue
def calculate_ratio(budget, revenue):
    if (revenue == 0 or budget == 0):
        return 0
    return float(budget) / float(revenue)


# Movies meta got lot of garbages
# Take only required column and do some clean up
def clean_up_and_create_movies_dataFrame(movies_metadata, l_reqd_col_list):
    mv_df = movies_metadata[l_reqd_col_list]
    columns = ['revenue', 'budget']
    for col in columns:
        mv_df[col] = mv_df[col].apply(pd.to_numeric, errors='coerce')
        mv_df.loc[:, col] = mv_df[col].fillna(0)
        mv_df[col].astype(float)
        mv_df.drop(mv_df[(mv_df[col] == 0.0) | (mv_df[col] < 10000)].index, inplace=True)

    mv_df['id'] = mv_df['id'].astype(str).astype(int)
    mv_df = mv_df.drop(mv_df.loc[mv_df['title'].isnull()].index)
    return mv_df


def update_release_date(mv_df):
    mv_df.loc[:, 'release_date'] = mv_df['release_date'].apply(lambda x: str(x).split('-')[0])
    mv_df = mv_df.rename(columns={"release_date": "year"})
    return mv_df


# Read the wiki dump that has been extracted in the previous job
def extract_wiki_filterd_dump(filter_wiki_csv_file):
    title_df = pd.read_csv(filter_wiki_csv_file)
    title_df = title_df.drop_duplicates(subset=['title'], keep='first')
    return title_df

'''
This is the final processing where we merge the filterd csv to movies metadata and finally
save the data frame to db
'''


def process(*, filter_wiki_csv_file: str, movies_metadata_file: str, local_data_path: str, rpt_table_name: str):
    movies_metadata = pd.read_csv(local_data_path + movies_metadata_file, dtype='unicode')
    mv_df = clean_up_and_create_movies_dataFrame(movies_metadata, reqd_col_list)
    mv_df = update_release_date(mv_df)
    mv_df.loc[:, 'ratio'] = mv_df.apply(lambda x: calculate_ratio(x['budget'], x['revenue']), axis=1)
    #Find the 1000 ratio rows
    merged_ratio_df = mv_df.nlargest(1000, 'ratio')

    #Extract the datafrom wiki dump
    title_df = extract_wiki_filterd_dump(local_data_path + filter_wiki_csv_file)

    #Merge based on title
    merged_df = pd.merge(merged_ratio_df, title_df, how='left', left_on='title', right_on='title')

    # Db connection object
    conn = DbConnection()
    conn.save_df_to_table(merged_df, rpt_table_name)
