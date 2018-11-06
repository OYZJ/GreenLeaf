from PIL import Image
import cv2

def binary(path):
    pic_resize(path)
    img = Image.open('2018-09-10-1.jpg')
    thresh = 160
    fn = lambda x : 0 if x > thresh else 255
    r = img.convert('L').point(fn, mode='1')
    r.save('2.jpg')

def pic_resize(path):
    """
    resize the picture
    :return:
    """
    pic = cv2.imread(path)
    pic = cv2.resize(pic, (480, 480), interpolation=cv2.INTER_CUBIC)
    # cv2.imshow('', pic)
    cv2.imwrite('2018-09-10-1.jpg', pic)
