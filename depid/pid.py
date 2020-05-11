from collections import Counter

from .utils import word_idx

class Depid(object):

    propositions = {
        "advcl",
        "advmod",
        "amod",
        "appos",
        "csubj",
        "csubjpass",
        "neg",
        "npadvmod",
        "nsubjpass",
        "nummod",
        "pobj",     # added later
        "poss",
        "predet",
        "preconj",
        "prep",
        "quantmod",
        "tmod",
        "vmod",
    }

    def __init__(self, count_conjunctions=False):
        self.prop_counter = Counter()
        self.tokens = 0
        if count_conjunctions:
            self.propositions.add("cc")

    def count_propositions(self, sent):
        tokens_out = []
        for token in sent:
            token_out = [token.orth_, token.lemma_, token.pos_, word_idx(token.head, sent), token.dep_]

            if self._is_token(token):
                self.tokens += 1
                token_out.append('T')
            else:
                token_out.append('')

            if self._is_proposition(token):
                prop = self._make_proposition(token)
                self.prop_counter[prop] += 1
                token_out.append(f'{prop[1]}: {prop[0]} {prop[2]}')
                if self.prop_counter[prop] == 1:
                    token_out.append('R')
                else:
                    token_out.append('')
            else:
                token_out.append('')
                token_out.append('')
            tokens_out.append(token_out)

        return tokens_out

    def _is_proposition(self, token):
        return (token.dep_ in self.propositions or (token.dep_ == "det" and token.lemma_ not in ('a', 'an', 'the'))
                or (token.dep_ == "nsubj" and not (token.tag_ == "PRP" and token.lemma_ in ("it", "this"))))

    def _make_proposition(self, token):
        return (token.lemma_, token.dep_, token.head.lemma_)

    def _is_token(self, token):
        return token.pos_ not in ('PUNCT', 'SPACE')

    def num_propositions(self, rep=False):
        if rep:
            return len(self.prop_counter)
        else:
            return sum(self.prop_counter.values())

    @property
    def num_tokens(self):
        return self.tokens



