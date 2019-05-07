import re
import json
from lxml import html
import logging


def extract_from_overstock(html_content):
    data_records = []
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
                "Content": re.sub("\.\s*$", ".", contents[i]).strip().replace("\n", " ")
            })
    else:
        logging.error("Numbers of matches found in HTML content don't match.")
        exit(1)

    output = json.dumps(data_records, indent=2)
    print(output)
    return output


def extract_from_rtvslo(html_content):
    html_tree = html.fromstring(html_content)
    xpath_dict = {
        "Author": '//*[@id="main-container"]/div[3]/div/header/div[3]/div[1]/strong/text()',
        "PublishedTime": "//*[@id=\"main-container\"]/div[3]/div/div[1]/div[2]/text()[1]",
        "Title": "/html/head/title/text()",
        "Subtitle": "//*[@id=\"main-container\"]/div[3]/div/header/div[2]/text()",
        "Lead": "//*[@id=\"main-container\"]/div[3]/div/header/p/text()",
        "Content": "//*[@id=\"main-container\"]/div[3]/div/div[2]/article/p/text()|//*[@id=\"main-container\"]/div[3]/div/div[2]/article/p/strong/text()"
    }
    dataItem = {}
    for key, xpth in xpath_dict.items():
        if key == "Title":
            dataItem[key] = re.sub(" - RTVSLO.si", "", html_tree.xpath(xpth)[0].strip())
        elif key == "Content":
            out = ''
            for entry in html_tree.xpath(xpth):
                out += ' '+entry
            dataItem[key] = out[1:]
        else:
            dataItem[key] = html_tree.xpath(xpth)[0].strip()
    print(json.dumps(dataItem, indent=2, ensure_ascii=False))
    return json.dumps(dataItem, indent=2, ensure_ascii=False)


def extract_from_ideo(html_content):
    html_tree = html.fromstring(html_content)

    title = """//*[@id="izdelki_okvir"]/div/div/div/div/a/text()"""
    description = "//div[@class=\"opis mobilno-skrij\"]/div/text()[last()]"
    price = """//*[@id="izdelki_okvir"]/div/div/div/div/div[2]/text()"""
    stock = """//*[@id="izdelki_okvir"]/div/div/div/div/span[2]/a/text()"""

    titles = html_tree.xpath(title)
    descriptions = html_tree.xpath(description)
    prices = html_tree.xpath(price)
    stocks = html_tree.xpath(stock)

    data = []
    for i in range(len(titles)):
        data.append({"Title": titles[i].strip(), "Price": prices[i].strip() + "€", "Description": descriptions[i].strip(), "Stock": stocks[i].strip()})

    print(json.dumps(data, indent=2, ensure_ascii=False))
    return json.dumps(data, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    base_content_path = "../input/"
    # Primer OVERSTOCK
    overstock_html1 = open("../input/overstock.com/jewelry01.html", 'r', encoding="latin-1").read()
    extract_from_overstock(overstock_html1)
    overstock_html2 = open("../input/overstock.com/jewelry02.html", 'r', encoding="latin-1").read()
    extract_from_overstock(overstock_html2)

    # Primer RTV SLO
    rtv_audi_html = open("../input/rtvslo.si/Audi.html", 'r', encoding="utf-8").read()
    extract_from_rtvslo(rtv_audi_html)
    rtv_volvo_html = open("../input/rtvslo.si/Volvo.html", 'r', encoding="utf-8").read()
    extract_from_rtvslo(rtv_volvo_html)

    # Primer IDEO.SI
    ideo_pometaci_html = open("../input/ideo.si/stroji za pometanje _ ideo.si.html", 'r',encoding="windows-1250").read()
    extract_from_ideo(ideo_pometaci_html)

    ideo_podmetni_kompleti_html = open("../input/ideo.si/Termostatski podometni kompleti _ ideo.si.html", 'r',encoding="windows-1250").read()
    extract_from_ideo(ideo_podmetni_kompleti_html)
