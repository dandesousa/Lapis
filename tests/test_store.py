#!/usr/bin/env python
# encoding: utf-8

import tempfile
import unittest
from lapis.store import Store


class TestStore(unittest.TestCase):
    """tests store related functions"""

    def setUp(self):
        self.__sqlite_file = tempfile.NamedTemporaryFile()
        self.__content_path = ""
        self.__store = Store(self.__sqlite_file.name, self.__content_path)

        from lapis.models import Tag
        self.__store.get_or_create(Tag, name="tag1")
        self.__store.get_or_create(Tag, name="tag2")
        self.__store.get_or_create(Tag, name="tag3")

    def tearDown(self):
        self.__sqlite_file.close()

    def test_tag_list(self):
        """tests that all tags exist and that they are returned when the regular expression is right"""
        tag_list = ("tag1", "tag2", "tag3")

        tags = list(self.__store.tags(""))
        self.assertEqual(3, len(tags))
        self.assertTrue(all((tag.name in tag_list for tag in tags)))

        tags = list(self.__store.tags("^tag"))
        self.assertEqual(3, len(tags))
        self.assertTrue(all((tag.name in tag_list for tag in tags)))

        tags = list(self.__store.tags("^tag2"))
        self.assertEqual(1, len(tags))
        self.assertTrue(tags[0].name == "tag2")

    def test_empty_tags(self):
        tags = list(self.__store.tags("^fake_tag$"))
        self.assertFalse(tags)