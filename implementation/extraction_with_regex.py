import re

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
            "Saving": "<span class=\"littleorange\">(\$[0-9\.]*).*</span>",
            "SavingPercent": "<span class=\"littleorange\">.*?\((.*)\)</span>",
            "Content": "<span class=\"normal\">([\s\S]*)<br>"
        }
        for key, regex in regex_dict.items():
            item[key] = re.search(regex, item_html).group(1)
        data_records.append(item)
    print(data_records)
    return data_records


if __name__ == "__main__":
    extract_from_overstock("overstock.com/jewelry02.html")
