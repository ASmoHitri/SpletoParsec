import unittest
from implementation import road_runner


class TestRoadRunnerMethods(unittest.TestCase):
    def test_get_next_item(self):
        # string test
        test_html = "      some item \n <i>test text</i></li></div>"
        self.assertEqual(("some item", "<i>test text</i></li></div>"), road_runner.get_next_item(test_html))

        # start tag test
        test_html = "<i>test text</i></li></div>"
        self.assertEqual(("<i>", "test text</i></li></div>"), road_runner.get_next_item(test_html))

        # end tag test
        test_html = "</li></div>"
        self.assertEqual(("</li>", "</div>"), road_runner.get_next_item(test_html))

    def test_is_tag(self):
        self.assertEqual(False, road_runner.is_tag("nisem tag>"))           # False test
        self.assertEqual(True, road_runner.is_tag("<tag>"))                 # True test - start tag
        self.assertEqual(True, road_runner.is_tag("</tag>"))                # True test - end tag

    def test_get_iterator_square_candidate(self):
        # simple test
        test_html = "some item <i>test text</i></li></div>"
        self.assertEqual((["<li>", "some item", "<i>", "test text", '</i>', "</li>"], "</div>"),
                         road_runner.get_iterator_square_candidate("li", test_html))

        # search with nested tag test 1
        test_html = "some item <p>test text</p></p></div></p>"
        self.assertEqual((["<p>", "some item", "<p>", "test text", '</p>', "</p>"], "</div></p>"),
                         road_runner.get_iterator_square_candidate("p", test_html))

        # search with nested tag test 2
        test_html = "some item <p>test text</p></p></p>"
        self.assertEqual((["<p>", "some item", "<p>", "test text", '</p>', "</p>"], "</p>"),
                         road_runner.get_iterator_square_candidate("p", test_html))

    def test_get_next_different_tag(self):
        # TODO
        pass

    def test_get_previous_tag_name(self):
        # no string between test
        html_list = ["<li>", "best item", "</li>", "<div>"]
        self.assertEqual("li", road_runner.get_previous_tag_name(html_list))

        # string between test
        html_list = ["<li>", "best item", "</li>", "some text", "<div>"]
        self.assertEqual("li", road_runner.get_previous_tag_name(html_list))

    def test_get_upper_square(self):
        # simple test
        html_list = ["</li>", "<li>", "best item", "</li>", "<li>"]
        self.assertEqual(["<li>", "best item", "</li>"], road_runner.get_upper_square(html_list))

        # test with nested tags
        html_list = ["</p>", "<p>", "best text", "<p>", "inner text", "</p>", "</p>", "<p>"]
        self.assertEqual(["<p>", "best text", "<p>", "inner text", "</p>", "</p>"], road_runner.get_upper_square(html_list))