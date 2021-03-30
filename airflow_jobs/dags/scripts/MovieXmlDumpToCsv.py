__author__ = 'Soonam Kalyan'

"""
A helper function that converts the xml dump to a formatted csv.
"""
import xml.etree.cElementTree as Xet
import xml.etree.ElementTree as ET
import pandas as pd
import gzip
import csv
import codecs

columns = ["title", "abstract", "url"]


# <doc>
# <title>Wikipedia: bla</title>
# <url>https://en.wikipedia.org/wiki/bla</url>
# <abstract>bla bla</abstract>
# <links></links>
# </doc>

def parse_wiki_data(file, element_tag):
    ret_dict = {}
    ret_list = []
    context = ET.iterparse(file, events=("start", "end"))
    is_first = True
    for event, elem in context:
        if is_first:
            root = elem
            is_first = False
        if event == 'end':
            if elem.tag in ['title', 'url', 'abstract']:
                if elem.tag == 'title':
                    ret_dict[elem.tag] = elem.text.replace('Wikipedia:', '').replace('(film)', '').strip()
                else:
                    ret_dict[elem.tag] = elem.text
            if elem.tag == element_tag:
                ret_list.append(ret_dict)
                ret_dict = {}
                root.clear()
    return ret_list


def convert_xml_to_csv(*, dump_wiki_xml_file: str, filter_wiki_csv_file: str, local_data_path: str):
    with gzip.open(local_data_path + dump_wiki_xml_file, 'r') as xml_file:
        data_list = parse_wiki_data(xml_file, 'doc')
        wiki_df = pd.DataFrame(data_list)
        wiki_df.drop_duplicates(subset=['title'], inplace=True)
        wiki_df.to_csv(local_data_path + filter_wiki_csv_file, header=True, index=False)
