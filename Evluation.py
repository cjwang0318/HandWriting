import re


def read_file(path, skip_lines_num):
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
    lines = lines[skip_lines_num:]
    return lines


def get_value(str):
    match = re.search(r'\'([^"]*)\'', str)
    result = match.group(1)
    # print(result)
    return result


def cal_accuracy_chars(test_str, groundtruth_str):
    right = 0
    wrong = 0

    test_chars = list(test_str)
    groundtruth_chars = list(groundtruth_str)
    if len(test_chars) == len(groundtruth_str):
        for i, element in enumerate(test_chars):
            if test_chars[i] == groundtruth_chars[i]:
                right = right + 1
            else:
                wrong = wrong + 1
    else:
        print("測試資料數量與標準答案數量不一致")
    result = [right, wrong]  # [# of right chars, # of wrong chars]
    return result


def cal_accuracy_rate(eval_result):
    accuracy_rate = eval_result[0] / (eval_result[0] + eval_result[1])
    return accuracy_rate


if __name__ == '__main__':
    paddle_output_file = "./evaluation/rec_result.txt"
    ground_truth = "./evaluation/rec_gt_sort.txt"
    predictList = []
    GTList = []
    fileList = read_file(paddle_output_file, 1)
    fileList.sort()
    for line in fileList:
        print(line)
        value = get_value(line)
        predictList.append(str(value))
    fileList = read_file(ground_truth, 0)
    fileList.sort()
    for line in fileList:
        value = line.split("\t")
        GTList.append(str(value[1]))

    result = cal_accuracy_chars(predictList, GTList)
    acc = cal_accuracy_rate(result)
    print(acc)
