import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import regionprops, label,moments
from skimage.morphology import binary_closing,binary_dilation,binary_erosion,binary_opening,skeletonize

def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0]+2,shape[1]+2))
    new_image[1:-1,1:-1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled) - 1

def cout_lr_vlines(region):
    x = region.image.mean(axis = 0) ==1
    return np.sum(x[:len(x)//2]) > np.sum(x[len(x)//2:])

def extractor(region):
    area = region.area / region.image.size
    cy,cx = region.centroid_local
    cy /= region.image.shape[0]
    cx /= region.image.shape[1]
    perimeter = region.perimeter / region.image.size
    eccen = region.eccentricity
    cnt_holes = count_holes(region)*2
    all_true = np.all(region.image).sum()
    vlines = cout_lr_vlines(region)
    ratio = (region.image.shape[0]/region.image.shape[1])
    convex = (region.area/region.convex_area)

              
    return np.array([area,cy,cx,perimeter,eccen,cnt_holes,all_true,vlines,ratio,convex])

def norm_l1(v1, v2):
    return ((v1 - v2) ** 2).sum() ** 0.5

def classificator(v, templates):
    result = "_"
    min_dist = 10 ** 16
    for key in templates:
        d = norm_l1(v, templates[key])
        if d < min_dist:
            result = key
            min_dist = d
    return result

alphabet = plt.imread("alphabet.png")[:, :, :-1]

gray = alphabet.mean(axis=2)
binary = gray > 0
labeled = label(binary)
regions = regionprops(labeled)
print(len(regions))

symbols = plt.imread("alphabet-small.png")[:, :, :-1]
gray = symbols.mean(axis=2)
binary = gray < 1
slabeled = label(binary)
sregions = regionprops(slabeled)
print(len(regions))

templates = {"A": extractor(sregions[2]),
            "B": extractor(sregions[3]),
            "8": extractor(sregions[0]),
            "0": extractor(sregions[1]),
            "1": extractor(sregions[4]),
            "W": extractor(sregions[5]),
            "X": extractor(sregions[6]),
            "*": extractor(sregions[7]),
            "-": extractor(sregions[9]),
            "/": extractor(sregions[8])}

# print(templates)
# for i,region in enumerate(sregions):
#     v = extractor(region)
#     plt.subplot(2,5,i+1)
#     plt.title(classificator(v,templates))
#     plt.imshow(region.image)
# plt.imshow(slabeled)
# plt.imshow(alphabet)
result = {}
for region in regions:
    v = extractor(region)
    symbol = classificator(v,templates)
    result[symbol] = result.get(symbol,0)+1
print(result)

plt.show()
