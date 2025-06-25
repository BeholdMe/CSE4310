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
    saturation = value - np.min(img, axis=2)

    # Get the Hue with piecewise func
    # if c == 0 -> h1 = 0
    hue = np.zeros_like(saturation)
    # if v == r -> h1 = ((g - b) / c) % 6
    i = (value == r) & (saturation != 0)
    hue[i] = ((g[i] - b[i]) / saturation[i] % 6)
    # if v == g -> h1 = ((b - r) / c) + 2
    i = (value == g) & (saturation != 0)
    hue[i] = ((b[i] - r[i]) / saturation[i] + 2)
    # if v == b -> h1 = ((r - g) / c) + 4
    i = (value == b) & (saturation != 0)
    hue[i] = ((r[i] - g[i]) / saturation[i] + 4)

    hue = 60 * hue
    hue[hue < 0] += 360
    hsv = np.stack((hue, saturation,value), axis=-1)
    return hsv


def hsvToRgb(hsv):
    h,s,v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    # get chroma
    c = v * s
    # get h'
    # should be in [0,6)
    h1 = h / 60.0

    # Get intermediate value x
    # X = C \times (1 - \space |H' \space mod \space 2 - 1)
    x = c * (1 - np.abs((h1 % 2) - 1))
    zeros = np.zeros_like(h)
    r1 = np.zeros_like(h)
    g1 = np.zeros_like(h)
    b1 = np.zeros_like(h)

    # set initial RGB (r1, g1, b1) based on h1 sector
    # use piecewise function
    #r1, g1, b1 = 0,0,0
    #    if h1 >= 0 and h1 < 1:
    #        r1,g1,b1 = c,x,0
    #    elif h1 >= 1 and h1 < 2:
    #        r1,g1,b1 = x,c,0
    #    elif h1 >= 2 and h1 < 3:
    #        r1,g1,b1 = 0,c,x
    #    elif h1 >= 3 and h1 < 4:
    #        r1,g1,b1 = 0,x,c
    #    elif h1 >= 4 and h1 < 5:
    #        r1,g1,b1 = x,0,c
    #    elif h1 >= 5 and h1 < 6:
    #        r1,g1,b1 = c,0,x

    # sector 1
    i = (h1 >= 1) & (h1 < 2)
    r1[i], g1[i], b1[i] = x[i], c[i], zeros[i]
    
    # sector 2
    i = (h1 >= 2) & (h1 < 3)
    r1[i], g1[i], b1[i] = zeros[i], c[i], x[i]
    
    #sector 3
    i = (h1 >= 3) & (h1 < 4)
    r1[i], g1[i], b1[i] = zeros[i], x[i], c[i]

    # sector 4
    i = (h1 >= 4) & (h1 < 5)
    r1[i], g1[i], b1[i] = x[i], zeros[i], c[i]
    
    #sector 5
    i = (h1 >= 5) & (h1 < 6)
    r1[i], g1[i], b1[i] = c[i], zeros[i], x[i]

    #add m to match brightness
    m = v - c
    r, g, b = r1 + m, g1 + m, b1 + m

    rgb = np.stack((r,g,b), axis=-1)
    return rgb



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
    satMod = float(input().strip())
    print("Enter value mod: ")
    valMod = float(input().strip())
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
    hsv[..., 0] = (hsv[..., 0] + hueMod) % 360
    hsv[..., 1] = np.clip(hsv[...,1] + satMod, 0, 1)
    hsv[..., 2] = np.clip(hsv[...,2] + valMod, 0, 1)
    modRGB = hsvToRgb(hsv)

    #Ask for output file name and save the modified rgb in said fiel
    print("What da name for da file brah: ")
    outputFile = input().strip()
    try:
        np.save(outputFile, modRGB)
        print(f"Saved to {outputFile}")
    except Exception as e:
        print(f"Error saving image: {e}")

if __name__ == "__main__":
    test()
