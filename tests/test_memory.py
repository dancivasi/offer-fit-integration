import pytest
import csv
import json
from memory import data


def test_csv_file_has_data():
    with open('events.csv', 'r') as csv_file:
        csv_check = csv.reader(csv_file)
        data = list(csv_check)
    words_found = any(any(word.isalpha() for word in row) for row in data)
    assert words_found is True


def test_json_file_has_data():
    with open('events.json', 'r') as json_file:
        data = json.load(json_file)
    assert len(data) > 0


def test_data_is_in_memory():
    assert len(data) > 0
