# -*- coding: utf-8 -*-

import unittest
import json
from collections import defaultdict
from nltk.tokenize import word_tokenize
import requests
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from index.auxiliaries import load_data, create_index, save_index, save_stats

class TestIndexMethods(unittest.TestCase):

    def test_load_data(self):
        data = load_data("urls.json")
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_create_index(self):
        data = load_data("urls.json")
        stemmer = PorterStemmer()
        index, pos_index, stats = create_index(data, stemmer)
        self.assertIsInstance(index, defaultdict)
        self.assertIsInstance(pos_index, defaultdict)
        self.assertIsInstance(stats, dict)

    def test_save_index(self):
        index = defaultdict(list)
        index['test'] = ['url1']
        save_index(index, "test_index.json")
        with open("test_index.json", "r") as f:
            saved_index = json.load(f)
        self.assertEqual(index, saved_index)

    def test_save_stats(self):
        stats = {"num_docs": 2, "num_tokens": 10, "avg_tokens_per_doc": 5}
        save_stats(stats, "test")