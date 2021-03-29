__author__ = 'Soonam Kalyan'

"""
A helper function that converts the xml dump to a formatted csv.
"""
import xml.etree.cElementTree as Xet
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

def convert_xml_to_csv(*, dump_wiki_xml_file: str, filter_wiki_csv_file: str, local_data_path: str):
    entry = False
    entry_dict = {}
    with codecs.open(local_data_path + filter_wiki_csv_file, "w", "utf-8") as filtered_csv:
        csv_writer = csv.writer(filtered_csv, quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(columns)
        data = gzip.open(local_data_path + dump_wiki_xml_file, 'rb')
        for event, elem in Xet.iterparse(data, events=['start', 'end']):
            if event == "start" and elem.tag == "doc":
                entry = True
                entry_dict = {}
            # Find all columns under
            if entry:
                if elem.tag in columns:
                    if elem.tag == "title" and elem.text:
                        title = elem.text.split("Wikipedia:")[-1].split("(")[0]
                        elem.text = title.strip()
                    entry_dict[elem.tag] = elem.text

            if entry and event == "end" and elem.tag == "doc":
                csv_writer.writerow([entry_dict['title'], entry_dict['abstract'], entry_dict['url']])
        elem.clear()
