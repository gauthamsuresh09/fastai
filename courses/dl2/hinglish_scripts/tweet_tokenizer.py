from fastai.text import *

from .tweet_processing_utils import clean_tweet_text
from typing import List

class TweetsTokenizer(Tokenizer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        special_cases = ['TWITTERHASHTAG', 'TWITTERMENTION', 'TWITTEREMOJI']
        for w in special_cases:
            self.tok.tokenizer.add_special_case(w, [{ORTH: w}])

    def proc_text(self, t:str) -> List[str]:
        t = clean_tweet_text(t) 
        return super().proc_text(t)

    @staticmethod
    def proc_all(ss, lang):
        tok = TweetsTokenizer(lang)
        return [tok.proc_text(s) for s in ss]

    @staticmethod
    def proc_all_mp(ss, lang='en', ncpus = None):
        ncpus = ncpus or num_cpus()//2
        with ProcessPoolExecutor(ncpus) as e:
            return sum(e.map(TweetsTokenizer.proc_all, ss, [lang]*len(ss)), [])
