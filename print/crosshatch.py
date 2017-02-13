import numpy as np
import cv2

def drawDiagonalUp(dim, spacing):
    image = np.zeros((dim,dim,3))
    l = []
    for i in range(spacing,dim * 2,spacing):
        x_start = max(0, i - dim)
        y_start = min(i,dim -1)
        x_end = min(i,dim -1)
        y_end = max(0, i - dim)
        cv2.line(image,(x_start, y_start),(x_end, y_end),(0,255,0))
        l.append((x_start, y_start, x_end, y_end))
    return image, l
    
    
def drawDiagonalDown(dim, spacing):
    image = np.zeros((dim,dim,3))
    l = []
    for i in range((dim * -1) + spacing,dim,spacing):
        x_start = max(0, -1 * i)
        y_start = max(0, i)
        x_end = min(dim - i,dim)
        y_end = min(dim, dim + i)
        cv2.line(image,(x_start, y_start),(x_end, y_end),(0,255,0))
        l.append((x_start, y_start, x_end, y_end))
    return image, l

def drawUp(dim, spacing):
    image = np.zeros((dim,dim,3))
    l = []
    for i in range(spacing,dim,spacing):
        x_start = i
        y_start = 0
        x_end = i
        y_end = dim
        cv2.line(image,(x_start, y_start),(x_end, y_end),(0,255,0))
        l.append((x_start, y_start, x_end, y_end))
    return image, l
    
def drawRight(dim, spacing):
    image = np.zeros((dim,dim,3))
    l = []
    for i in range(spacing,dim,spacing):
        x_start = 0
        y_start = i
        x_end = dim
        y_end = i
        cv2.line(image,(x_start, y_start),(x_end, y_end),(0,255,0))
        l.append((x_start, y_start, x_end, y_end))
    return image, l
    
def getVectorsDiag(vectors, im):
    masked_list = []
    for v in vectors:
        state = False
        current = []
        prev = [[0,0]]
        for x in range(v[0],v[2]):
            y = v[2]+v[0]-x if v[3] - v[1] < 0 else x + (v[1] - v[0])
            if any(im[y][x]) != state:
                if state == False:
                    current = [[x,y]]
                else:
                    masked_list.append(np.array([current,prev], dtype=np.int32))
                state = not(state)
            #if last iteration and still True
            if x == v[2]-1 and state == True:
                masked_list.append(np.array([current,prev], dtype=np.int32))
            prev = [[x,y]]
    return masked_list

def getVectorsOrth(vectors, im):
    masked_list = []
    for v in vectors:
        state = False
        current = []
        prev = [[0,0]]
        for i in range(max(v)):
            x = i
            y = i
            if v[0] == 0:
                x = v[1]
            else: 
                y = v[0]
            if any(im[x][y]) != state:
                if state == False:
                    current = [[y,x]]
                else:
                    masked_list.append(np.array([current,prev], dtype=np.int32))
                state = not(state)
            if i == max(v)-1 and state == True:
                masked_list.append(np.array([current,prev], dtype=np.int32))
            prev = [[y,x]]
    return masked_list
   