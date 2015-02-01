import unittest
from chat_parser import ChatParser

__author__ = 'khariharan'


class TestChatParser(unittest.TestCase):

    def setUp(self):
        # Nothing to do here yet
        self.parser = ChatParser()

    def test_mention(self):
        output = self.parser.parse('Hey there my friend @Roman!')
        self.assertEqual('{"mentions": ["Roman"]}', output)

        output = self.parser.parse('Hey there my friend @!Roman')
        self.assertEqual('{}', output)

        output = self.parser.parse('hey there my friend roman')
        self.assertEqual('{}', output)

    def test_mentions(self):
        output = self.parser.parse("It's time for standup @Chris, @Rahul and @Ray!")
        self.assertEqual(output, '{"mentions": ["Chris", "Rahul", "Ray"]}')

    def test_emoticon(self):
        output = self.parser.parse('Is this the real (life)')
        self.assertEqual('{"emoticons": ["life"]}', output)

        output = self.parser.parse('Is this just (fantasy).... caught')
        self.assertEqual('{"emoticons": ["fantasy"]}', output)

        output = self.parser.parse('In (a (#landslide)')
        self.assertEqual('{}', output)

        output = self.parser.parse('No escape from reality')
        self.assertEquals('{}', output)

    def test_emoticons(self):
        output = self.parser.parse('Open your (eyes), look up to the (skies) and (seeeeeeeeee)')
        self.assertEqual('{"emoticons": ["eyes", "skies", "seeeeeeeeee"]}', output)



