import re
import json
import logging


def extract_from_overstock(html_content):
    data_records = []
    regex_dict = {
        "Title": "<td valign=\"top\">\s+<a\s+href=\"\S*\"><b>(.*)</b>",
        "ListPrice": "List Price:</b>\s*</td>\s*<td align=\"left\" nowrap=\"nowrap\">\s*<s>(.*)</s>",
        "Price": "<span class=\"bigred\">\s*<b>(.*)</b>",
        "Saving": "<span class=\"littleorange\">(\$[0-9\.,]*).*</span>",
        "SavingPercent": "<span class=\"littleorange\">.*?\((.*)\)</span>",
        "Content": "<span class=\"normal\">([\s\S]*?)<br>"
    }
    titles_match = list(re.finditer(regex_dict["Title"], html_content))
    list_prices_match = list(re.finditer(regex_dict["ListPrice"], html_content))
    prices_match = list(re.finditer(regex_dict["Price"], html_content))
    savings_match = list(re.finditer(regex_dict["Saving"], html_content))
    saving_percents_match = list(re.finditer(regex_dict["SavingPercent"], html_content))
    contents_match = list(re.finditer(regex_dict["Content"], html_content))
    length = len(titles_match)
    if all(len(lst) == length for lst in [list_prices_match, prices_match, savings_match, saving_percents_match, contents_match]):
        for i in range(length):
            data_records.append({
                "Title": titles_match[i].group(1),
                "ListPrice": list_prices_match[i].group(1),
                "Price": prices_match[i].group(1),
                "Saving": savings_match[i].group(1),
                "SavingPercent": saving_percents_match[i].group(1),
                "Content": contents_match[i].group(1).strip().replace("\n", " ")
            })
    else:
        logging.error("Numbers of matches found in HTML content don't match.")
        exit(1)

    output = json.dumps(data_records, ensure_ascii=False, indent=2)
    print(output)
    return output


def extract_from_rtvslo(html_content):
    regex_dict = {
        "Author": "<div class=\"author-name\">(.*)</div>",
        "PublishedTime": "<div class=\"publish-meta\">\s+(.*)<br>",
        "Title": "<title>(.*) - RTVSLO.si</title>",
        "Subtitle": "<div class=\"subtitle\">(.*)</div>",
        "Lead": "<p class=\"lead\">(.*)\s*</p>",
        "Content": "<p\s*[(class=\"Body\"]*>(.+?)</p>(?=[\S\s]*class=\"news-block \w+\")"
    }

    dataItem = {}
    for key, regex in regex_dict.items():
        if key == "Content":
            out = ''
            for strng in re.findall(regex, html_content):
                strng = re.sub("<[^>]*>", " ", strng)
                if strng != '' and strng:
                    strng = strng.strip()
                    out += ' '+strng
            dataItem[key] = out[1:]
        else:
            dataItem[key] = re.search(regex, html_content).group(1).strip()
    print(json.dumps(dataItem, indent=2, ensure_ascii=False))
    return json.dumps(dataItem, indent=2, ensure_ascii=False)


def extract_from_ideo(html_content):
    title = """<div class="naslov">\s*<div style=.*>\s*<a href=.*>(.*)</a>"""
    description= """<div class=\"opis mobilno-skrij\">*\s*<div style=.*>\s*(.*)\s*</div>"""
    price = """<div class="mobilno-skrij" style=.*>Spletna cena:</div>\s*<div class="cena" style=.*>(.*)<small>"""
    stock = "<span class=\"vprasaj_dobava\">\s*<a rel=.*>(.*)</a>"

    titles = re.findall(title, html_content)
    descriptions = re.findall(description, html_content)
    prices = re.findall(price, html_content)
    stocks = re.findall(stock, html_content)

    data = []
    for i in range(len(titles)):
        data.append({"Title": titles[i], "Price": prices[i] +
                     "€", "Description": re.sub("([[\\t]+</div>]?)","",descriptions[i].strip()), "Stock": stocks[i]})

    print(json.dumps(data, indent=2, ensure_ascii=False))
    return json.dumps(data, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    base_content_path = "../input/"
    #Primer OVERSTOCK
    overstock_html1 = open("../input/overstock.com/jewelry01.html", 'r', encoding="latin-1").read()
    extract_from_overstock(overstock_html1)
    overstock_html2 = open("../input/overstock.com/jewelry02.html", 'r', encoding="latin-1").read()
    extract_from_overstock(overstock_html2)

    #Primer RTV SLO
    rtv_audi_html = open("../input/rtvslo.si/Audi.html", 'r', encoding="utf-8").read()
    extract_from_rtvslo(rtv_audi_html)
    rtv_volvo_html = open("../input/rtvslo.si/Volvo.html", 'r', encoding="utf-8").read()
    extract_from_rtvslo(rtv_volvo_html)

    #Primer IDEO
    ideo_pometaci_html = open("../input/ideo.si/ideo1.html", 'r', encoding="windows-1250").read()
    extract_from_ideo(ideo_pometaci_html)

    ideo_podmetni_kompleti_html = open("../input/ideo.si/ideo2.html", 'r',encoding="windows-1250").read()
    extract_from_ideo(ideo_podmetni_kompleti_html)