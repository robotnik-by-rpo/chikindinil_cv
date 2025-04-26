import socket
import numpy as np
from skimage.measure import  regionprops, label
from skimage.morphology import *
import matplotlib.pyplot as plt

host = "84.237.21.36"
port = 5152

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat = b"nope"

    plt.ion()
    plt.figure()

    while beat != b"yep":

        sock.send(b"get")
        bts = recvall(sock, 40002)

        image = np.frombuffer(bts[2:40002],dtype = "uint8").reshape(bts[0],bts[1])
        image = image > 140
    
        labeled = label(image)
        regions = regionprops(labeled)
        if len(regions) < 2:
            result = 0
        else:
            cy_1,cx_1=regions[0].centroid
            cy_2,cx_2 = regions[1].centroid
            result = ((cy_1-cy_2)**2 + (cx_1 - cx_2)**2)**0.5
        print(result)
        sock.send(f"{round(result,1)}".encode())
        print(sock.recv(10))
        plt.clf()
       
        plt.imshow(labeled)
        plt.pause(1)

        sock.send(b"beat")
        beat = sock.recv(10)