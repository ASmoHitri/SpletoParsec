import re
import json
from lxml import html

base_content_path = "../input/"


def extract_from_overstock(file_name: str):
    data_records = []
    html_content = open(base_content_path + file_name, 'r').read()
    html_tree = html.fromstring(html_content)
    items = html_tree.xpath('//td[@valign="top"][a]')
    for item in items:
        data_record = {}
        data_record["Title"] = str(item.xpath('./a/b/text()')[0])
        data_record["ListPrice"] = str(item.xpath('.//tbody/tr/td[2]/s/text()')[0])
        data_record["Price"] = str(item.xpath('.//tbody/tr/td/span[@class="bigred"]/b/text()')[0])

        saving_all = str(item.xpath('.//tbody/tr/td[2]/span/text()')[0])
        data_record['Saving'] = re.search("\$[0-9.,]*", saving_all).group(0)
        data_record['SavingPercent'] = re.search("\((.*)\)", saving_all).group(1)

        content_string = str(item.xpath('.//span[@class="normal"]/text()')[0])
        data_record["Content"] = re.sub("\.\s*$", ".", content_string)      # remove trailing whitespace

        data_records.append(data_record)
    output = json.dumps(data_records, indent=2)
    print(output)
    return output


if __name__ == "__main__":
    extract_from_overstock("overstock.com/jewelry01.html")
