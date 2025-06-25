import numpy as np
import matplotlib.pyplot as plt
import imageio.v3 as iio
import color_space_test as cst

def random_crop(img, size):
    # get height and width
    # image must be cropped within range
    height, width = img.shape[:2]
    if size <= 0 or size > min(height, width):
        raise ValueError("Crop size not in range")
    
    #find the random center using randomint
    centerY = np.random.randint(sizht - size // 2)
    centerX = np.random.randint(size // 2, width - size // 2)
    
    # crop by using random center
    y1 = centerY - size // 2
    y2 = centerY + size // 2
    x1 = centerX - size // 2
    x2 = centerX + size // 2

    # return cropped image
    return img[y1:y2, x1:x2]

def extract_patch(img, num_patches):
    # get h (height) and w (width)
    h, w = img.shape[:2]
    
    # n to be the square root of num patches
    n = int(np.sqrt(num_patches))

    patchSize = h // n
    patches = []

    # go through image and crop patches one by one
    for i in range(0, h, patchSize):
        for j in range(0, w, patchSize):
            patches.append(img[i:i + patchSize, j:j + patchSize])
            if len(patches) == num_patches:
                return np.array(patches)
            
    # just in case
    return np.array(patches)

def resize_img(img, factor):
    # Resize with nearest neighbor interpolation
    if factor <= 0:
        raise ValueError("Scale factor need be more than 0")
    
    #find the hight and width and add factor to it
    height, width = img.shape[:2]
    newHeight = int(height * factor)
    newWidth = int(width * factor)

    # initialize the resized image
    resizedImg = np.zeros((newHeight, newWidth, img.shape[2]), dtype=img.dtype)

    # Use nearest neighbor to map unfilled pixels in resized image
    for i in range(newHeight):
        for j in range(newWidth):
            # find which of the OG pixel to be mapped from
            ogI = min(int(i / factor), height - 1)
            ogJ = min(int(j / factor), width - 1)
            # set pixel in new image using chosen OG pixel
            resizedImg[i, j] = img[ogI, ogJ]

    return resizedImg

def color_jitter(img, hue, saturation, value):
    #Randomly change hsv values on input image
    
    #Amount <= given value
    if not(0 <= hue <= 360):
        raise ValueError("Hue must be in [0, 360]")
    elif not(0 <= saturation <= 1):
        raise ValueError("Saturation must be in [0, 1]")
    elif not(0 <= value <= 1):
        raise ValueError("Value must be in [0, 1]")
    
    # randomize up to inputs
    hueMod = np.random.uniform(-hue, hue)
    saturationMod = np.random.uniform(-saturation, saturation)
    valueMod = np.random.uniform(-value, value)

    hsv = cst.rgbToHsv(img)
    # copypasted from color_to_space test
    hsv[..., 0] = (hsv[..., 0] + hueMod) % 360
    hsv[..., 1] = np.clip(hsv[...,1] + saturationMod, 0, 1)
    hsv[..., 2] = np.clip(hsv[...,2] + valueMod, 0, 1)
    return cst.hsvToRgb(hsv)

# Test functions
# Not necessary but helps me visualize if any errors
def testDaCrop():
    img = iio.imread("C:\\Users\\RatuwinaBalaputradew\\Documents\\CSE4310\\assignments\\assignment1\\img\\livbird.jpg")
    cropped = random_crop(img, 128)

    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(img)
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Cropped")
    plt.imshow(cropped)
    plt.axis("off")

    plt.show()

def testDaPatching():
    img = iio.imread("C:\\Users\\RatuwinaBalaputradew\\Documents\\CSE4310\\assignments\\assignment1\\img\\livbird.jpg")
    
    patches = extract_patch(img, 64)
    # plt.figure(figsize=(8,8))
    idx = 0
    for i in range(8):
        for j in range(8):
            plt.subplot(8, 8, idx + 1)
            plt.imshow(patches[idx], cmap='gray')
            plt.title(f"Patch {idx + 1}")
            plt.axis("off")
            idx += 1
    plt.tight_layout()
    plt.show()

def testDaResize():
    img = iio.imread("C:\\Users\\RatuwinaBalaputradew\\Documents\\CSE4310\\assignments\\assignment1\\img\\livbird.jpg")
    resized = resize_img(img, 3)

    plt.figure(figsize=(3,3))
    plt.title("Original")
    plt.imshow(img)
    plt.axis("off")

    plt.figure(figsize=(9,9))
    plt.title("Resized with factor of 3")
    plt.imshow(resized)
    plt.axis("off")

    plt.show()

def testColorJitter():
    img = iio.imread("C:\\Users\\RatuwinaBalaputradew\\Documents\\CSE4310\\assignments\\assignment1\\img\\livbird.jpg")
    colorJit = color_jitter(img, 100, 0.5, 0.5)

    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(img)
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Color Jittered")
    plt.imshow(colorJit)
    plt.axis("off")

    plt.show()

if __name__ == "__main__":
    testDaCrop()
    testDaPatching()
    testDaResize()
    testColorJitter()