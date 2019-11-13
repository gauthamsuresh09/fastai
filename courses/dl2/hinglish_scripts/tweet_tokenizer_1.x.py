from fastai.text import *

from .tweet_processing_utils import clean_tweet_text


class TweetsTokenizer(Tokenizer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        special_cases = ['TWITTERHASHTAG', 'TWITTERMENTION', 'TWITTEREMOJI']
        self.special_cases += special_cases

    def process_text(self, t:str, tok:BaseTokenizer) -> List[str]:
        t = clean_tweet_text(t) 
        return super().process_text(t, tok)
    
