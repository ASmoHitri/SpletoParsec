import unittest
from implementation import road_runner


class TestRoadRunnerMethods(unittest.TestCase):
    def test_get_next_item(self):
        # string test
        test_html = "      some item \n <i>test text</i></li></div>"
        self.assertEqual(("some item", "<i>test text</i></li></div>"),
                         road_runner.get_next_item(test_html))

        # start tag test
        test_html = "<i>test text</i></li></div>"
        self.assertEqual(("<i>", "test text</i></li></div>"), road_runner.get_next_item(test_html))

        # end tag test
        test_html = "</li></div>"
        self.assertEqual(("</li>", "</div>"), road_runner.get_next_item(test_html))

    # def test_is_tag(self):
    #     self.assertEqual(False, road_runner.is_tag("nisem tag>"))           # False test
    #     self.assertEqual(True, road_runner.is_tag("<tag>"))                 # True test - start tag
    #     self.assertEqual(True, road_runner.is_tag("</tag>"))                # True test - end tag
        # self.assertEqual(True, road_runner.is_tag("<  img  sranje 4y7h3p78gp 9hrgu   55%  />", 'both')

    def test_replace_tags(self):
        self.assertEqual('<bla.*?>, bla, </bla blblaa.*?>, <bbbb , <ajajaja e2 .*?/>',
                         road_runner.replace_tags("<bla>, bla, </bla blblaa>, <bbbb , <ajajaja e2 />"))

    def test_get_iterator_square_candidate(self):
        # simple test
        test_html = ["</div>",
                     "<li>", "previous item", "</li>",
                     "<li>", "some item", "<i>", "test text", '</i>', "</li>",
                     "<div>"]
        self.assertEqual((["<li>", "some item", "<i>", "test text", '</i>', "</li>"], 9),
                         road_runner.get_iterator_square_candidate("li", test_html, 4))

        # # search with nested tag test 1
        # test_html = ["<p>", "some item", "<p>", "test text", "</p>", "</p>", "</div>", "</p>"]
        # self.assertEqual((["<p>", "some item", "<p>", "test text", '</p>', "</p>"], 5),
        #                  road_runner.get_iterator_square_candidate("p", test_html, 0))

        # # search with nested tag test 2
        # test_html = ["<p>", "some item", "<p>", "test text", "</p>", "</p>", "</p>"]
        # self.assertEqual((["<p>", "some item", "<p>", "test text", '</p>', "</p>"], 5),
        #                  road_runner.get_iterator_square_candidate("p", test_html, 0))

    def test_get_previous_tag_name(self):
        # no string between test
        html_list = ["<li>", "best item", "</li>", "<div>"]
        self.assertEqual("li", road_runner.get_previous_tag_name(html_list, 3))

        # string between test
        html_list = ["<li>", "best item", "</li>", "some text", "<div>"]
        self.assertEqual("li", road_runner.get_previous_tag_name(html_list, 4))

    def test_get_upper_square(self):
        # simple test
        html_list = ["</li>", "<li>", "best item", "</li>", "<li>", "more text"]
        self.assertEqual(["<li>", "best item", "</li>"], road_runner.get_upper_square(html_list, 4))

        # test with nested tags
        html_list = ["</p>", "<p>", "best text", "<p>", "inner text", "</p>", "</p>", "<p>"]
        self.assertEqual(["<p>", "best text", "<p>", "inner text", "</p>", "</p>"],
                         road_runner.get_upper_square(html_list, 7))

    def test_update_iterator_regex(self):
        regex_list = ["<div>", "(.*?)", "(<img>", "r1", "r2", "</img>)?",
                      "(<li>", "dfjsdf", "</li>)?"]
        iterator_regex_list = ["<img>", "(.*?)", "</img>"]
        self.assertEqual(['<div>', '(.*?)', '(<img>', '(.*?)', '</img>\s*)*', '(<li>', 'dfjsdf', '</li>)?'],
                         road_runner.update_iterator_regex(regex_list, iterator_regex_list))

        regex_list = ["<div>", "(.*?)", "(<img>", "r1", "r2", "</img>)*",
                      "(<li>", "dfjsdf", "</li>)?"]
        iterator_regex_list = ["<img>", "(.*?)", "</img>"]
        self.assertEqual(["<div>", "(.*?)", "(<img>", "r1", "r2", "</img>)*", "(<li>", "dfjsdf", "</li>)?"],
                         road_runner.update_iterator_regex(regex_list, iterator_regex_list))

        regex_list = ["<div>", "(.*?)", "<img>", "(.*?)", "</img>", "<img>", "(.*?)", "</img>",
                      "(<li>", "dfjsdf", "</li>)?"]
        self.assertEqual(["<div>", "(.*?)", "(<img>", "(.*?)", "</img>\s*)*", "(<li>", "dfjsdf", "</li>)?"],
                         road_runner.update_iterator_regex(regex_list, iterator_regex_list))
