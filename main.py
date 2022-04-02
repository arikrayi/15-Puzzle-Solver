import numpy as np
import heapq as hq
import time

class Node:
    def __init__(self, level, cost, matrix, emptyTile, parent):
        self.cost = cost
        self.level = level
        self.matrix = matrix
        self.emptyTile = emptyTile
        self.parent = parent

    def __lt__(self, other):
        return self.cost <= other.cost

def changeToZero(matrix):
    matrixZero = matrix.copy()
    matrixZero.resize(4,4)
    for r in range(0,4):
        for c in range(0,4):
            if matrixZero[r,c] == 16:
                matrixZero[r,c] = 0
    return matrixZero

def fungsiKurang(matrix):
    kurang = 0;
    for i in range(1,17):
        x = 0;
        while (matrix[x] != i):
            x += 1;
        for j in range(x,16):
            if matrix[j] < i:
                kurang += 1
    for r in range(0,4):
        for c in range(0,4):
            if matrix[(r*4)+c] == 16:
                if (r + c) % 2 != 0:
                    kurang += 1
    return kurang

def fungsiCost(parentCost, r, c, element, r1, c1):
    if ((r*4) + c + 1 == element):
        return parentCost
    elif ((r1*4) + c1 + 1 == element):
        return parentCost + 2
    else:
        return parentCost + 1

def move(parent,r,c,r2,c2):
    tempMatrix = list(parent.matrix)
    tempMatrix[(r*4)+c] = tempMatrix[(r2*4)+c2]
    tempMatrix[(r2*4)+c2] = 16
    return tuple(tempMatrix)

def cariKemungkinan(prioQueue, visited):
    nodes = 1
    while (True):
        parent = hq.heappop(prioQueue)
        visited.add(parent.matrix)
        r = parent.emptyTile[0]
        c = parent.emptyTile[1]
        if (r != 0):
            tempMatrix = move(parent,r,c,r-1,c)
            if (tempMatrix not in visited):
                nodes += 1
                cost = fungsiCost(parent.cost,r,c,tempMatrix[(r*4)+c],r-1,c)
                tempNode = Node(parent.level+1, cost, tempMatrix, [r-1,c], parent)
                hq.heappush(prioQueue,tempNode)
                visited.add(tempMatrix)
                if (cost == parent.level+1):
                    return [tempNode, nodes]
        if (c != 0):
            tempMatrix = move(parent,r,c,r,c-1)
            if (tempMatrix not in visited):
                nodes += 1
                cost = fungsiCost(parent.cost,r,c,tempMatrix[(r*4)+c],r,c-1)
                tempNode = Node(parent.level+1, cost, tempMatrix, [r,c-1], parent)
                hq.heappush(prioQueue,tempNode)
                visited.add(tempMatrix)
                if (cost == parent.level+1):
                    return [tempNode, nodes]
        if (c != 3):
            tempMatrix = move(parent,r,c,r,c+1)
            if (tempMatrix not in visited):
                nodes += 1
                cost = fungsiCost(parent.cost,r,c,tempMatrix[(r*4)+c],r,c+1)
                tempNode = Node(parent.level+1, cost, tempMatrix, [r,c+1], parent)
                hq.heappush(prioQueue, tempNode)
                visited.add(tempMatrix)
                if (cost == parent.level+1):
                    return [tempNode, nodes]
        if (r != 3):
            tempMatrix = move(parent,r,c,r+1,c)
            if (tempMatrix not in visited):
                nodes += 1
                cost = fungsiCost(parent.cost,r,c,tempMatrix[(r*4)+c],r+1,c)
                tempNode = Node(parent.level+1, cost, tempMatrix, [r+1,c], parent)
                hq.heappush(prioQueue, tempNode)
                visited.add(tempMatrix)
                if (cost == parent.level+1):
                    return [tempNode, nodes]


if __name__ == "__main__":
    prioQueue = []
    visited  = set()
    cost = 0
    r = 0
    c = 0

    test = tuple([])
    matrix1 = tuple([1,2,3,4,5,6,16,8,9,10,7,11,13,14,15,12])
    matrix2 = tuple([1,2,5,4,3,6,16,7,9,10,8,11,13,14,15,12])
    matrix3 = tuple([1,2,3,4,5,7,10,8,11,9,6,16,13,14,15,12])
    matrix4 = tuple([3,1,5,6,7,8,10,9,11,4,2,16,13,15,14,12])
    matrix5 = tuple([1,3,5,7,9,11,13,15,16,2,4,6,8,10,12,14])

    input = input("Masukkan nomor matrix: ")
    if input == "1":
        test = matrix1
    elif input == "2":
        test = matrix2
    elif input == "3":
        test = matrix3
    elif input == "4":
        test = matrix4
    elif input == "5":
        test = matrix5
    else:
        print("Input salah")
        exit()

    tAwal = time.time()
    for i in range(0,16):
        if test[i] == 16:
            r = i // 4
            c = i % 4
            break

    for i in range(0,16):
        if test[i] != 16 and test[i] != i+1:
            cost += 1

    if fungsiKurang(test) % 2 == 0:
        hq.heappush(prioQueue,(Node(0, cost, test, [r,c], None)))
        end = cariKemungkinan(prioQueue, visited)
        tAkhir = time.time()
        pathway = []
        paths = end[0].level
        print("Jalur terpendek pada puzzle ini adalah:")
        while (end[0] != None):
            pathway.append(changeToZero(np.matrix(end[0].matrix)))
            end[0] = end[0].parent
        for i in range(len(pathway)-1, -1, -1):
            print(pathway[i], "\n")
        print("Nilai kurang:", fungsiKurang(test))
        print("Jumlah jalur terpendek:", paths)
        print("Waktu:", tAkhir - tAwal, "detik")
        print("Simpul:", end[1])
    else:
        print("Nilai kurang:", fungsiKurang(test))
        print("Cannot be solved")