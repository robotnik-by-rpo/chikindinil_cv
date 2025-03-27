import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label;

stars = np.load("stars.npy")
cnt = 0

def star_plus(stars,x,y):
    flag = False
    if (stars[y-1,x] and stars[y-2,x] and stars[y,x-1] and stars[y,x-2] and stars[y,x+1] and stars[y,x+2] and stars[y+1,x] and stars[y+2,x] and stars[y,x])==1 :
        flag = True
    return flag

def star_cross(stars,x,y):
    flag = False
    if (stars[y+1,x-1] and stars[y+2,x-2] and stars[y-1,x-1] and stars[y-2,x-2] and stars[y-1,x+1] and stars[y-2,x+2] and stars[y+1,x+1] and stars[y+2,x+2] and stars[y,x])==1:
        flag = True

    return flag

for y in range(0,stars.shape[0]):
    for x in range(0,stars.shape[1]):
        if stars[y,x] == 1:
            if(star_cross(stars,x,y) == True):
                cnt +=1
            elif star_plus(stars,x,y) == True:
                cnt +=1
             
print(cnt)
plt.figure()
plt.imshow(stars)
plt.show()