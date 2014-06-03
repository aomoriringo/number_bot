#-*- coding:utf-8 -*-
import csv

class Sequence:
    def __init__(self, name, display_name, step, start, seq, num_type=1):
        # name, display_name: 数列の名称
        # step: seqのステップ数
        # start: seqのoffset
        # num_type: 数列の種別
        # 1 -> 名称を持った数列
        # 2 -> キリ番
        self.name = name
        self.seq = seq
        self.step = step
        self.start = start
        self.num_type = num_type
        self.display_name = display_name if display_name else name
        # dname = display_name if display_name else name
        # if isinstance(dname, str):
        #     self.display_name = dname.decode('utf-8')
        # else:
        #     self.display_name = dname

class SequenceList(list):
    def __init__(self):
        list.__init__(self)

    def import_csv(self, filename):
        num_reader = csv.reader(open(filename, 'r'), delimiter=',', skipinitialspace=True)
        for row in num_reader:
            self.append(
                Sequence(
                    row[0], row[2], int(row[1]),
                    1, [int(x) for x in row[3:]])
                )

    def search(self, target):
        for s in self:
            seq = s.seq
            if target in seq:
                id = seq.index(target)
                return s.display_name, (id + s.start) * s.step, s.num_type
        return None


#seqs = SequenceList()
#seqs.import_csv('numbers.csv')

turnings = []
turnings += [x*100 for x in range(1,9)]
turnings += [x*1000 for x in range(1,9)]
turnings += [x*10000 for x in range(1,9)]
turnings += [x*100000 for x in range(1,9)]
turnings += [x*111 for x in range(1,9)]
turnings += [x*1111 for x in range(1,9)]
turnings += [x*11111 for x in range(1,9)]
turnings += [x*111111 for x in range(1,9)]
#seqs.append(Sequence('turning point numbers', 1, 1, turnings, 2))

def print_nums(_from, to):
    for x in range(_from, to):
        s = seqs.search(x)
        if s:
            print x, " -> ", s[0], s[1], 'th'
        else:
            pass

def num_count(_from, to, step):
    from_idx = _from
    while from_idx < _from:
        to_idx = from_idx + step
        for x in range(from_idx, to_idx):
            s = seqs.search(x)
