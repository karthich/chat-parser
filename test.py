import unittest
from chat_parser import ChatParser

__author__ = 'khariharan'

class TestChatParser(unittest.TestCase):

    def setUp(self):
        # Nothing to do here yet
        self.parser = ChatParser()

    def test_mentions(self):
        output = self.parser.parse('Hey there my friend @Roman!')
        self.assertEqual('{"mentions": ["Roman"]}', output)

        output = self.parser.parse('Hey there my friend @!Roman')
        self.assertEqual('{}', output)

        output = self.parser.parse('hey there my friend roman')
        self.assertEqual('{}', output)

    def test_multiple_mentions(self):
        output = self.parser.parse("It's time for standup @Chris, @Rahul and @Ray!")
        self.assertEqual(output, '{"mentions": ["Chris", "Rahul", "Ray"]}')

