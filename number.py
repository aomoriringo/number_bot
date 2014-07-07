#-*- coding:utf-8 -*-
from inflect import engine
#from number_bot import LANGUAGES

class Number:
    def __init__(self, name, display_name, num, order):
        self.name = name
        self.display_name = display_name
        self.num = num
        self.order = order
        self.engine = engine()
    #def set_language(self, lang='en'):
    #    LANGUAGES[lang].install()

    def get_message(self, username, lang='en'):
        detail = self.get_detail_text(lang)
        if lang=='ja':
            return "@%s さんのツイート数が%sに達しました" \
                   % (username, detail)
        else:
            return "@%s's tweet count has reached %s." \
                   % (username, detail)

class NamedNumber(Number):
    def get_detail_text(self, lang):
        if lang=='ja':
            return "%s番目の%s %s" \
                   % (self.order, self.display_name, self.num)
        else:
            ord_ = self.engine.ordinal(self.order)
            return "%s %s, %s" \
                   % (ord_, self.name, self.num)

class PowerNumber(Number):
    def get_detail_text(self, lang):
        if lang=='ja':
            return "%sの%s乗 %s" \
                    % (self.name, self.order, self.num)
        else:
            ord_ = self.engine.ordinal(self.order)
            return "%s power of %s, %s" \
                    % (ord_, self.name, self.num)

class RoundNumber(Number):
    def get_detail_text(self, lang):
        return "%s" % self.num

