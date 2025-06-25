# Color Spaces
To use this, just run it. It will ask for certain inputs: image filename, hue shift value, saturation shift value, value shift value, and output file name. The inputs are command line inputs.

Make sure
- The image filename is **absolute pathname**
- Hue shift value is **between 0 and 360**
- Both saturation and value shift values is a float **betwen 0 and 1**.

It should be outputed in the same directory you're working on.

# Image Transformations
I have already written test cases for all of the image transformations. Just change the values in each of these test cases.

The image is hardcoded to be livbird.jpg (which is a square image of the Liverpool FC logo), but change the pathname to another image that you have and it should work.

The new image **must be square**. In other words, the image should have its width == height.

# Create Image Pyramids
The final line runs the function. Change it so that it uses an image that your computer can access, and change the second parameter to be the height you are looking for.

You can also run the `createImagePyramid(img, height)` function with a filename as its first parameter and the height as the second. The height **CANNOT** be less than 1.

WHen it is done, you'll likely have new images based on the "height" you set out. The images will have the same file extension as the original image.