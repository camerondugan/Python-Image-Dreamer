from PIL import Image
from collections import defaultdict
from os.path import exists
import random


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


def getFromCache(cachePath,rgb):
    cache = open(cachePath,'r')
    curVal = None
    adj = None
    index = 0
    for line in cache:
        if (line.__contains__(str(rgb))):
            curVal = line
            break
        index += 1
    cache.close()
    if (curVal != None):
        curVal = curVal[:-1]
        adj = curVal.split(':')[1].split('_')
    else:
        adj = []
    return [index,adj]

def addToCache(cachePath,rgb,adj):
    cache = open(cachePath,'a')
    cur = getFromCache(cachePath,rgb)
    print(cur[1])
    # if (not str(cur[1]).__contains__(str(adj))):
        # data=str(cur[1])[1:-1] + str(adj)
    data= cur[1].append(str(adj) + '_')
    cache.write(f'{rgb}:{data}\n')

def genGrabBag(img):
    print('genGB')
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
                addToCache(cachePath,rgb,px[w,h])
                #grabBag[rgb].append(px[w,h])
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
    img = getImage('input/yourimage.png')
    gb = genGrabBag(img)
    avgw,avgh = int(sumw/ic),int(sumh/ic)

    output = Image.new(img.mode, (avgw,avgh))
    output = copyFrame(img,output)
    #output = dream(output,gb)
    output.save('output/yourimage.png')

if __name__ == '__main__':
    main()