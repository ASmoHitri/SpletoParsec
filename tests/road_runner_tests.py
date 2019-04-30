import unittest
from implementation import road_runner


class TestRoadRunnerMethods(unittest.TestCase):
    def test_get_iterator_square_candidate(self):
        # simple test
        test_html = "some item <i>test text</i></li></div>"
        self.assertEqual(["<li>", "some item", "<i>", "test text", '</i>', "</li>"],
                         road_runner.get_iterator_square_candidate("li", test_html))

        # search with nested tag test
        test_html = "some item <p>test text</p></p></div>"
        self.assertEqual(["<p>", "some item", "<p>", "test text", '</p>', "</p>"],
                         road_runner.get_iterator_square_candidate("p", test_html))
