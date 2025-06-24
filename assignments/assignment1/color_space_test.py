import numpy as np
import imageio.v3 as iio
import sys

def rgbToHsv(img):
    # Step 1 - Normalize to [0,1]
    img = img.astype('float32') / 255.0
    r, g, b = img[..., 0], img[..., 1], img[..., 2]

    # Calculate the Value
    value = np.max(img, axis=2)
    
    # Calculate teh Saturation
    saturation = value - np.mn(img, axis=2)

    h1 = 0
    # Get the Hue with piecewise func
    # h' is h1
    # if c == 0 -> h1 = 0
    # if v == r -> h1 = ((g - b) / c) % 6
    # if v == g -> h1 = ((b - r) / c) + 2
    # if v == b -> h1 = ((r - g) / c) + 4
    if saturation == 0:
        h1 = 0
    elif value == r:
        h1 = ((g - b) / c) % 6
    elif value == g:
        h1 = ((b - r) / c) + 2
    elif value == b:
        h1 = ((r - g) / c) + 4

    hue = 60 * h1

    hsv = np.stack[hue,saturation,value]
    return hsv

def hsvToRgb(hsv):
    h,s,v = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    # check if grey (no hue)
    if s == 0:
        r = v
        g = v
        b = v
        rgb = np.stack[r,g,b]
        return rgb
    else:
        # get chroma
        c = np.dot(v, s)

        # get h'
        # should be in [0,6)
        h1 = h / 60.0

        # compute intermediate value x
        x = c * (1 - np.abs((h1 % 2) - 1))

        # set initial RGB (r1, g1, b1) based on h1 sector
        r1, g1, b1 = 0,0,0
        if h1 >= 0 and h1 < 1:
            r1,g1,b1 = c,x,0
        elif h1 >= 1 and h1 < 2:
            r1,g1,b1 = x,c,0
        elif h1 >= 2 and h1 < 3:
            r1,g1,b1 = 0,c,x
        elif h1 >= 3 and h1 < 4:
            r1,g1,b1 = 0,x,c
        elif h1 >= 4 and h1 < 5:
            r1,g1,b1 = x,0,c
        elif h1 >= 5 and h1 < 6:
            r1,g1,b1 = c,0,x
        
        #add m to match brightness
        m = v - c

        r,g,b = r1 + m, g1 + m, b1 + m
        return r,g,b

def test():
    # Ask for input for filename
    # Make sure file can be read using iio
    print("Enter filename of image: ")
    filename = input().strip()
    try:
        img = iio.imread(filename)
    except Exception as e:
        print(f"Error loading image: {e}")
        sys.exit(1)
    
    # ask for modification values for hue, saturation, and value
    print("Enter hue mod [0, 360]: ")
    hueMod = float(input().strip())
    print("Enter saturation mod: ")
    satMod = float(input.strip())
    print("Enter value mod: ")
    valMod = float(input.strip())
    # Make sure mod values fit within range
    # Hue in [0, 360]
    # Sat and Val in [0, 1]
    if(hueMod < 0 or hueMod > 360):
        print("Enter hue mod within [0, 360]")
        sys.exit(1)
    if(satMod < 0 or satMod > 1):
        print("Enter saturation mod within [0, 1]")
        sys.exit(1)
    if(valMod < 0 or valMod > 1):
        print("Enter value mod within [0, 1]")
        sys.exit(1)

    # convert to hsv and change hue/sat/val with mods
    hsv = rgbToHsv(img)