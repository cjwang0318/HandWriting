import cv2
from htr_pipeline import read_page, DetectorConfig, LineClusteringConfig

img='./img/4.jpg'

# read image
img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(img)

# read image shape
height, width = img2.shape[:2]  # image height and width

# calculate scale value


# detect and read text
read_lines = read_page(img, DetectorConfig(scale=1.76, margin=5),
                       line_clustering_config=LineClusteringConfig(min_words_per_line=1))

# output text
# for read_line in read_lines:
#     print(' '.join(read_word.text for read_word in read_line))

# print(read_lines)
font = cv2.FONT_HERSHEY_SIMPLEX
for i, read_line in enumerate(read_lines):
    for read_word in read_line:
        print("Number of BBX=" + len(read_line))
        aabb = read_word.aabb
        cv2.rectangle(img2, (aabb.xmin, aabb.ymin), (aabb.xmax, aabb.ymax), (0, 255, 0), 4)
        # text = read_word.text
		# cv2.putText(img2, text, (aabb.xmax, aabb.ymin), font, 1, (255, 0, 0), 1)

img2 = img[aabb.ymin:aabb.ymax, aabb.xmin:aabb.xmax]
cv2.imwrite('./test.jpg', img2)
