import json

__author__ = 'khariharan'
import re
import urllib2
from BeautifulSoup import BeautifulSoup


class ChatParser(object):
    # This is just a stub for now
    """
        message - text message to parse for mentions, emoticons, urls
    """

    def parse(self, message):
        words = self.split_message_into_words(message)

        mentions = []
        emoticons = []
        links = []

        # Going to go ahead and assume that a word can be only a mention or emoticon or url
        for word in words:
            parsed_output_mentions = self._parse_for_mentions(word)
            if parsed_output_mentions is not None:
                mentions.append(parsed_output_mentions)
                continue

            parsed_output_emoticons = self._parse_for_emoticons(word)
            if parsed_output_emoticons is not None:
                emoticons.append(parsed_output_emoticons)
                continue

            parsed_output_links = self._parse_for_links(word)
            if parsed_output_links is not None:
                links.append(parsed_output_links)
                continue

        parsed_output = {}

        if len(mentions) > 0:
            parsed_output['mentions'] = mentions

        if len(emoticons) > 0:
            parsed_output['emoticons'] = emoticons

        if len(links) > 0:
            parsed_output['links'] = links

        return json.dumps(parsed_output)


    def split_message_into_words(self, message):
        # Lets just split by whitespace for now. Maybe there is an edge case later
        # Neat trick: Passing no arguments to split makes it split by whitespace
        # (http://stackoverflow.com/questions/8113782/split-string-on-whitespace-in-python)
        return message.split()


    def _parse_for_mentions(self, word):
        # Three things can happen here.
        # No mention is made, in which case an attribute error is thrown (handle it accordingly)
        # Mention is made, parse it (happy path)
        # Word that starts with @ but not followed by an actual word character class passed (e.g @!Roman)
        # just return '@' and we can filter it out
        match = re.search("""^@[\w]*""", word)
        try:
            matched_word = match.group(0)

            # invalid mention
            if matched_word == '@':
                return None
            else:
                # Happy path
                return matched_word[1:]

        except AttributeError:
            # no mention was made
            return None


    def _parse_for_emoticons(self, word):
        # Same as before except that it wont match with anything that doesnt fit that pattern (word_characters)
        match = re.search("""^\([\w]*\)[\.,;?!]*$""", word)
        try:
            matched_word = match.group(0)
            return matched_word[matched_word.find("(") + 1:matched_word.find(")")]

        except AttributeError:
            return None

    def _parse_for_links(self, word):
        match = re.search("""^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$""", word)
        try:
            matched_word = match.group(0)
            soup = BeautifulSoup(urllib2.urlopen(matched_word))
            title = soup.title.string
            if title is not None:
                return {'url': matched_word, 'title': soup.title.string}
            else:
                return None

        except AttributeError:
            return None
        except urllib2.URLError:
            return None

