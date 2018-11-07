from PIL import Image

def binary(path):
    img = Image.open(path)
    # img = img.rotate(270)
    thresh = 160
    fn = lambda x : 0 if x > thresh else 255
    r = img.convert('L').point(fn, mode='1')
    r = r.rotate(270)
    r.save('2.jpg')


