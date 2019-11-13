import re

import emoji
emojis = list(emoji.UNICODE_EMOJI.keys())

emoji_pattern = re.compile(
    "["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U00002760-\U0000276F"  # emoticons
    "]+", flags=re.UNICODE
)

emoji_regex = re.compile("[" + u"".join(emojis) + "]", flags=re.UNICODE)

def clean_tweet_text(line, preserve_tags=False):
    if line[:3] == 'RT ':
        line = line[3:]
    cleaned_line = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', line)
    cleaned_line = re.sub(r'pic\.twitter\.com\/\w+','',cleaned_line)
    cleaned_line = re.sub(r'( *(\.( *))+)',' . ', cleaned_line)
    if preserve_tags:
        cleaned_line = re.sub(r'@(\w{1,15})( )*(:)*',' TWITTERMENTION ',cleaned_line)
        cleaned_line = re.sub(r'#\w*[a-zA-Z]+\w*',' TWITTERHASHTAG ', cleaned_line)
    else:
        cleaned_line = re.sub(r'@(\w{1,15})( )*(:)*',' ',cleaned_line)
        cleaned_line = re.sub(r'#\w*[a-zA-Z]+\w*',' ', cleaned_line)
    cleaned_line = emoji_regex.sub(' TWITTEREMOJI ', cleaned_line)
    cleaned_line = re.sub(r'(\s+|\n+)',' ',cleaned_line)
    return cleaned_line

def get_text_from_tweet(tweet):
    if 'retweeted_status' in tweet.keys():
        if 'extended_tweet' in tweet['retweeted_status']:
            text = tweet['retweeted_status']['extended_tweet']['full_text']
        else:
            text = tweet['retweeted_status']['text']
    else:
        if 'extended_tweet' in tweet:
            text = tweet['extended_tweet']['full_text']
        else:
            text = tweet['text']
    return text
