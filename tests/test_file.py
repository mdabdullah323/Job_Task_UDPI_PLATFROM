from unittest import TestCase
from file import File


class TestFile(TestCase):
    file = File("./data/test_database.json")

    def test_create_and_save_file(self):
        _data = [{"key": "value"}]
        self.file.data = _data
        self.assertEqual(_data, self.file.data)
