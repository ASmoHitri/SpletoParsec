import re
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


def is_tag(string):
    if string[0] == "<":
        return True
    return False


def get_iterator_square_candidate(tag_name, items_list, curr_idx):
    num_of_opening_tags = 1
    square_list = ["<{}>".format(tag_name)]
    while num_of_opening_tags > 0:
        curr_idx = curr_idx + 1
        next_item = items_list[curr_idx]
        if next_item == "</{}>".format(tag_name):
            num_of_opening_tags -= 1
        elif next_item == "<{}>".format(tag_name):
            num_of_opening_tags += 1
        square_list.append(next_item)
    return square_list, curr_idx


def get_next_different_tag(tag_name, html):
    regex = "(?<=</{0}>)\s*(</?[^{0}]>)".format(tag_name)
    match = re.search(regex, html)
    if match:
        return match.group(1)
    return None


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
                    square_candidate, new_idx = get_iterator_square_candidate(prev_tag_name_wrapper, wrapper_list, idxs[0])
                    upper_square = get_upper_square(wrapper_list, idxs[0])
                    iterator, iterator_regex = is_iterator(upper_square, square_candidate)
                    if iterator:
                        # fix regex
                        idxs[0] = new_idx
                        continue

                if curr_sample_tag_name == prev_tag_name_sample:
                    square_candidate, new_idx = get_iterator_square_candidate(prev_tag_name_sample, sample_list, idxs[1])
                    upper_square = get_upper_square(sample_list, idxs[1])
                    iterator, iterator_regex = is_iterator(upper_square, square_candidate)
                    if iterator:
                        # fix regex
                        idxs[1] = new_idx
                        continue


                # not iterator --> optional -- cross matching
                # TODO ne bo okkk, rabis indexe!!
                # wrapper_next = get_next_different_tag(curr_wrapper_tag_name, wrapper_html)
                # sample_next = get_next_different_tag(curr_sample_tag_name, sample_html)

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
    # print(get_next_different_tag("li", html))

    regex_str = "</?(\w*)[\s\S]*?>"
    print(re.search(regex_str, "</li class=jfke>").group(1))

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







