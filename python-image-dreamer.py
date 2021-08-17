from PIL import Image
from collections import defaultdict
from os.path import exists
import os
import random
#acc is used as the look radius (higher is more noisy)
acc = 2

def getImage(path,max):
    global sumw, sumh, ic
    img = Image.open(path,'r')
    img = img.convert('RGBA')
    img.thumbnail((max,max))
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
    print('looking at art...')
    px = img.load()
    grabBag = defaultdict(lambda: [])
    cachePath = 'pixels.txt'
    if not exists(cachePath):
        f = open(cachePath,'w')
        f.write('')
        f.close()
    for h in range(img.height):
        for w in range(img.width):
            sur = surround(w,h,acc,img.width,img.height)
            sur = posToRGB(img,sur)
            for rgb in sur:
                grabBag[rgb].append(px[w,h])
    return grabBag

def copyFrame(img1,img2,offset):
    px1 = img1.load()
    px2 = img2.load()
    pw = [offset,img2.width-1-offset]
    ph = [offset,img2.height-1-offset]
    for w in pw:
        for h in range(offset,img2.height-offset):
            px2[w,h] = px1[w,h]
    for h in ph:
        for w in range(offset,img2.width-offset):
            px2[w,h] = px1[w,h]
    return img2

def dream(out,grabBag):
    print('dreaming... zzz...')
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

def main(path,accuracy,max):
    img = getImage(path,max)
    gb = genGrabBag(img)
    output = Image.new(img.mode, (img.width,img.height))
    output = copyFrame(img,output,0)
    minAxis = min(output.width,output.height)
    minAxis2 = int(minAxis/2)
    for offset in range(0,minAxis2,int(minAxis2-minAxis2*accuracy)+1):
        output = copyFrame(img,output,offset)
    output = dream(output,gb)
    path = path[path.find('/'):]
    path = path[:-3] + 'png'
    output.save('output/' + path)
    print('saved: ' + path)
if __name__ == '__main__':
    pictures = os.listdir('input')
    mx = int(input('max file size (start low (250)): '))
    ac = int(input('Dream Accuracy (0-100)%: '))
    ac = min(max(1,ac),100)
    ac = ac/100
    for pic in pictures:
        main('input/'+pic,ac,mx)