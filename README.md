# SpletoParsec
Projekt SpletoParsec vsebuje orodja za ekstrakcijo podatkov iz spletnih strani.  
En del predstavlja ekstrakcija s statičnimi regexi in xPathi, ki omogoča ekstrakcijo iz določenih strani iz domen:  
+ overstock.com
+ rtvslo.si
+ ideo.si

Primeri strani, ki jih je mogoče ekstrahirati se nahajajo v mapi **input**, primeri outputov oziroma rezultatov ekstrakcije teh strani pa v mapi **outputs**.  
  
Drugi del pa je RoadRunner-like implementacija, ki za podana dva HTMLja zgradi regex s katerim potem lahko ekstrahiramo podatke teh strani.   
  
Uporaba funkcij za ekstrakcijo:
  
## Ekstrakcija podatkov z regexom  
~~~~
from implementation import extraction_with_regex as regex_extr

# ekstrakcija podatkov iz domene overstock.com
overstock_html = open(<file_name>, 'r', encoding=<file_encoding>).read()
regex_extr.extract_from_overstock(overstock_html)

# ekstrakcija podatkov iz domene rtvslo.si
rtv_html = open(<file_name>, 'r', encoding="utf-8").read()
regex_extr.extract_from_rtvslo(rtv_html)

# ekstrakcija podatkov iz domene ideo.si
ideo_html = open(<file_name>, 'r', encoding=<file_encoding>).read()
regex_extr.extract_from_ideo(ideo_html)
~~~~  
  
## Ekstrakcija podatkov z xPathom 
~~~~
from implementation import extraction_with_xpath as xpath_extr

# ekstrakcija podatkov iz domene overstock.com
overstock_html = open(<file_name>, 'r', encoding=<file_encoding>).read()
xpath_extr.extract_from_overstock(overstock_html)

# ekstrakcija podatkov iz domene rtvslo.si
rtv_html = open(<file_name>, 'r', encoding="utf-8").read()
xpath_extr.extract_from_rtvslo(rtv_html)

# ekstrakcija podatkov iz domene ideo.si
ideo_html = open(<file_name>, 'r', encoding=<file_encoding>).read()
xpath_extr.extract_from_ideo(ideo_html)
~~~~

## Road Runner
Requirements:
+ lxml, bs4 (navedeni v requirements.txt)
+ namestitev: `pip3 install -r requirements.txt`  
   
~~~~
from implementation import road_runner

html1 = open(<file_name>, 'r', encoding=<file_encoding>).read()
html2 = open(<file_name>, 'r', encoding=<file_encoding>).read()
output_regex = road_runner.get_wrapper(html1, html2)
~~~~  