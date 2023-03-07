import os
from tqdm import tqdm


def read_file(path, skip_lines_num):
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
    lines = lines[skip_lines_num:]
    return lines


def write_file(path, write_data):
    with open(path, 'w', encoding='utf-8') as writer:
        writer.writelines(write_data)


def get_unicode(str):
    res = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in str)


if __name__ == '__main__':
    # load paddle chinese dictionary
    root_path = "D:/temp/Gnt1.2Test"
    cht_dict = read_file("./paddle/chinese_cht_dict.txt", 0)
    gt_list = read_file(root_path + "/gt.txt", 0)
    output_list = []
    for line in tqdm(gt_list):
        temp = line.split('\t')
        path = temp[0]
        gt_word = temp[1]
        if gt_word in cht_dict:
            # print(gt_word)
            output_list.append(line + "\n")
        else:
            # print("./output/images/"+path)
            os.remove(root_path + "/images/" + path)
    write_file(root_path + "/gt_filtered.txt", output_list)
