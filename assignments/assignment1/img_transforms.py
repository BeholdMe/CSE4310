import numpy as np
import matplotlib.pyplot as plt
import imageio.v3 as iio

def random_crop(img, size):
    # get height and width
    # image must be cropped within range
    height, width = img.shape[:2]
    if size <= 0 or size > min(height, width):
        raise ValueError("Crop size not in range")
    
    #find the random center using randomint
    centerY = np.random.randint(size // 2, height - size // 2)
    centerX = np.random.randint(size // 2, width - size // 2)
    
    # crop by using random center
    y1 = centerY - size // 2
    y2 = centerY + size // 2
    x1 = centerX - size // 2
    x2 = centerX + size // 2

    # return cropped image
    return img[y1:y2, x1:x2]

def testDaCrop():
    img = iio.imread("C:\\Users\\RatuwinaBalaputradew\\Documents\\CSE4310\\assignments\\assignment1\\img\\random_crop.png")
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