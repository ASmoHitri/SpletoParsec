import re
import bs4
from lxml.html.clean import Cleaner
base_content_path = "../input/"


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


def is_tag(input_str: str, which_tag='any'):
    """
    which tag can be start, end or any.
    Returns None if input str is not a tag
    """
    test_tag = re.search("<(.*?)>", input_str)
    if which_tag == 'any':
        if test_tag:
            return True
        else:
            return None
    elif which_tag == 'start':
        if not test_tag:
            return None
        return not is_tag(input_str, 'both') and not is_tag(input_str, 'end')
    elif which_tag == 'both':
        if not test_tag:
            return None
        test = re.search("<([^/].*?/)>", input_str)
        if test:
            return True
        else:
            return False
    else:  # which_tag == 'end'
        if not test_tag:
            return None
        test = re.search("<(/.*?[^/])>", input_str)
        if test:
            return True
        else:
            return False


def get_iterator_square_candidate(tag_name, items_list, curr_idx):
    num_of_opening_tags = 1
    square_list = [items_list[curr_idx]]
    while num_of_opening_tags > 0 and curr_idx < len(items_list) - 1:
        curr_idx = curr_idx + 1
        next_item = items_list[curr_idx]
        tag = is_tag(next_item, which_tag="start")
        if tag is not None:
            if get_tag_name(next_item) == tag_name:
                if tag:
                    num_of_opening_tags += 1
                else:
                    num_of_opening_tags -= 1
        square_list.append(next_item)
    return square_list, curr_idx


def get_previous_tag_name(items_list, curr_idx):
    curr_idx = curr_idx - 1
    while not is_tag(items_list[curr_idx]):
        curr_idx -= 1
    tag = items_list[curr_idx]
    return "".join(filter(str.isalpha, tag))


def get_upper_square(items_list, curr_idx):
    num_of_closing_tags = 1
    idx = curr_idx - 1
    tag_name = get_tag_name(items_list[curr_idx])
    while num_of_closing_tags > 0:
        idx -= 1
        if items_list[idx] == "<{}>".format(tag_name):
            num_of_closing_tags -= 1
        elif items_list[idx] == "</{}>".format(tag_name):
            num_of_closing_tags += 1
    return items_list[idx:curr_idx]


def get_tag_name(input_str: str, get_all=False):
    """
    returns tuple:
    (tag_name, id_if_exists, class_if_exists) or (tag_name)
    """
    tag_name = re.search("</?(\w*)?[\s\S]*>", input_str)
    if tag_name:
        tag_name = tag_name.group(1)
    if get_all:
        class_name = re.search("<[\s\S]*class=\"(.*?)\"[\s\S]*>", input_str)
        if class_name:
            class_name = class_name.group(1)
        id = re.search("<[\s\S]*id=\"(.*?)\"[\s\S]*>", input_str)
        if id:
            id = id.group(1)
        return tag_name, class_name, id
    return tag_name


def is_iterator(wrapper_list, sample_list):
    regex_list = []
    wrapper_idx = 0
    sample_idx = 0

    while wrapper_idx < len(wrapper_list) and sample_idx < len(sample_list):
        next_item_w = wrapper_list[wrapper_idx]
        next_item_s = sample_list[sample_idx]
        if next_item_w == next_item_s:
            regex_list.append(next_item_w)
            wrapper_idx += 1
            sample_idx += 1
            continue
        if is_tag(next_item_w):
            if is_tag(next_item_s):
                return False, None
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
    return True, regex_list


def update_iterator_regex(regex, iterator_regex):
    idx = len(regex) - 1
    iterator_tag_name = get_tag_name(iterator_regex[0])
    curr_tag_name = get_tag_name(regex[idx])
    if curr_tag_name != iterator_tag_name:
        num_of_closing_tags = 1
        while num_of_closing_tags > 0:
            idx -= 1
            if get_tag_name(regex[idx]) == curr_tag_name:
                tag_state = is_tag(regex[idx], which_tag="start")
                if tag_state:
                    num_of_closing_tags -= 1
                elif tag_state is False:
                    num_of_closing_tags += 1
        idx -= 1
        if get_tag_name(regex[idx]) != iterator_tag_name:
            print("Bad input regex!")
            return None
    end_idx = idx
    if regex[end_idx][-1] == "*":
        return regex
    num_of_closing_tags = 1
    while num_of_closing_tags > 0:
        idx -= 1
        if get_tag_name(regex[idx]) == iterator_tag_name:
            tag_state = is_tag(regex[idx], which_tag="start")
            if tag_state:
                num_of_closing_tags -= 1
            elif tag_state is False:
                num_of_closing_tags += 1
    start_idx = idx
    before_regex = regex[0:start_idx]
    if end_idx == len(regex) - 1:
        after_regex = []
    else:
        after_regex = regex[end_idx + 1:]
    iterator_regex[0] = "(" + iterator_regex[0]
    iterator_regex[-1] = iterator_regex[-1] + ")*"
    return before_regex + iterator_regex + after_regex


