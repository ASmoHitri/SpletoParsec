html1 = """<!DOCTYPE html>
<html>
<head>
<style>
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #333333;
}

li {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 16px;
  text-decoration: none;
}

li a:hover {
  background-color: #111111;
}
</style>
</head>
<body>

<p>My first paragraph.</p>
<p>My first paragraph A.</p>
<p>My first paragraph B.</p>



<ul>
  <li><a href="#home">Home</a></li>
  <li><a href="#news">News</a></li>
  <li><a href="#contact">Contact</a></li>
  <li><a href="#about">About</a></li>
</ul>

</body>
</html>"""

html2 = """<!DOCTYPE html>
<html>
<head>
<style>
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #333333;
}

li {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 16px;
  text-decoration: none;
}

li a:hover {
  background-color: #111111;
}
</style>
</head>
<body>

<p>My first paragraph F.</p>
<p>My first paragraph E.</p>
<p>My first paragraph D.</p>

<b> zmeda </b>
<IMG src="mike.png />

<ul>
  <li><a href="#home">Home</a></li>
  <li><a href="#news">News</a></li>
  <li><a href="#contact">Contact</a></li>
  <li><a href="#about">About</a></li>
  <li><a href="#contact">Contact14</a></li>
  <li><a href="#about">About22</a></li>
</ul>

</body>
</html>"""

from lxml.html.clean import Cleaner
import bs4
import re

def sanitize(dirty_html):
    cleaner = Cleaner(page_structure=True,
                  meta=True,
                  embedded=True,
                  links=True,
                  style=True,
                  processing_instructions=True,
                  inline_style=True,
                  scripts=True,
                  javascript=True,
                  comments=True,
                  frames=True,
                  forms=True,
                  annoying_tags=True,
                  remove_unknown_tags=True,
                  safe_attrs_only=True,
                  safe_attrs=frozenset(['src','color', 'href', 'title', 'class', 'name', 'id']),
                  remove_tags=('span', 'font', 'img')
                  )
    return cleaner.clean_html(dirty_html)

def clean_up(html1, html2):
    #remove the not necessary stuff
    html1 = sanitize(html1)
    html2 = sanitize(html2)
    #transform to bs
    html1_bs = bs4.BeautifulSoup(html1)
    html2_bs = bs4.BeautifulSoup(html2)
    html1 = html1_bs.prettify()
    html2 = html2_bs.prettify()
    return html1, html2

def get_next_item(html):
    """
    Input html must be stripped!
    """
    idx = 0
    if html[idx] == "<":
        while html[idx] != ">":
            idx += 1
        return html[0:idx + 1].strip(), html[idx + 1:]
    else:
        while html[idx] != "<":
            idx += 1
        return html[0:idx].strip(), html[idx:]

def html_to_list(html):
    """Input must be  a prettifyed html"""
    html_list = []
    while html:
        next_item, html = get_next_item(html)
        if next_item == "":
            continue
        else:
            html_list.append(next_item)
    return html_list

def is_tag(string):
    if string[0] == "<":
        return True
    return False

def get_tag_name(tag):
    try:
        return re.search("<*(\w*)>", tag).group(1)
    except:
        return "Input is not a tag!"



def comapre_tree(wrapper, sample):
    """Input wrapper and sample are as lists"""
    w_i = 0 #wrapper index
    s_i = 0 #sample index
    regex_list = []

    while w_i < len(wrapper) or s_i < len(sample):
        # check whether the same or mismatch
        if wrapper[w_i]== sample[s_i]:
            regex_list.append(wrapper[w_i])
            w_i += 1
            s_i += 1
            continue
        if is_tag(wrapper[w_i]):
            if is_tag(sample[s_i]):
                #tag --> tag mismatch TODO ??????
                while wrapper[w_i] != sample[s_i]:
                    regex_list.append("<")



            else:
                # string-tag mismatch --> sample string #TODO: ali je to prav, da je poj tak regex, ali samo povečamo s_i +=1
                regex_list.append("(.*?)")
                w_i += 1
        elif is_tag(sample[s_i]):
            # string-tag mismatch --> wrapper string
            regex_list.append("(.*?)")
            s_i += 1
        else:
            # string mismatch
            regex_list.append("(.*?)")
            w_i += 1
            s_i += 1
    return regex_list


def is_end_tag(tag):
    return tag[1] == "/"







html1, html2 = clean_up(html1, html2)
html1 = html_to_list(html1)
get_next_tag(html1, 1, "body")

if __name__ == "__main__":
    html1, html2 = clean_up(html1, html2)
    html1 = html_to_list(html1)







