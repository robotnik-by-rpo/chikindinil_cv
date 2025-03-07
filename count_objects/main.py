import numpy as np
import matplotlib.pyplot as plt


external = np.diag([1, 1, 1, 1]).reshape(4, 2, 2)

internal = np.logical_not(external)

cross = np.array([[[1, 0], [0, 1]], [[0, 1], [1, 0]]])


def match(a, masks):
     for mask in masks:
        if np.all(a == mask):
            return True
     return False


def count_objects(image):
    E = 0
    for y in range(0, image.shape[0] - 1):
         for x in range(0, image.shape[1] - 1):
            sub = image[y : y + 2, x : x + 2]
            if match(sub, external):
                 E += 1
            elif match(sub, internal):
                 E -= 1
            elif match(sub, cross):
                 E += 2
    return E / 4


image = np.load("example1.npy")
image[image > 0] = 1
print("Number of figures in the first picture:",count_objects(image))

image3d = np.load("example2.npy")
sum3d = 0
image3d[image3d > 0] = 1
for i in range(image3d.shape[-1]):
    sum3d += count_objects(image3d[:,:,i])
print("Number of figures in the second picture:",sum3d)


