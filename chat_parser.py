import json

__author__ = 'khariharan'
import re

class ChatParser(object):
    # This is just a stub for now
    """
        message - text message to parse for mentions, emoticons, urls
    """

    def parse(self, message):
        words = self.split_message_into_words(message)

        mentions = []

        # Going to go ahead and assume that a word can be only a mention or emoticon or url
        for word in words:
            parsed_output_mentions = self._parse_for_mentions(word)
            if parsed_output_mentions is not None:
                mentions.append(parsed_output_mentions)
                continue

        parsed_output = {}

        if len(mentions) > 0:
            parsed_output['mentions'] = mentions

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

