#-*- coding:utf-8 -*-
import csv
from prime import prime_table

class Number:
    def __init__(self, name, display_name, num, order):
        self.name = name
        self.display_name = display_name
        self.num = num
        self.order = order

class NamedNumber(Number):
    def get_message(self, username):
        return "@%s さんのツイート数が%s番目の%s %sに達しました" \
            % (username, self.order, self.display_name, self.num)

class PowerNumber(Number):
    def get_message(self, username):
        return "@%s さんのツイート数が%sの%s乗 %sに達しました" \
            % (username, self.name, self.order, self.num)

class RoundNumber(Number):
    def get_message(self, username):
        return "@%s さんのツイート数が%sに達しました" \
            % (username, self.num)

class Sequence:
    def __init__(self, name, display_name, step, seq, num_class):
        # name, display_name: 数列の名称
        # step: seqのステップ数
        self.name = name
        self.seq = seq
        self.step = step
        self.num_class = num_class
        self.display_name = display_name if display_name else name

    def order(self, target):
        if not self.exists_num(target):
            return None
        id_ = self.seq.index(target) + 1
        return id_ * self.step

    def exists_num(self, target):
        return target in self.seq

    def get_num(self, target):
        if not self.exists_num(target):
            return None
        return self.num_class(self.name, self.display_name,
                              target, self.order(target))

class SequenceList(list):
    def __init__(self, filename=None):
        list.__init__(self)
        if filename:
            self.import_csv(filename)

    def import_csv(self, filename):
        num_reader = csv.reader(open(filename, 'r'), delimiter=',', skipinitialspace=True)
        for row in num_reader:
            seq = self.gen_sequence(row)
            self.append(seq)

    def search(self, target):
        for s in self:
            if s.exists_num(target):
                return s.get_num(target)
        return None

class PrimeSequenceList(SequenceList):
    def __init__(self, to=None, step=100):
        list.__init__(self)
        if to:
            self.extend_primes(to, step)

    def extend_primes(self, to, step):
        name = 'prime'
        display_name = '素数'
        _ptable = prime_table(to)
        ptable = [n for i, n in enumerate(_ptable) if (i+1)%step==0]
        self.append(Sequence(name, display_name, step, ptable, NamedNumber))

class NamedSequenceList(SequenceList):
    def gen_sequence(self, csvrow):
        '''
        csv format
        [sequence name] [step] [display name] [numbers...]
        '''
        name         = csvrow[0]
        step         = int(csvrow[1])
        display_name = csvrow[2]
        nums         = [int(x) for x in csvrow[3:]]
        return Sequence(name, display_name, step, nums, NamedNumber)

class PowerSequenceList(SequenceList):
    def gen_sequence(self, csvrow):
        '''
        csv format
        [base number] [numbers...]
        '''
        name         = csvrow[0]
        nums         = [int(x) for x in csvrow[1:]]
        return Sequence(name, name, 1, nums, PowerNumber)

class RoundSequenceList(SequenceList):
    def gen_sequence(self, csvrow):
        '''
        csv format
        [numbers...]
        '''
        nums = [int(x) for x in csvrow]
        return Sequence('round', '', 1, nums, RoundNumber)

def get_sequences():
    seq = SequenceList()
    seq.extend(NamedSequenceList('data/named_numbers.csv'))
    seq.extend(PrimeSequenceList(1000000, 10))
    seq.extend(PowerSequenceList('data/power_numbers.csv'))
    seq.extend(RoundSequenceList('data/round_numbers.csv'))
    return seq
