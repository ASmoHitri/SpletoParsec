import re
import json

base_content_path = "../input/"


def extract_from_overstock(file_name: str):
    data_records = []
    html_content = open(base_content_path + file_name, 'r').read()
    item_regex = "<td valign=\"top\">\s+<a.*</a>[\s\S]*?<a"
    item_matches = re.finditer(item_regex, html_content)
    for match in item_matches:
        item_html = match.group(0)
        item = {}
        regex_dict = {
            "Title": "<a\s+href=\"\S*\"><b>(.*)</b>",
            "ListPrice": "nowrap=\"nowrap\">\s*<s>(.*)</s>",
            "Price": "<span class=\"bigred\">\s*<b>(.*)</b>",
            "Saving": "<span class=\"littleorange\">(\$[0-9\.,]*).*</span>",
            "SavingPercent": "<span class=\"littleorange\">.*?\((.*)\)</span>",
            "Content": "<span class=\"normal\">([\s\S]*)<br>"
        }
        for key, regex in regex_dict.items():
            item[key] = re.search(regex, item_html).group(1)
        data_records.append(item)
    output = json.dumps(data_records, indent=2)
    print(output)
    return output


def extract_from_rtvslo(file_name: str):
    html_content = open(base_content_path + file_name, 'r').read()
    regex_dict = {
        "Author": "<div class=\"author-name\">(.*)</div>",
        "PublishedTime": "<div class=\"publish-meta\">\s+(.*)<br>",
        "Title": "<title>(.*) - RTVSLO.si</title>",
        "Subtitle": "<div class=\"subtitle\">(.*)</div>",
        "Lead": "<p class=\"lead\">(.*)\s*</p>",
        "Content": "<p\s*[class=\"Body\"]*>(.+?)</p>"
    }

    dataItem = {}
    for key, regex in regex_dict.items():
        if key == "Content":
            out = ''
            for str in re.findall(regex, html_content):
                str = re.sub("<[^>]*>", " ", str)
                if str != '' and str:
                    out += ' '+str
            dataItem[key] = out[1:]
        else:
            dataItem[key] = re.search(regex, html_content).group(1)
    # dataItem
    # print(json.dumps(dataItem, indent=2, ensure_ascii=False))
    return json.dumps(dataItem, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    extract_from_overstock("overstock.com/jewelry01.html")

    print(extract_from_rtvslo(
        "rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html"))
    print(extract_from_rtvslo(
        "rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljs╠îe v razredu - RTVSLO.si.html"))
