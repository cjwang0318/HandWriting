import sys
def read_file(path, skip_lines_num):
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
    lines = lines[skip_lines_num:]
    return lines
if __name__ == '__main__':
    lines=read_file('test.txt',0)
    for line in lines:
        res = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in line)
        print(res)