def get_next_tag(html_list, index):
    is_end = is_tag(html_list[index], which_tag='end')
    # is end tag, pogledamo prvega, ki se razlikuje
    if is_end:
        while True:
            index += 1
            if index >= len(html_list):
                return None
            if is_tag(html_list[index]):
                return (index, get_tag_name(html_list[index]))
    # is both
    elif is_tag(html_list[index], which_tag='both'):
        while True:
            index += 1
            if index >= len(html_list):
                return None
            if is_tag(html_list[index]):
                return (index, get_tag_name(html_list[index]))
    # is a start tag
    else:
        start_tags = 1
        end_tags = 0
        while True:
            index += 1
            if index >= len(html_list):
                return None
            if is_tag(html_list[index]):
                if start_tags == end_tags:
                    return (index, get_tag_name(html_list[index]))
                elif is_tag(html_list[index], which_tag='end'):
                    end_tags += 1
                else:
                    start_tags += 1

# def compare_tree(wrapper_html, sample_html):
#     """
#     :param wrapper_html: Wrapper HTML
#     :param sample_html: Sample HTML
#     """
#     wrapper_list = []
#     sample_list = []
#     regex_list = []
#
#     wrapper_idx = 0
#     sample_idx = 0
#
#     while wrapper_html and sample_html:
#         next_item_w, wrapper_html = get_next_item(wrapper_html)
#         next_item_s, sample_html = get_next_item(sample_html)
#
#         # add new items to list
#         wrapper_list.append(next_item_w)
#         sample_list.append(next_item_s)
#
#         # check whether the same or mismatch
#         if next_item_w == next_item_s:
#             regex_list.append(next_item_w)
#             return regex_list
#         if is_tag(next_item_w):
#             if is_tag(next_item_s):
#                 # tag mismatch
#                 prev_tag_name = get_previous_tag_name(wrapper_list)
#                 curr_sample_tag_name = get_tag_name(next_item_s)
#                 curr_wrapper_tag_name = get_tag_name(next_item_w)
#
#                 iterator_candidate_html = None
#                 iterator_candidate_list = None
#                 if curr_wrapper_tag_name == prev_tag_name:
#                     iterator_candidate_html = wrapper_html
#                     iterator_candidate_list = wrapper_list
#                 elif curr_sample_tag_name == prev_tag_name:
#                     iterator_candidate_html = sample_html
#                     iterator_candidate_list = sample_list
#
#                 if iterator_candidate_html:
#                     square_candidate = get_iterator_square_candidate(prev_tag_name, iterator_candidate_html)
#                     upper_square = get_upper_square(iterator_candidate_list)
#                     # check if iterator
#
#                 # not iterator --> optional -- cross matching
#                 # TODO ne bo okkk, rabis indexe!!
#                 wrapper_next = get_next_different_tag(curr_wrapper_tag_name, wrapper_html)
#                 sample_next = get_next_different_tag(curr_sample_tag_name, sample_html)
#
#             else:
#                 # string-tag mismatch --> sample string
#                 regex_list.append("(.*?)")
#                 sample_idx += 1
#         elif is_tag(next_item_s):
#             # string-tag mismatch --> wrapper string
#             regex_list.append("(.*?)")
#             wrapper_idx += 1
#         else:
#             # string mismatch
#             regex_list.append("(.*?)")
#             wrapper_idx += 1
#             sample_idx += 1
#     return regex_list


