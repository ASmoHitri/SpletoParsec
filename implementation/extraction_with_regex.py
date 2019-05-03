import re
import json
import logging

base_content_path = "../input/"


def extract_from_overstock(file_name: str):
    data_records = []
    html_content = open(base_content_path + file_name, 'r', encoding="Latin_1").read()
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
                "Content": contents_match[i].group(1)
            })
    else:
        logging.error("Numbers of matches found in HTML content don't match.")
        exit(1)

    output = json.dumps(data_records, ensure_ascii=False, indent=2)
    print(output)
    return output


def extract_from_rtvslo(file_name: str):
    html_content = open(base_content_path + file_name, 'r', encoding="utf-8").read()
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
            dataItem[key] = re.search(regex, html_content).group(1)
    print(json.dumps(dataItem, indent=2, ensure_ascii=False))
    return json.dumps(dataItem, indent=2, ensure_ascii=False)

def extract_from_ideo(file_name: str):
    html_content = open(base_content_path + file_name, 'r').read()

    title = """<div class="naslov">\s*<div style=.*>\s*<a href=.*>(.*)</a>"""
    lead = """<div class=\"opis mobilno-skrij\">\s*<div style=.*>\s*(.*)\s*</div>"""
    price = """<div class="mobilno-skrij" style=.*>Spletna cena:</div>\s*<div class="cena" style=.*>(.*)<small>"""
    stock = "<span class=\"vprasaj_dobava\">\s*<a rel=.*>(.*)</a>"

    titles = re.findall(title,html_content)
    leads = re.findall(lead,html_content)
    prices = re.findall(price,html_content)
    stocks = re.findall(stock,html_content)

    data =[]
    for i in range(len(titles)):
        data.append({"Title":titles[i], "Price":prices[i]+"€", "Lead":leads[i], "Stock": stocks[i]})

    print(json.dumps(data, indent=2, ensure_ascii=False))
    return json.dumps(data, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    extract_from_overstock("overstock.com/jewelry01.html")

    extract_from_rtvslo(
        "rtvslo.si/Audi.html")

    extract_from_rtvslo(
        "rtvslo.si/Volvo.html")

    extract_from_ideo("ideo.si/stroji za pometanje _ ideo.si.html")

    extract_from_ideo("ideo.si/posteljni podi in vzmetnice _ ideo.si.html")


