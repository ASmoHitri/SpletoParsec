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


def extract_from_rtvslo(file_name: str):
    html_content = open(base_content_path + file_name, 'r').read()
    # html_content = open(
    #     base_content_path + "rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html").read()
    # html_content = open(
    #     base_content_path + "rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljs╠îe v razredu - RTVSLO.si.html").read()
    html_tree = html.fromstring(html_content)
    xpath_dict = {
        "Author": '//*[@id="main-container"]/div[3]/div/header/div[3]/div[1]/strong/text()',
        "PublishedTime": "//*[@id=\"main-container\"]/div[3]/div/div[1]/div[2]/text()[1]",
        "Title": "/html/head/title/text()",
        "Subtitle": "//*[@id=\"main-container\"]/div[3]/div/header/div[2]/text()",
        "Lead": "//*[@id=\"main-container\"]/div[3]/div/header/p/text()",
        "Content": "//*[@id=\"main-container\"]/div[3]/div/div[2]/article/p/text()"
    }
    # //*[@id = "main-container"]/div[3]/div/div[2]/article/p[3]
    dataItem = {}
    # test = "Content"
    # html_tree.xpath(xpath_dict[test])
    # # dataItem
    for key, xpth in xpath_dict.items():
        if key == "Title":
            dataItem[key] = re.sub(" - RTVSLO.si", "", html_tree.xpath(xpth)[0].strip())
        if key == "Content":
            out = ''
            for entry in html_tree.xpath(xpth):
                out += ' '+entry
            dataItem[key] = out[1:]
        else:
            dataItem[key] = html_tree.xpath(xpth)[0].strip()
    print(json.dumps(dataItem, indent=2, ensure_ascii=False))
    return json.dumps(dataItem, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    extract_from_overstock("overstock.com/jewelry01.html")
    extract_from_rtvslo(
        "rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html")
    extract_from_rtvslo(
        "rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljs╠îe v razredu - RTVSLO.si.html")
