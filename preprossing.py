import cv2
import glob
import os

inputpath = 'D:\\temp\\test\\CASIA_Filtered'
outputpath = 'D:\\temp\\test2\\CASIA_Filtered'


# defining a function for the task
def create_dirtree_without_files(src, dst):
    # getting the absolute path of the source
    # directory
    src = os.path.abspath(src)

    # making a variable having the index till which
    # src string has directory and a path separator
    src_prefix = len(src) + len(os.path.sep)

    # making the destination directory
    if not os.path.isdir(dst):
        os.makedirs(dst)

    input_dirpath_list = []
    # doing os walk in source directory
    for root, dirs, files in os.walk(src):
        for dirname in dirs:
            # here dst has destination directory,
            # root[src_prefix:] gives us relative
            # path from source directory
            # and dirname has folder names
            input_dirpath = os.path.join(src, root[src_prefix:], dirname)
            dirpath = os.path.join(dst, root[src_prefix:], dirname)
            input_dirpath_list.append(input_dirpath)
            # making the path which we made by
            # joining all of the above three
            if not os.path.isdir(dirpath):
                os.mkdir(dirpath)
    return input_dirpath_list


def img_write_path(str, str1, str2):
    new_str = str.replace(str1, str2)
    return new_str


def img_binarization(path):
    for i in path:
        #print(i.split('/')[-1])
        img = cv2.imread(i)
        h_img, w_img, c_img = img.shape
        gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gry, (3, 3), 0)
        th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # 注意路徑
        binary_write_path=img_write_path(i, "test", "test2")
        #print(binary_write_path)
        cv2.imwrite(binary_write_path, th)


if __name__ == '__main__':
    # calling the above function
    input_dirpath_list = create_dirtree_without_files(inputpath, outputpath)
    for dir_path in input_dirpath_list:
        print(dir_path)
        path = dir_path + "\\*.png"
        file_path_list = sorted(glob.glob(path))
        if len(file_path_list) == 0:
            continue
        # print(file_path_list)
        img_binarization(file_path_list)
