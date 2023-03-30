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


def gnt_convert(path, save_dir):
    gnt_paths = list(Path(path).iterdir())

    label_list = []
    for gnt_path in gnt_paths:
        count = 0
        print(gnt_path)
        with open(str(gnt_path), 'rb') as f:
            while f.read(1) != "":
                f.seek(-1, 1)
                count += 1
                try:
                    # 只所以新增try，是因為有時f.read會報錯 struct.error: unpack requires a buffer of 4 bytes
                    # 原因尚未找到
                    length_bytes = struct.unpack('<I', f.read(4))[0]

                    tag_code = f.read(2)

                    width = struct.unpack('<H', f.read(2))[0]

                    height = struct.unpack('<H', f.read(2))[0]

                    im = Image.new('RGB', (width, height))
                    img_array = im.load()
                    for x in range(height):
                        for y in range(width):
                            pixel = struct.unpack('<B', f.read(1))[0]
                            img_array[y, x] = (pixel, pixel, pixel)

                    filename = str(count) + '.png'
                    tag_code = tag_code.decode('gbk').strip('\x00')
                    save_path = f'{save_dir}/images/{gnt_path.stem}'
                    if not Path(save_path).exists():
                        Path(save_path).mkdir(parents=True, exist_ok=True)
                    im.save(f'{save_path}/{filename}')

                    label_list.append(f'{gnt_path.stem}/{filename}\t{tag_code}')
                except:
                    break

    write_txt(f'{save_dir}/gt.txt', label_list)

def read_from_dgrl(dgrl):
    if not os.path.exists(dgrl):
        print('DGRL not exis!')
        return

    dir_name, base_name = os.path.split(dgrl)
    label_dir = dir_name+'_label'
    image_dir = dir_name+'_images'
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    with open(dgrl, 'rb') as f:
        # 讀取表頭尺寸
        header_size = np.fromfile(f, dtype='uint8', count=4)
        header_size = sum([j << (i*8) for i, j in enumerate(header_size)])
        # print(header_size)

        # 讀取表頭剩下內容，提取 code_length
        header = np.fromfile(f, dtype='uint8', count=header_size-4)
        code_length = sum([j << (i*8) for i, j in enumerate(header[-4:-2])])
        # print(code_length)

        # 讀取圖像尺寸資訊，提取圖像中行數量
        image_record = np.fromfile(f, dtype='uint8', count=12)
        height = sum([j << (i*8) for i, j in enumerate(image_record[:4])])
        width = sum([j << (i*8) for i, j in enumerate(image_record[4:8])])
        line_num = sum([j << (i*8) for i, j in enumerate(image_record[8:])])
        print('圖像尺寸:')
        print(height, width, line_num)

        # 讀取每一行的資訊
        for k in range(line_num):
            print(k+1)

            # 讀取該行的字元數量
            char_num = np.fromfile(f, dtype='uint8', count=4)
            char_num = sum([j << (i*8) for i, j in enumerate(char_num)])
            print('字元數量:', char_num)

            # 讀取該行的標註資訊
            label = np.fromfile(f, dtype='uint8', count=code_length*char_num)
            label = [label[i] << (8*(i % code_length))
                     for i in range(code_length*char_num)]
            label = [sum(label[i*code_length:(i+1)*code_length])
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
            y = sum([j << (i*8) for i, j in enumerate(pos_size[:4])])
            x = sum([j << (i*8) for i, j in enumerate(pos_size[4:8])])
            h = sum([j << (i*8) for i, j in enumerate(pos_size[8:12])])
            w = sum([j << (i*8) for i, j in enumerate(pos_size[12:])])
            # print(x, y, w, h)

            # 讀取該行的圖片
            bitmap = np.fromfile(f, dtype='uint8', count=h*w)
            bitmap = np.array(bitmap).reshape(h, w)

            # 保存資訊
            label_file = os.path.join(
                label_dir, base_name.replace('.dgrl', '_'+str(k)+'.txt'))
            with open(label_file, 'w', encoding='UTF-8') as f1:
                f1.write(label)
            bitmap_file = os.path.join(
                image_dir, base_name.replace('.dgrl', '_'+str(k)+'.jpg'))
            cv.imwrite(bitmap_file, bitmap)

if __name__ == '__main__':
    # gne_path = './CASIA/gnt/Gnt1.0Train'  # 目錄下均為gnt檔案
    # save_dir = './output'
    # gne_path = r'D:\temp\Gnt1.2Test'  # 目錄下均為gnt檔案
    # save_dir = r'D:\temp\output'
    # gnt_convert(gne_path, save_dir)

    #dgrl_path='./CASIA/dgrl'
    dgrl_path = r'D:\temp\HWDB2.0Test'
    dgrl_paths = Path(dgrl_path).iterdir()
    dgrl_paths = list(dgrl_paths)
    for dgrl_path in tqdm(dgrl_paths):
        read_from_dgrl(dgrl_path)
