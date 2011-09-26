#!/usr/bin/env python2

f = open('addr_book.csv')
to_fields = lambda line: line.strip().split('\t')
field_names = to_fields(f.readline())

def show_line(line):
    ret = []
    fields = to_fields(line)
    fields = [x for x in fields if x]
    print(' '.join(fields))
    # for idx, f in enumerate(field_names):
        # try:
        #     if fields[idx]:
        #         ret.append("%s -> %s" % (f, fields[idx]))
        # except IndexError:
        #     print(len(fields))
        #     print("position %d not found" % idx)

    return '\n'.join(ret)


if __name__ == '__main__':
    for line in f:
        print(show_line(line))
