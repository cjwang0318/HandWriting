import os
import random
import shutil

def write_file(path, write_data):
    with open(path, 'w', encoding='utf-8') as writer:
        writer.writelines(write_data)

def move_and_rename_file():
    shutil.move('/home/user/Downloads/test.txt', '/home/user/Documents/useful_name.txt')

def get_file_name(mypath):
    # 獲取當前資料夾名稱然後存成dir_path變數
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # print(dir_path)
    # 讀取資料夾內所有檔案名稱然後放進all_file_name這個list裡
    all_file_name = os.listdir(mypath)
    # print(all_file_name)
    return dir_path, all_file_name

def convert_to_paddle_ocr_format(dir_path, all_file_name, ocr_data_path, fold_portion):
    training_data_format = []
    testing_data_format = []
    for file in all_file_name:
        word_name = file[0]
        # print(word_name)
        if random.random() < fold_portion:
            str = f"{ocr_data_path}/{file}\t{word_name}"
            training_data_format.append(str+"\n")
        else:
            str = f"{ocr_data_path}/{file}\t{word_name}"
            testing_data_format.append(str+"\n")
    write_file("rec_gt_train.txt", training_data_format)
    write_file("rec_gt_test.txt", testing_data_format)

def convert_to_paddle_ocr_num_format(dir_path, all_file_name, ocr_data_path, fold_portion):
    training_data_format = []
    testing_data_format = []
    count=1
    for file in all_file_name:
        word_name = file[0]
        # print(word_name)
        if random.random() < fold_portion:
            old_file_name=f"{dir_path}/{file}"
            #print("%06d" % count)
            file="img_%06d.png" % count
            new_file_name = f"./data/paddle_format/{file}"
            shutil.move(old_file_name,new_file_name)
            str = f"{ocr_data_path}/{file}\t{word_name}"
            training_data_format.append(str+"\n")
        else:
            old_file_name = f"{dir_path}/{file}"
            # print("%06d" % count)
            file = "img_%06d.png" % count
            new_file_name = f"./data/paddle_format/{file}"
            shutil.move(old_file_name, new_file_name)
            str = f"{ocr_data_path}/{file}\t{word_name}"
            testing_data_format.append(str+"\n")
        count += 1
    write_file("rec_gt_train.txt", training_data_format)
    write_file("rec_gt_test.txt", testing_data_format)

if __name__ == '__main__':
    # 指定要列出所有檔案的目錄
    mypath = "./data/cleaned_data(50_50)"
    ocr_data_path = "cleaned_data(50_50)"
    fold_portion = 0.8  # 80% for training and 20% for testing
    dir_path, all_file_name = get_file_name(mypath)
    #convert_to_paddle_ocr_format(dir_path, all_file_name, ocr_data_path, fold_portion)
    convert_to_paddle_ocr_num_format(mypath, all_file_name, ocr_data_path, fold_portion)

