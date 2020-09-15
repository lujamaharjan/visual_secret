from PIL import Image
from numpy import *
import math

# global variables
list_of_cofficient = [3, 5, 7, 11, 13, 17, 19, 23]


# change image to matrix
def changeImageToMatrix(imagename):
    img = Image.open(imagename)  # opens image
    image_as_array = array(img)  # converts into numpy array
    return image_as_array


# Encryption
def encryption(total_Shares, threshold, pixel):
    epixels = list()  # for storing encrypted images

    for i in range(total_Shares):
        temp = pixel
        for j in range(1, threshold):
            temp = temp + list_of_cofficient[j - 1] * int(math.pow(i + 1, j))

        epixels.append(temp % 256)
    return epixels


# Decryption
def decryption(epixel, threshold):
    dpixel = 0
    for i in range(1, threshold + 1):
        li = 1
        for j in range(1, threshold + 1):
            if i != j:
                li = li * (-j / (i - j))
        dpixel = dpixel + epixel[i - 1] * li
    return dpixel


def imageEncryption(total_Shares, threshold, image):
    image = changeImageToMatrix(image)
    image = list(image)
    encrypted_images = list()
    for b in range(total_Shares):
        encrypted_images.append(image)
    encrypted_images = array(encrypted_images)
    # for encrypting the image and store all shares in one list
    for i in range(len(image)):
        for j in range(len(image[i])):
            for k in range(len(image[i][j])):
                encrypt = encryption(total_Shares, threshold, image[i][j][k])
                for b in range(total_Shares):
                    encrypted_images[b][i][j][k] = encrypt[b]
    return array(encrypted_images)


def imageDecryption(images, threshold):
    decrypted_image = array(images[0])
    sample = list(images[0])
    for i in range(len(sample)):
        for j in range(len(sample[i])):
            for k in range(len(sample[i][j])):
                row = []
                for b in range(threshold):
                    row.append(images[b][i][j][k])
                colorpixel = decryption(row, threshold)
            decrypted_image[i][j][k] = colorpixel
    print(decrypted_image)
    Image.fromarray(decrypted_image, 'RGB').show()
