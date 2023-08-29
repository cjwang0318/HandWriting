import cv2
import os
import numpy as np
from htr_pipeline import read_page, DetectorConfig, LineClusteringConfig



filepath = "./img/1.jpg"
basename = os.path.basename(filepath)  # example.py
filename = os.path.splitext(basename)[0]  # example

# read image
img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(filepath)
img3 = img2.copy()

# read image shape
height, width = img2.shape[:2]  # image height and width
print(f"image height={height}")

# calculate scale value
scaleValue = 1.24
scaleValue=1
print(f"scaleValue={scaleValue}")

# detect and read text
read_lines = read_page(img, DetectorConfig(scale=scaleValue, margin=5),
                       line_clustering_config=LineClusteringConfig(min_words_per_line=1))

# output text
# for read_line in read_lines:
#     print(' '.join(read_word.text for read_word in read_line))

# print(read_lines)
font = cv2.FONT_HERSHEY_SIMPLEX
for i, read_line in enumerate(read_lines):
    j=0
    print("Number of BBX=" + str(len(read_line)))
    for read_word in read_line:
        aabb = read_word.aabb
        cv2.rectangle(img2, (aabb.xmin, aabb.ymin), (aabb.xmax, aabb.ymax), (0, 255, 0), 4)
        img4 = img3[aabb.ymin:aabb.ymax, aabb.xmin:aabb.xmax]
        cv2.imwrite(f'./img/crop_img/{filename}_{j}.jpg', img4)
        j+=1
        line_detection(img4)
        #text = read_word.text
        #print(f"BBX_{j} Texe={text}")
    # cv2.putText(img2, text, (aabb.xmax, aabb.ymin), font, 1, (255, 0, 0), 1)

cv2.imwrite('./BBX_result.jpg', img2)