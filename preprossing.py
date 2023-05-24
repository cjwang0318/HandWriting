import cv2
import glob
path=sorted(glob.glob("test_data/*.jpg"))
for i in path:
    print(i.split('/')[-1])
    img=cv2.imread(i)
    h_img, w_img, c_img = img.shape
    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gry,(3,3), 0)
    th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imwrite("test_data_binary/"+i.split('/')[-1],th)
