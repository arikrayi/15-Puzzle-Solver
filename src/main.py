import numpy as np
import heapq as hq
import time

# Class untuk menyimpan tiap simpul
class Node:
    def __init__(self, level, cost, buffer, emptyTile, parent):
        self.cost = cost
        self.level = level
        self.buffer = buffer
        self.emptyTile = emptyTile
        self.parent = parent

    def __lt__(self, other):
        return self.cost <= other.cost

# Fungsi pengubahan hasil ke bentuk matrix
def changeToZero(buffer):
    matrixZero = buffer.copy()
    matrixZero.resize(4,4)
    for r in range(0,4):
        for c in range(0,4):
            if matrixZero[r,c] == 16:
                matrixZero[r,c] = 0
    return matrixZero

# Fungsi pencarian nilai kurang
def fungsiKurang(buffer):
    kurang = 0;
    for i in range(1,17):
        x = 0;
        while (buffer[x] != i):
            x += 1;
        for j in range(x,16):
            if buffer[j] < i:
                kurang += 1
    for r in range(0,4):
        for c in range(0,4):
            if buffer[(r*4)+c] == 16:
                if (r + c) % 2 != 0:
                    kurang += 1
    return kurang

# Fungsi menghitung cost dari pergerakan dan cost parent
def fungsiCost(parentCost, r, c, element, r1, c1):
    if ((r*4) + c + 1 == element):
        return parentCost
    elif ((r1*4) + c1 + 1 == element):
        return parentCost + 2
    else:
        return parentCost + 1

# Fungsi membuat tuple baru sesuai pergerakan
def move(parent,r,c,r2,c2):
    tempMatrix = list(parent.buffer)
    tempMatrix[(r*4)+c] = tempMatrix[(r2*4)+c2]
    tempMatrix[(r2*4)+c2] = 16
    return tuple(tempMatrix)

# Fungsi utama pencarian solusi
def cariKemungkinan(prioQueue, visited):
    nodes = 1
    while (True):
        # Node parent untuk dicari kemungkinan geraknya
        parent = hq.heappop(prioQueue)
        visited.add(parent.buffer)
        r = parent.emptyTile[0]
        c = parent.emptyTile[1]
        # Kemungkinan gerak ke atas
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
        # Kemungkinan gerak ke kiri
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
        # Kemungkinan gerak ke kanan
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
        # Kemungkinan gerak ke kanan
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

# Fungsi pembacaan file pada folder ../test/
def readFile(filename):
    tempList = list([])
    try:
        with open("../test/" + filename) as f:
            content = f.readlines()
    except:
        print("File tidak ditemukan")
        exit()
    for x in content:
        i = 0
        while (i < len(x)) and (x[i] != '\n'):
            if (x[i] != ' ') and (x[i+1] == ' '):
                tempList.append(int(x[i]))
                i += 1
            elif (x[i] != ' ') and (x[i+1] != ' '):
                tempList.append(int(x[i:i+2]))
                i += 2
            else:
                i += 1
    return tuple(tempList)


if __name__ == "__main__":
    # Deklarasi variabel
    prioQueue = []
    visited  = set()
    puzzle = tuple([])
    cost = 0
    r = 0
    c = 0

    # Membaca file input
    input = input("Masukkan nama file: ")
    puzzle = readFile(input)

    tAwal = time.time()

    # Mencari posisi emptyTile
    for i in range(0,16):
        if puzzle[i] == 16:
            r = i // 4
            c = i % 4
            break
    
    # Mencari cost awal
    for i in range(0,16):
        if puzzle[i] != 16 and puzzle[i] != i+1:
            cost += 1

    # Pencarian solusi
    if fungsiKurang(puzzle) % 2 == 0:
        hq.heappush(prioQueue,(Node(0, cost, puzzle, [r,c], None)))
        end = cariKemungkinan(prioQueue, visited)
        tAkhir = time.time()

        # Menampilkan hasil dan informasinya
        pathway = []
        paths = end[0].level
        print("Jalur terpendek pada puzzle ini adalah:")
        while (end[0] != None):
            pathway.append(changeToZero(np.matrix(end[0].buffer)))
            end[0] = end[0].parent
        for i in range(len(pathway)-1, -1, -1):
            print(pathway[i], "\n")
        print("Nilai kurang:", fungsiKurang(puzzle))
        print("Jumlah pergerakan terpendek:", paths)
        print("Waktu:", tAkhir - tAwal, "detik")
        print("Simpul:", end[1])
    else:
        print("Nilai kurang:", fungsiKurang(puzzle))
        print("Cannot be solved")