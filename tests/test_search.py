import unittest

from src.main import _search


class TestSearch(unittest.TestCase):
    def test_sm_seed(self):
        step = 417
        needles = [6, 10, 9, 15, 10, 0, 2, 7, 5, 8]
        results = _search(step, needles)

        expect = {"results": [{"seed": "bd1646f7",
                               "encoded_needle": "098726e4", "step": 417}]}
        self.assertEqual(expect, results)

    def test_usm_seed(self):
        step = 477
        needles = [9, 10, 7, 11, 12, 15, 7, 7]
        results = _search(step, needles)

        expect = {"results": [{"seed": "c31a2f06",
                               "encoded_needle": "0dd53f07", "step": 477}]}
        self.assertEqual(expect, results)

    def test_sm_id_seed(self):
        step = 1012
        needles = [2, 14, 5, 6, 10, 15, 7, 6, 6]
        results = _search(step, needles, True)

        expect = {"results": [
            {"add": 15, "seed": "f9337724",
                "encoded_needle": "07257578", "step": 1012},
            {"add": 10, "seed": "53c58ec3",
                "encoded_needle": "0d59b899", "step": 1012},
            {"add": 10, "seed": "01919810",
                "encoded_needle": "0d59b899", "step": 1012}]}
        self.assertEqual(expect, results)

    def test_usm_id_seed(self):
        step = 1132
        needles = [9, 10, 7, 11, 12, 15, 7, 7, 0]
        results = _search(step, needles, True)

        expect = {"results": [
            {"add": 0, "seed": "84550450",
                "encoded_needle": "0dd53f07", "step": 1132},
            {"add": 13, "seed": "765f81aa",
                "encoded_needle": "13f28f42", "step": 1132},
            {"add": 11, "seed": "1e300ec2",
                "encoded_needle": "16ffde7e", "step": 1132},
            {"add": 3, "seed": "1b19e915",
                "encoded_needle": "093f4202", "step": 1132},
        ]}
        self.assertEqual(expect, results)
