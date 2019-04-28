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
        # remove trailing whitespace
        data_record["Content"] = re.sub("\.\s*$", ".", content_string)

        data_records.append(data_record)
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
