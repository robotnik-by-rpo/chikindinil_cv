
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops, label
from skimage.morphology import *
from skimage.transform import resize

cnt_all_pencil = 0
for i in range(1,13):
    cnt_pencil = 0
    image_plt = plt.imread(f"img ({i}).jpg")
    image_plt = image_plt.mean(axis = 2)
    gray_image = resize(image_plt,(1100,1100))
    binary_image = gray_image < 135
    binary_image = binary_closing(binary_image, np.ones((25,25)))
    labeled = label(binary_image)[50:1050,50:1050]
    regions = regionprops(labeled)
    for r in regions:
        if r.eccentricity > 0.99:
            cnt_pencil += 1
            cnt_all_pencil += 1
    print(f"Quantity pencils on image {i} = {cnt_pencil}")
print(f"All quantity pencils on images = {cnt_all_pencil}")
   