def compare_tree(wrapper_list, sample_list):
    """
    :param wrapper_list: Wrapper HTML list
    :param sample_list: Sample HTML list
    """

    regex_list = []
    idxs = [0, 0]   # 0 - wrapper index, 1 - sample index
    wrapper_len = len(wrapper_list)
    sample_len = len(sample_list)

    while idxs[0] < wrapper_len and idxs[1] < sample_len:
        next_item_w = wrapper_list[idxs[0]]
        next_item_s = sample_list[idxs[1]]

        # check whether the same or mismatch
        if next_item_w == next_item_s:
            regex_list.append(next_item_w)
            idxs[0] += 1
            idxs[1] += 1
            continue
        if is_tag(next_item_w):
            if is_tag(next_item_s):
                # tag mismatch
                prev_tag_name_wrapper = get_previous_tag_name(wrapper_list, idxs[0])
                prev_tag_name_sample = get_previous_tag_name(sample_list, idxs[1])
                curr_sample_tag_name = get_tag_name(next_item_s)
                curr_wrapper_tag_name = get_tag_name(next_item_w)

                # check if iterator
                if curr_wrapper_tag_name == prev_tag_name_wrapper:
                    square_candidate, new_idx = get_iterator_square_candidate(
                        prev_tag_name_wrapper, wrapper_list, idxs[0])
                    upper_square = get_upper_square(wrapper_list, idxs[0])
                    iterator, iterator_regex = is_iterator(upper_square, square_candidate)
                    if iterator:
                        # fix regex
                        regex_list = update_iterator_regex(regex_list, iterator_regex)
                        idxs[0] = new_idx + 1
                        continue

                if curr_sample_tag_name == prev_tag_name_sample:
                    square_candidate, new_idx = get_iterator_square_candidate(
                        prev_tag_name_sample, sample_list, idxs[1])
                    upper_square = get_upper_square(sample_list, idxs[1])
                    iterator, iterator_regex = is_iterator(upper_square, square_candidate)
                    if iterator:
                        # fix regex
                        regex_list = update_iterator_regex(regex_list, iterator_regex)
                        idxs[1] = new_idx + 1
                        continue

                # not iterator --> optional -- cross matching
                new_wrapper_idx, wrapper_next_tag = get_next_tag(wrapper_list, idxs[0])
                new_sample_idx, sample_next_tag = get_next_tag(sample_list, idxs[1])
                if wrapper_next_tag == curr_sample_tag_name:
                    # wrapper is optional
                    regex_to_add = wrapper_list[idxs[0]:new_wrapper_idx]
                    regex_to_add[0] = "(" + regex_to_add[0]
                    regex_to_add[-1] = regex_to_add[-1] + ")?"
                    regex_list = regex_list + regex_to_add
                    idxs[0] = new_wrapper_idx
                if sample_next_tag == curr_wrapper_tag_name:
                    # sample is optional
                    regex_to_add = sample_list[idxs[1]:new_sample_idx]
                    regex_to_add[0] = "(" + regex_to_add[0]
                    regex_to_add[-1] = regex_to_add[-1] + ")?"
                    regex_list = regex_list + regex_to_add
                    idxs[1] = new_sample_idx

            else:
                # string-tag mismatch --> sample string
                regex_list.append("(.*?)")
                idxs[1] += 1
        elif is_tag(next_item_s):
            # string-tag mismatch --> wrapper string
            regex_list.append("(.*?)")
            idxs[0] += 1
        else:
            # string mismatch
            regex_list.append("(.*?)")
            idxs[0] += 1
            idxs[1] += 1
    return regex_list


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


def clean_up(html1, html2):
    # remove the not necessary stuff
    cleaner = Cleaner(page_structure=False, style=True, safe_attrs=frozenset([]), )
    html1 = cleaner.clean_html(html1)
    html2 = cleaner.clean_html(html2)
    # transform to bs
    html1_bs = bs4.BeautifulSoup(html1, "lxml")
    html2_bs = bs4.BeautifulSoup(html2, "lxml")
    html1 = html1_bs.prettify()
    html2 = html2_bs.prettify()
    return html1, html2


def replace_tags(input_string: str):
    input_string = re.sub("<(.*?[^/])>", "<\g<1>.*?>", input_string)
    input_string = re.sub("<(.*?)/>", "<\g<1>.*?/>", input_string)
    return input_string


def get_wrapper(file_name1, file_name2, encoding="utf-8"):
    wrapper_content = open(base_content_path + file_name1, 'r', encoding=encoding).read()
    sample_content = open(base_content_path + file_name2, 'r', encoding=encoding).read()
    wrapper_content, sample_content = clean_up(wrapper_content, sample_content)
    print(wrapper_content)
    print("-------------------------------------------------------")
    print(sample_content)
    wrapper = html_to_list(wrapper_content)
    sample = html_to_list(sample_content)
    regex_list = compare_tree(wrapper, sample)
    regex = ""
    for regex_part in regex_list:
        regex += regex_part
    return regex


if __name__ == "__main__":
    # file1 = "../tests/test_html1.html"
    # file2 = "../tests/test_html2.html"
    # file1 = "../input/rtvslo.si/Audi.html"
    # file2 = "../input/rtvslo.si/Volvo.html"
    # file1 = "../input/overstock.com/jewelry01.html"
    # file2 = "../input/overstock.com/jewelry02.html"
    file1 = "../tests/html_example1.html"
    file2 = "../tests/html_example2.html"

    print(get_wrapper(file1, file2))
