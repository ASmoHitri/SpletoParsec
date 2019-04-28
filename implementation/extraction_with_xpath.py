import re
import json
from lxml import html
import logging

base_content_path = "../input/"


def extract_from_overstock(file_name: str):
    data_records = []
    html_content = open(base_content_path + file_name, 'r').read()
    html_tree = html.fromstring(html_content)

    titles = html_tree.xpath('//td[@valign="top"]/a/b/text()')
    list_prices = html_tree.xpath('.//tbody/tr/td[2]/s/text()')
    prices = html_tree.xpath('//tbody/tr/td/span[@class="bigred"]/b/text()')
    savings_all = html_tree.xpath('//tbody/tr/td[2]/span[@class="littleorange"]/text()')
    contents = html_tree.xpath('.//span[@class="normal"]/text()')
    length = len(titles)

    if all(len(lst) == length for lst in [list_prices, prices, savings_all, contents]):
        for i in range(length):
            data_records.append({
                "Title": titles[i],
                "ListPrice": list_prices[i],
                "Price": prices[i],
                "Saving": re.search("\$[0-9.,]*", savings_all[i]).group(0),
                "SavingPercent": re.search("\((.*)\)", savings_all[i]).group(1),
                "Content": re.sub("\.\s*$", ".", contents[i])
            })
    else:
        logging.error("Numbers of matches found in HTML content don't match.")
        exit(1)

    output = json.dumps(data_records, indent=2)
    print(output)
    return output


if __name__ == "__main__":
    extract_from_overstock("overstock.com/jewelry01.html")
