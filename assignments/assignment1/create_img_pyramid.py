import numpy as np
from PIL import Image
import os

def createImagePyramid(img, height):
    # make sure height is 1+
    if height < 1:
        raise ValueError("Height of pyramid should be 1+")
    
    #opens the image using the path given by input, then set the OG height and width
    image = Image.open(img)
    ogWidth, ogHeight = image.size

    #get the root and .jpg/png/etc. from the image path filnemae
    root, ext = os.path.splitext(img)

    pyramidImages = []

    # create resized imagas in powers of 2 until "height"
    for i in range(1, height):
        scale = 2 ** i
        newWidth = max(1, ogWidth // scale)
        newHeight = max(1, ogHeight // scale)

        # resize using PIL bc mine sucky sucky
        resized = image.resize((newWidth, newHeight), Image.NEAREST)
        output = f"{root}_{scale}x{ext}"

        #append the resized image onto the array
        resized.save(output)
        pyramidImages.append(resized)
        print(f"Saved as {output}")

    return pyramidImages

createImagePyramid("img\\livbird.jpg", 4)