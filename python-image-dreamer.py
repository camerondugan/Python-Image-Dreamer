import sqlite3
from PIL import Image
from collections import defaultdict
import random

db = sqlite3.connect('cache.db')
#sum and count height width of input
sumw,sumh = 0,0
#input count
ic = 0
#accuracy
acc = 2

def getImage(path):
    global sumw, sumh, ic
    img = Image.open(path,'r')
    img = img.convert('RGBA')
    sumw += img.width
    sumh += img.height
    ic += 1
    return img

def surround(x,y,r,maxX,maxY):
    sur = []
    for w in range(-r+1,r):
        for h in range(-r+1,r):
            cw,ch = x+w,y+h
            if (cw >= 0 and ch >= 0 and cw < maxX and ch < maxY):
                sur.append((cw,ch))
    return sur

def posToRGB(img,arr):
    px = img.load()
    tmp = []
    for x,y in arr:
        val = px[x,y]
        tmp.append(val)
    return tmp

def genGrabBag(img):
    print('genGB')
    px = img.load()
    grabBag = defaultdict(lambda: [])
    for h in range(img.height):
        for w in range(img.width):
            sur = surround(w,h,acc,img.width,img.height)
            sur = posToRGB(img,sur)
            for rgb in sur:
                grabBag[rgb].append(px[w,h])
    return grabBag

def copyFrame(img1,img2):
    print('cp frame')
    px1 = img1.load()
    px2 = img2.load()
    pw = [0,img1.width-1]
    ph = [0,img1.height-1]
    for w in pw:
        for h in range(img1.height):
            px2[w,h] = px1[w,h]
    for h in ph:
        for w in range(img1.width):
            px2[w,h] = px1[w,h]
    return img2

def dream(out,grabBag):
    print('dream')
    ox = out.load()
    for w in range(out.width):
        for h in range(out.height):
            sur = surround(w,h,acc,out.width,out.height)
            sur = posToRGB(out,sur)
            random.shuffle(sur)
            c = 0
            choices = []
            while len(choices)<1 and c < len(sur):
                choices = grabBag[sur[c]]
                if (len(choices)>0):
                    ox[w,h] = random.choice(choices)
                c += 1
    return out

def main():
    img = getImage('input/mtg.jpg')
    gb = genGrabBag(img)
    avgw,avgh = int(sumw/ic),int(sumh/ic)

    output = Image.new(img.mode, (avgw,avgh))
    output = copyFrame(img,output)
    output = dream(output,gb)
    output.save('output/yourimage.png')

if __name__ == '__main__':
    main()