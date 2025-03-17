import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from skimage.morphology import (binary_erosion,binary_closing,binary_opening,binary_dilation)

for num_pic in range(1,7): 
  data = np.load(f"wires{num_pic}npy.txt")
  labeled = label(data)
  cnt_pr = np.max(labeled) #Считаем кол-во объектов
  result = binary_erosion(data,np.ones(3).reshape(3,1))
  res = label(result)
  break_pr = np.max(res)
  if cnt_pr < break_pr:
    print("Some wire is broken")
    for i in range(1,cnt_pr+1):
      mask = labeled==i
      pr_er = binary_erosion(mask)
      cnt_pr_br = np.max(label(pr_er))
      if cnt_pr_br == 1:
        print(f"Wires {i} from {num_pic} image don't have pieces")
      else:
        print(f"Wires {i} from {num_pic} image have {cnt_pr_br} pieces")
  else:
    print(f"No wires is broken on {num_pic} image")