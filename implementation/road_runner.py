import re
from lxml.html.clean import Cleaner
from lxml import etree
base_content_path = "../input/"


# def get_wrapper(file_name1, file_name2, encoding="utf-8"):
#     # wrapper_content = open(base_content_path + file_name1, 'r', encoding=encoding).read()
#     # sample_content = open(base_content_path + file_name2, 'r', encoding=encoding).read()
#     # wrapper_soup = BeautifulSoup(wrapper_content, 'html.parser')
#     # sample_soup = BeautifulSoup(sample_content, 'html.parser')
#     bad_html = "<html><title>Title of the document       <div> Something </div>   neki neki       \n</title><p> Nek text </p></head>"
#     cleaner = Cleaner(style=True, page_structure=False)
#     html = cleaner.clean_html(bad_html)
#     # print(html)
#
#     tree = etree.HTML(html)
#     print(etree.tostring(tree, pretty_print=True))
#     for child in tree.iter():
#             print(child.tag)

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


def is_tag(string):
    if string[0] == "<":
        return True
    return False


def get_iterator_square_candidate(tag_name, html):
    square_list = ["<{}>".format(tag_name)]
    next_item, html = get_next_item(html)
    while next_item != "</{}>".format(tag_name):
        square_list.append(next_item)
        next_item, html = get_next_item(html)
    square_list.append(next_item)
    return square_list


def get_next_different_tag(tag_name, html):
    regex = "(?<=</{0}>)\s*(</?[^{0}]>)".format(tag_name)
    match = re.search(regex, html)
    if match:
        return match.group(1)
    return None


def get_previous_tag_name(items_list):
    idx = len(items_list) - 1
    while not is_tag(items_list[idx]):
        idx -= 1
    tag = items_list[idx]
    return "".join(filter(str.isalpha, tag))


def compare_tree(wrapper_html, sample_html):
    """
    :param wrapper_html: Wrapper HTML
    :param sample_html: Sample HTML
    """
    wrapper_list = []
    sample_list = []
    regex_list = []

    wrapper_idx = 0
    sample_idx = 0

    while wrapper_html and sample_html:
        next_item_w, wrapper_html = get_next_item(wrapper_html)
        next_item_s, sample_html = get_next_item(sample_html)

        # add new items to list
        wrapper_list.append(next_item_w)
        sample_list.append(next_item_s)

        # check whether the same or mismatch
        if next_item_w == next_item_s:
            regex_list.append(next_item_w)
            return regex_list
        if is_tag(next_item_w):
            if is_tag(next_item_s):
                # tag mismatch
                prev_tag_name = get_previous_tag_name(wrapper_list)
                curr_tag_name = "".join(filter(str.isalpha, next_item_s))
                iterator_candidate_html = wrapper_html
                if curr_tag_name == prev_tag_name:
                    iterator_candidate_html = sample_html
                square_candidate = get_iterator_square_candidate(prev_tag_name, iterator_candidate_html)
                # check if iterator

                # if not iterator --> optional -- cross matching
                # TODO ne bo okkk, rabis indexe!!
                wrapper_next = get_next_different_tag(curr_tag_name, wrapper_html)
                sample_next = get_next_different_tag(curr_tag_name, sample_html)


            else:
                # string-tag mismatch --> sample string
                regex_list.append("(.*?)")
                sample_idx += 1
        elif is_tag(next_item_s):
            # string-tag mismatch --> wrapper string
            regex_list.append("(.*?)")
            wrapper_idx += 1
        else:
            # string mismatch
            regex_list.append("(.*?)")
            wrapper_idx += 1
            sample_idx += 1
    return regex_list


def get_wrapper(file_name1, file_name2, encoding="utf-8"):
    wrapper_content = open(base_content_path + file_name1, 'r', encoding=encoding).read()
    sample_content = open(base_content_path + file_name2, 'r', encoding=encoding).read()
    # wrapper_soup = BeautifulSoup(wrapper_content, 'html.parser')
    # sample_soup = BeautifulSoup(sample_content, 'html.parser')
    cleaner = Cleaner(page_structure=False)
    wrapper_content = cleaner.clean_html(wrapper_content)
    sample_content = cleaner.clean_html(sample_content)

    compare_tree(wrapper_content, sample_content, )


if __name__ == "__main__":
    # get_wrapper("neki", "neki")

    html = "<li>		dfjsdf		<i> </i>	</li>	<li>		ldkfpfadgr		</li>	<p>\
     class=\"fgjtr\">		hdhrfrh	</p></div>"
    print(get_next_different_tag("li", html))

def get_tag_name(tag):
    return re.search("<*(\w*)>", tag).group(1)

#TODO: spremeni ime
def get_sth(tag_name, html):
    n_rows = 0 #stevilo vmrensih vrstic
    while True:
        next_item, html = get_next_item(html)
        if is_tag(next_item):
            if get_tag_name(next_item) == tag_name:
                n_rows += 1
            else:
                return next_item, n_rows







