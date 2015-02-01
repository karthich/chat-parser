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


    def test_link(self):
        output = self.parser.parse('This article explains what you are looking for http://goo.gl/8zH2Kr')
        self.assertEqual(
            '{"links": [{"url": "http://goo.gl/8zH2Kr", "title": "Rick Astley - Never Gonna Give You Up - YouTube"}]}',
            output)

        output = self.parser.parse('This one is definitely not going to work https://www.google.com')
        self.assertEqual('{"links": [{"url": "https://www.google.com", "title": "Google"}]}', output)

        output = self.parser.parse('This one never has any links')
        self.assertEqual('{}', output)

        output = self.parser.parse('This link doesnt really exist http://letsnotgofindthisanswerforallthepeopleintheworld.com')
        self.assertEqual('{}', output)

    def test_links(self):
        output = self.parser.parse(
            'Lets try these links http://www.nbcolympics.com and then this one http://goo.gl/8zH2Kr')
        self.assertEqual(
            '{"links": [{"url": "http://www.nbcolympics.com", "title": "NBC Olympics | Home of the 2016 Olympic Games in Rio"}, {"url": "http://goo.gl/8zH2Kr", "title": "Rick Astley - Never Gonna Give You Up - YouTube"}]}',
            output)

