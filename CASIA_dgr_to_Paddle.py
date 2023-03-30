import struct
import os

from pathlib import Path
from PIL import Image
import cv2 as cv
import numpy as np
from tqdm import tqdm


def write_txt(save_path: str, content: list, mode='w'):
    """
    將list內容寫入txt中
    @param
    content: list格式內容
    save_path: 絕對路徑str
    @return:None
    """
    with open(save_path, mode, encoding='utf-8') as f:
        for value in content:
            f.write(value + '\n')


def read_from_dgrl(dgrl, train_txt):
    if not os.path.exists(dgrl):
        print('DGRL not exis!')
        return

    dir_name, base_name = os.path.split(dgrl)
    label_dir = dir_name + '_label'
    image_dir = dir_name + '_images'
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    with open(dgrl, 'rb') as f:
        # 讀取表頭尺寸
        header_size = np.fromfile(f, dtype='uint8', count=4)
        header_size = sum([j << (i * 8) for i, j in enumerate(header_size)])
        # print(header_size)

        # 讀取表頭剩下內容，提取 code_length
        header = np.fromfile(f, dtype='uint8', count=header_size - 4)
        code_length = sum([j << (i * 8) for i, j in enumerate(header[-4:-2])])
        # print(code_length)

        # 讀取圖像尺寸資訊，提取圖像中行數量
        image_record = np.fromfile(f, dtype='uint8', count=12)
        height = sum([j << (i * 8) for i, j in enumerate(image_record[:4])])
        width = sum([j << (i * 8) for i, j in enumerate(image_record[4:8])])
        line_num = sum([j << (i * 8) for i, j in enumerate(image_record[8:])])
        print('圖像尺寸:')
        print(height, width, line_num)
        img_ori = np.zeros((height, width), np.uint8)
        img_ori.fill(255)

        '''for save txt'''
        append_txt = []
        # 讀取每一行的資訊
        for k in range(line_num):
            print(k + 1)

            # 讀取該行的字元數量
            char_num = np.fromfile(f, dtype='uint8', count=4)
            char_num = sum([j << (i * 8) for i, j in enumerate(char_num)])
            print('字元數量:', char_num)

            # 讀取該行的標註資訊
            label = np.fromfile(f, dtype='uint8', count=code_length * char_num)
            label = [label[i] << (8 * (i % code_length))
                     for i in range(code_length * char_num)]
            label = [sum(label[i * code_length:(i + 1) * code_length])
                     for i in range(char_num)]
            label = [struct.pack('I', i).decode(
                'gbk', 'ignore')[0] for i in label]
            print('合併前：', label)
            label = ''.join(label)
            # 去掉不可見字元 \x00，這一步不加的話後面保存的內容會出現看不見的問題
            label = ''.join(label.split(b'\x00'.decode()))
            print('合併後：', label)

            # 讀取該行的位置和尺寸
            pos_size = np.fromfile(f, dtype='uint8', count=16)
            y = sum([j << (i * 8) for i, j in enumerate(pos_size[:4])])
            x = sum([j << (i * 8) for i, j in enumerate(pos_size[4:8])])
            h = sum([j << (i * 8) for i, j in enumerate(pos_size[8:12])])
            w = sum([j << (i * 8) for i, j in enumerate(pos_size[12:])])
            # print(x, y, w, h)
            '''調大y避免重疊'''
            # y=y+20*k
            y = y - 40 * (6 - k)
            # 讀取該行的圖片
            bitmap = np.fromfile(f, dtype='uint8', count=h * w)
            # bitmap_all = np.fromfile(f, dtype='uint8', count=height*2482)
            bitmap = np.array(bitmap).reshape(h, w)
            img_ori[y:y + h, x:x + w] = bitmap
            # bitmap_all = np.fromfile(f, dtype='uint8', count=height*2482)

            # 保存資訊
            '''for save txt'''
            txt_json = {
                "transcription": label,
                "points": [[x, y], [x + w, y], [x + w, y + h], [x, y + h]],
            }
            append_txt.append(txt_json)
            label_file = os.path.join(
                label_dir, base_name.replace('.dgrl', '_' + str(k) + '.txt'))
            with open(label_file, 'w', encoding='UTF-8') as f1:
                f1.write(label)
            bitmap_file = os.path.join(
                image_dir, base_name.replace('.dgrl', '_' + str(k) + '.jpg'))
            # cv.imwrite(bitmap_file, bitmap)

        '''for save txt'''
        bitmap_file_ori = os.path.join(
            image_dir, base_name.replace('.dgrl', '.jpg'))
        cv.imwrite(bitmap_file_ori, img_ori)
        train_txt.write(bitmap_file_ori.replace(image_dir+"\\", "") + "\t" + str(append_txt) + '\n')


if __name__ == '__main__':
    dgrl_path = r'D:\temp\HWDB2.0Test'
    dgrl_paths = Path(dgrl_path).iterdir()
    dgrl_paths = list(dgrl_paths)
    '''for save txt'''
    train_txt = open('test_label.txt', 'w', encoding='UTF-8')
    for dgrl_path in tqdm(dgrl_paths):
        read_from_dgrl(dgrl_path, train_txt)
    train_txt.close()
