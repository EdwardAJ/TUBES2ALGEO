import OpenGL
import math, string
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from copy import copy, deepcopy

import sys
import time
import threading

#Gunakan tombol panah kanan,kiri,atas,bawah untuk menggerakan sudut kamera
#Gunakan 'W','A','S','D' untuk menggerakan kamera ke atas, kiri, bawah, kanan.
#Gunakan 'Z' dan 'X' untuk zoom in dan zoom out.

#Deklarasi Variabel Global
dim = 60.0 #msk
width = 1200 #lebar window
height = 675 #tinggi window
th = 0 #azimut / horizon angle
ph = 0 #elevation angle
#fov = 1.2 #field of view (sudut pandang)
asp = width / height #aspect ratio
length = 500.0 #panjang axis
movex = 0
movey = 0
movez = 0

global koordinatkubus
koordinatkubus = [
[1.0, 1.0, -1.0, 1.0],
[-1.0, 1.0, -1.0, 1.0],
[-1.0, 1.0, 1.0, 1.0],
[1.0, 1.0, 1.0, 1.0],

[1.0, -1.0, 1.0, 1.0],
[-1.0, -1.0, 1.0, 1.0],
[-1.0, -1.0, -1.0, 1.0],
[1.0, -1.0, -1.0, 1.0],

[1.0, 1.0, 1.0, 1.0],
[-1.0, 1.0, 1.0, 1.0],
[-1.0, -1.0, 1.0, 1.0],
[1.0, -1.0, 1.0, 1.0],

[1.0, -1.0, -1.0, 1.0],
[-1.0, -1.0, -1.0, 1.0],
[-1.0,  1.0, -1.0, 1.0],
[1.0,  1.0, -1.0, 1.0],

[-1.0,  1.0,  1.0, 1.0],
[-1.0,  1.0, -1.0, 1.0],
[-1.0, -1.0, -1.0, 1.0],
[-1.0, -1.0,  1.0, 1.0],

[1.0,  1.0, -1.0, 1.0],
[1.0,  1.0,  1.0, 1.0],
[1.0, -1.0,  1.0, 1.0],
[1.0, -1.0, -1.0, 1.0]
]
global firstkoordinatkubus
firstkoordinatkubus = deepcopy(koordinatkubus)
global matrix
global firstmatrix
global command
matrix=[] #define empty matrix

#Deklarasi Array dan Variabel2nya yang dibutuhkan
Neff = 100
#PosX[Neff] , Array berisi posisi X yang dimasukkan oleh user
#PosY[Neff] , Array berisi posisi Y yang dimasukkan oleh user
#PosZ[Neff] , Array berisi posisi Z yang dimasukkan oleh user
#Perintah[Neff], Array berisi perintah yang dimasukkan oleh user, kalau perintah tidak sesuai maka program looping ulang

#Deklarasi Input Awal
global msk
msk = "halo"

def MakeMatrix():
    global firstmatrix
    rows = int(input('Masukkan jumlah titik :'))

    for i in range(0,rows): #total row
            row=[]
            for j in range(0,3): #total column
                row.append(1.0) #adding 0 value for each column for this row
            matrix.append(row) #add fully defined column into the row


    for i in range(0,rows): #total row
        elemen = input(f"titik {i+1} :")
        z = elemen.split(' ')
        matrix[i][0] = float(z[0]);
        matrix[i][1] = float(z[1]);

    firstmatrix = deepcopy(matrix)

def translate():
    global koordinatkubus
    global matrix
    global msk
    #global dx,dy,dz,deltadx,deltady,deltadz

    if(msk == 2):
        dx = float(input('dx :'))
        dy = float(input('dy :'))
        b = [[1,0,0],[0,1,0],[dx,dy,1]]
        matrix = matmult(matrix,b)
    elif(msk == 3):

        dx = float(input('dx :'))
        dy = float(input('dy :'))
        dz = float(input('dz :'))

        timetemp = time.time()
        tempkoordinat = koordinatkubus
        deltadx = 0
        deltady = 0
        deltadz = 0
        while ((abs(deltadx) < abs(dx)) or (abs(deltady) < abs(dy)) or (abs(deltadz) < abs(dz))):
            if (abs(deltadx) <abs(dx)):
                    deltadx = deltadx + 0.01*dx
            if (abs(deltady) <abs(dy)):
                    deltady = deltady + 0.01*dy
            if (abs(deltadz) <abs(dz)):
                    deltadz = deltadz + 0.01*dz

            b = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[deltadx,deltady,deltadz,1]]
            koordinatkubus = matmult(tempkoordinat,b)


            newtime = time.time()
            sleeptime = ((1000/60) - (newtime - timetemp))/1000.0
            if sleeptime > 0:
                time.sleep(sleeptime)
            timetemp = newtime
            glutPostRedisplay()

    return


def dilate():
    global koordinatkubus
    global matrix
    global msk

    if(msk == 2):
        k = float(input("k :"))
        b = [[k,0,0],[0,k,0],[0,0,1]]
        matrix = matmult(matrix,b)

    elif(msk == 3):

        k = float(input("k :"))
        timetemp = time.time()
        tempkoordinat = koordinatkubus

        #MASIH ADA BUG
        if (abs(k) >= 1):
            deltak = 1
            while (abs(deltak) < abs(k)):
                deltak = deltak + 0.02*k
                b = [[deltak,0,0,0],[0,deltak,0,0],[0,0,deltak,0],[0,0,0,1]]
                koordinatkubus = matmult(tempkoordinat,b)
                newtime = time.time()
                sleeptime = ((1000/60) - (newtime - timetemp))/1000.0
                if sleeptime > 0:
                    time.sleep(sleeptime)
                timetemp = newtime
                glutPostRedisplay()
        else:
            deltak = 1
            while (abs(deltak) > abs(k)):
                deltak = deltak - 0.1*abs(k)
                b = [[deltak,0,0,0],[0,deltak,0,0],[0,0,deltak,0],[0,0,0,1]]
                koordinatkubus = matmult(tempkoordinat,b)
                newtime = time.time()
                sleeptime = ((1000/60) - (newtime - timetemp))/1000.0
                if sleeptime > 0:
                    time.sleep(sleeptime)
                timetemp = newtime
                glutPostRedisplay()


    #print(koordinatkubus)
    return

def rotate():
    global koordinatkubus
    global matrix
    global msk

    if(msk == 2):
        degree = float(input('degree :'))
        a = float(input('a :'))
        b = float(input('b :'))
        c = [[1,0,0],[0,1,0],[-a,-b,1]]
        matrix = matmult(matrix,c)
        degree = degree * math.pi / 180
        c = [[math.cos(degree),math.sin(degree),0],[-1*math.sin(degree),math.cos(degree),0],[0,0,1]]
        matrix = matmult(matrix,c)
        c = [[1,0,0],[0,1,0],[a,b,1]]
        matrix = matmult(matrix,c)
    elif(msk == 3):
        sumbu = input('sumbu :')
        degree = float(input('degree :'))
        degree = degree * math.pi / 180

        deltadeg = 0
        timetemp = time.time()
        tempkoordinat = koordinatkubus

        if(sumbu == 'x'):
            while (abs(deltadeg) < abs(degree)):
                deltadeg = deltadeg + 0.01*degree
                b = [[1,0,0,0],[0,math.cos(deltadeg),-math.sin(deltadeg),0],[0,math.sin(deltadeg),math.cos(deltadeg),0],[0,0,0,1]]
                koordinatkubus = matmult(tempkoordinat,b)
                newtime = time.time()
                sleeptime = ((1000/60) - (newtime - timetemp))/1000.0
                if sleeptime > 0:
                    time.sleep(sleeptime)
                timetemp = newtime
                glutPostRedisplay()

        elif(sumbu == 'y'):
            while (abs(deltadeg) < abs(degree)):
                deltadeg = deltadeg + 0.01*degree
                b = [[math.cos(deltadeg),0,math.sin(deltadeg),0],[0,1,0,0],[-math.sin(deltadeg),0,math.cos(deltadeg),0],[0,0,0,1]]
                koordinatkubus = matmult(tempkoordinat,b)
                newtime = time.time()
                sleeptime = ((1000/60) - (newtime - timetemp))/1000.0
                if sleeptime > 0:
                    time.sleep(sleeptime)
                timetemp = newtime
                glutPostRedisplay()

        elif(sumbu == 'z'):
            while (abs(deltadeg) < abs(degree)):
                deltadeg = deltadeg + 0.01*degree
                b = [[math.cos(deltadeg),-math.sin(deltadeg),0,0],[math.sin(deltadeg),math.cos(deltadeg),0,0],[0,0,1,0],[0,0,0,1]]
                koordinatkubus = matmult(tempkoordinat,b)
                newtime = time.time()
                sleeptime = ((1000/60) - (newtime - timetemp))/1000.0
                if sleeptime > 0:
                    time.sleep(sleeptime)
                timetemp = newtime
                glutPostRedisplay()

    #print(koordinatkubus)
    return

def reflect():
    global koordinatkubus
    global matrix
    global msk

    if(msk == 2):
        basis = str(input('basis :'))
        if(basis == 'x'):
            b = [[1,0,0],[0,-1,0],[0,0,1]]
            matrix = matmult(matrix,b)
        elif(basis == 'y'):
            b = [[-1,0,0],[0,1,0],[0,0,1]]
            matrix = matmult(matrix,b)
        elif(basis =='y=x'):
            b = [[0,1,0],[1,0,0],[0,0,1]]
            matrix = matmult(matrix,b)
        elif(basis == 'y=-x'):
            b = [[0,-1,0],[-1,0,0],[0,0,1]]
            matrix = matmult(matrix,b)
        elif(basis == 'a,b'):
            a = float(input('a :'))
            b = float(input('b :'))
            c = [[1,0,0],[0,1,0],[-a,-b,1]]
            matrix = matmult(matrix,c)
            c = [[-1,0,0],[0,-1,0],[0,0,1]]
            matrix = matmult(matrix,c)
            c = [[1,0,0],[0,1,0],[a,b,1]]
            matrix = matmult(matrix,c)
    elif(msk == 3):
        basis = str(input('basis :'))
        if(basis == 'xy'):
            b = [[1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,1]]
            koordinatkubus = matmult(koordinatkubus,b)
        elif(basis == 'yz'):
            b = [[-1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
            koordinatkubus = matmult(koordinatkubus,b)
        elif(basis == 'zx'):
            b = [[1,0,0,0],[0,-1,0,0],[0,0,1,0],[0,0,0,1]]
            koordinatkubus = matmult(koordinatkubus,b)
        elif(basis == '0,0,0'):
            b = [[-1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,1]]
            koordinatkubus = matmult(koordinatkubus,b)
    #print(koordinatkubus)
    return


def shear():
    global koordinatkubus
    global matrix
    global msk

    if(msk == 2):
        param = str(input('sumbu :'))
        k = float(input('k :'))
        if(param == 'x'):
            c = [[1,0,0],[k,1,0],[0,0,1]]
            matrix = matmult(matrix,c)
        elif(param == 'y'):
            c = [[1,k,0],[0,1,0],[0,0,1]]
            matrix = matmult(matrix,c)

    if(msk == 3):
        param = str(input('sumbu :'))
        k = float(input('k :'))
        deltak = 0
        timetemp = time.time()
        tempkoordinat = koordinatkubus
        if(param == 'x'):
            while (abs(deltak) < abs(k)):
                deltak = deltak + 0.02*k
                c = [[1,0,0,0],[deltak,1,0,0],[deltak,0,1,0],[0,0,0,1]]
                koordinatkubus = matmult(tempkoordinat,c)
                newtime = time.time()
                sleeptime = ((1000/60) - (newtime - timetemp))/1000.0
                if sleeptime > 0:
                    time.sleep(sleeptime)
                timetemp = newtime
                glutPostRedisplay()

        elif(param == 'y'):
            while (abs(deltak) < abs(k)):
                deltak = deltak + 0.02*k
                c = [[1,deltak,0,0],[0,1,0,0],[0,deltak,1,0],[0,0,0,1]]
                koordinatkubus = matmult(tempkoordinat,c)
                newtime = time.time()
                sleeptime = ((1000/60) - (newtime - timetemp))/1000.0
                if sleeptime > 0:
                    time.sleep(sleeptime)
                timetemp = newtime
                glutPostRedisplay()

        elif(param == 'z'):
            while (abs(deltak) < abs(k)):
                deltak = deltak + 0.02*k
                c = [[1,0,deltak,0],[0,1,deltak,0],[0,0,1,0],[0,0,0,1]]
                koordinatkubus = matmult(koordinatkubus,c)
                newtime = time.time()
                sleeptime = ((1000/60) - (newtime - timetemp))/1000.0
                if sleeptime > 0:
                    time.sleep(sleeptime)
                timetemp = newtime
                glutPostRedisplay()

    #print(koordinatkubus)
    return

def stretch():
    global koordinatkubus
    global matrix
    global msk

    if(msk == 2):
        param = str(input('sumbu :'))
        k = float(input('k :'))
        if(param == 'x'):
            c = [[k,0,0],[0,1,0],[0,0,1]]
            matrix = matmult(matrix,c)
        elif(param == 'y'):
            c = [[1,0,0],[0,k,0],[0,0,1]]
            matrix = matmult(matrix,c)
    elif(msk == 3):
        param = str(input('sumbu :'))
        k = float(input('k :'))
        deltak = 0
        timetemp = time.time()
        tempkoordinat = koordinatkubus

        if(param == 'x'):
            while (abs(deltak) < abs(k)):
                deltak = deltak + 0.02*k
                c = [[deltak,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
                koordinatkubus = matmult(tempkoordinat,c)
                newtime = time.time()
                sleeptime = ((1000/60) - (newtime - timetemp))/1000.0
                if sleeptime > 0:
                    time.sleep(sleeptime)
                timetemp = newtime
                glutPostRedisplay()

        elif(param == 'y'):
            while (abs(deltak) < abs(k)):
                deltak = deltak + 0.02*k
                c = [[1,0,0,0],[0,deltak,0,0],[0,0,1,0],[0,0,0,1]]
                koordinatkubus = matmult(tempkoordinat,c)
                newtime = time.time()
                sleeptime = ((1000/60) - (newtime - timetemp))/1000.0
                if sleeptime > 0:
                    time.sleep(sleeptime)
                timetemp = newtime
                glutPostRedisplay()

        elif(param == 'z'):
            while (abs(deltak) < abs(k)):
                deltak = deltak + 0.02*k
                c = [[1,0,0,0],[0,1,0,0],[0,0,deltak,0],[0,0,0,1]]
                koordinatkubus = matmult(tempkoordinat,c)
                newtime = time.time()
                sleeptime = ((1000/60) - (newtime - timetemp))/1000.0
                if sleeptime > 0:
                    time.sleep(sleeptime)
                timetemp = newtime
                glutPostRedisplay()

    #print(koordinatkubus)
    return

def custom():
    global koordinatkubus
    global matrix
    if (msk == 2):
        a = float(input('a :'))
        b = float(input('b :'))
        c = float(input('c :'))
        d = float(input('d :'))
        e = [[a,c,0],[b,d,0],[0,0,1]]
        matrix = matmult(matrix,e)
    elif (msk == 3):
        a = float(input('a :'))
        b = float(input('b :'))
        c = float(input('c :'))
        d = float(input('d :'))
        e = float(input('e :'))
        f = float(input('f :'))
        g = float(input('g :'))
        h = float(input('h :'))
        i = float(input('i :'))
        da = 0
        db = 0
        dc = 0
        dd = 0
        de = 0
        df = 0
        dg = 0
        dh = 0
        di = 0
        timetemp = time.time()
        tempkoordinat = koordinatkubus
        while ((abs(da) < abs(a)) or (abs(db) < abs(b)) or (abs(dc) < abs(c)) or (abs(dd) < abs(d)) or (abs(de) < abs(e)) or (abs(df) < abs(f)) or (abs(dg) < abs(g)) or (abs(dh) < abs(h)) or (abs(di) < abs(i))):
            if ((abs(da) < abs(a))):
                da = da + 0.01*a
            if ((abs(db) < abs(b))):
                db = db + 0.01*b
            if ((abs(dc) < abs(c))):
                dc = dc + 0.01*c
            if ((abs(dd) < abs(d))):
                dd = dd + 0.01*d
            if ((abs(de) < abs(e))):
                de = de + 0.01*e
            if ((abs(df) < abs(f))):
                df = df + 0.01*f
            if ((abs(dg) < abs(g))):
                dg = dg + 0.01*g
            if ((abs(dh) < abs(h))):
                dh = dh + 0.01*h
            if ((abs(di) < abs(i))):
                di = di + 0.01*i

            j = [[da,dd,dg,0],[db,de,dh,0],[dc,df,di,0],[0,0,0,1]]
            koordinatkubus = matmult(tempkoordinat,j)
            newtime = time.time()
            sleeptime = ((1000/60) - (newtime - timetemp))/1000.0
            if sleeptime > 0:
                time.sleep(sleeptime)
            timetemp = newtime
            glutPostRedisplay()

    #print(koordinatkubus)
    return

def reset():
    global koordinatkubus
    global matrix
    #global firstmatrix
    if (msk == 2):
        matrix = deepcopy(firstmatrix)
    elif (msk == 3):
        koordinatkubus = deepcopy(firstkoordinatkubus)
    #print(koordinatkubus)
    return

def multiple():
    global koordinatkubus
    i = int(input('Banyak perintah :'))
    for i in range(i):
        print(i)
        print(' :')
        command = input('')
        if(command == 'translate'):
            translate()
            glutPostRedisplay()
        elif(command == 'dilate'):
            dilate()
            glutPostRedisplay()
        elif(command == 'rotate'):
            rotate()
            glutPostRedisplay()
        elif(command == 'reflect'):
            reflect()
            glutPostRedisplay()
        elif(command == 'shear'):
            shear()
            glutPostRedisplay()
        elif(command == 'stretch'):
            stretch()
            glutPostRedisplay()


def matmult(a,b):
    global width,height
    zip_b = zip(*b)
    zip_b = list(zip_b)
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b))
             for col_b in zip_b] for row_a in a]

def LogicDraw() :
    global dx,dy,dz
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    #gluPerspective(fov, asp , dim / 4 , dim * 4)
    #glOrtho(-1000 * fov , width * fov ,height * fov ,100,0 *fov ,-100 *fov)
    glOrtho(-dim*asp,+dim*asp, -dim,+dim, -dim,+dim)
    glTranslate( -movex , -movey , -movez )
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    return


def DrawCube3D () :
    #Kode Untuk Membuat Kubus
    #Membuat Grafik Khusus 3D
    glBegin(GL_QUADS)
    global koordinatkubus
    #koordinatkubus = [[1.0, 1.0, -1.0],[-1.0, 1.0, -1.0],[-1.0, 1.0, 1.0],[1.0, 1.0, 1.0]]

    #Menyebutkan titik sudut kubus pada setiap sisi, beserta warna pada setiap sisi
    #Sisi atas kubus, warna hijau
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(koordinatkubus[0][0], koordinatkubus[0][1], koordinatkubus[0][2])
    glVertex3f(koordinatkubus[1][0], koordinatkubus[1][1], koordinatkubus[1][2])
    glVertex3f(koordinatkubus[2][0], koordinatkubus[2][1], koordinatkubus[2][2])
    glVertex3f(koordinatkubus[3][0], koordinatkubus[3][1], koordinatkubus[3][2])

    #Sisi bawah kubus, warna kuning
    glColor3f(1.0, 0.5, 0.0)
    glVertex3f(koordinatkubus[4][0], koordinatkubus[4][1], koordinatkubus[4][2])
    glVertex3f(koordinatkubus[5][0], koordinatkubus[5][1], koordinatkubus[5][2])
    glVertex3f(koordinatkubus[6][0], koordinatkubus[6][1], koordinatkubus[6][2])
    glVertex3f(koordinatkubus[7][0], koordinatkubus[7][1], koordinatkubus[7][2])

    #Sisi depan kubus
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(koordinatkubus[8][0], koordinatkubus[8][1], koordinatkubus[8][2])
    glVertex3f(koordinatkubus[9][0], koordinatkubus[9][1], koordinatkubus[9][2])
    glVertex3f(koordinatkubus[10][0], koordinatkubus[10][1], koordinatkubus[10][2])
    glVertex3f(koordinatkubus[11][0], koordinatkubus[11][1], koordinatkubus[11][2])

    #Sisi belakang kubus
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(koordinatkubus[12][0], koordinatkubus[12][1], koordinatkubus[12][2])
    glVertex3f(koordinatkubus[13][0], koordinatkubus[13][1], koordinatkubus[13][2])
    glVertex3f(koordinatkubus[14][0], koordinatkubus[14][1], koordinatkubus[14][2])
    glVertex3f(koordinatkubus[15][0], koordinatkubus[15][1], koordinatkubus[15][2])

    #Sisi kiri kubus
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(koordinatkubus[16][0], koordinatkubus[16][1], koordinatkubus[16][2])
    glVertex3f(koordinatkubus[17][0], koordinatkubus[17][1], koordinatkubus[17][2])
    glVertex3f(koordinatkubus[18][0], koordinatkubus[18][1], koordinatkubus[18][2])
    glVertex3f(koordinatkubus[19][0], koordinatkubus[19][1], koordinatkubus[19][2])

    #Sisi kanan kubus
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(koordinatkubus[20][0], koordinatkubus[20][1], koordinatkubus[20][2])
    glVertex3f(koordinatkubus[21][0], koordinatkubus[21][1], koordinatkubus[21][2])
    glVertex3f(koordinatkubus[22][0], koordinatkubus[22][1], koordinatkubus[22][2])
    glVertex3f(koordinatkubus[23][0], koordinatkubus[23][1], koordinatkubus[23][2])

    glEnd()

    return

def DrawAxis () :

    glBegin(GL_LINES)

    glColor3f(0.0,1.0,1.0)
    glVertex3d(0.0,0.0,0.0)
    glVertex3d(-1*length,0.0,0.0)
    glVertex3d(length,0.0,0.0)

    glVertex3d(0,0,0)
    glVertex3d(0,length,0)
    glVertex3d(0,-1*length,0)

    glVertex3d(0,0,0)
    glVertex3d(0.0,0.0,length)

    glVertex3d(0,0,0)
    glVertex3d(0.0,0.0,-1.0*length)

    glEnd()

    return

def DrawGuide () :
    glBegin(GL_LINES)

    glColor4f(0.5, 0.5, 0.5, 0.3); #mengurangi opacity :)

    #Mari kita gambar guide lines, sejajar sumbu x
    i = -length
    while (i <= length):
        glVertex3d(0.0,0.0,i)
        glVertex3d(length,0.0,i)
        i = i + 50

    i = -length
    while (i<= length):
        glVertex3d(0.0,0.0,i)
        glVertex3d(-1*length,0.0,i)
        i = i + 50

    #Mari kita gambar guide lines, sejajar sumbu z

    i = -length
    while (i <= length):

        glVertex3d(i,0.0,0.0)
        glVertex3d(i,0.0,length)

        i = i + 50

    i = -length
    while (i <= length):

        glVertex3d(i,0.0,0.0)
        glVertex3d(i,0.0,-1*length)
        i = i + 50

    glEnd()

def PrintWindow (x, y ,z, text) :
    glColor3f(1,1,1)
    glRasterPos3f(x,y,z)
    for i in range (0,len(text)) :
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12,ord(text[i]))

def PrintInfoGuide (x, y ,z, text) :
    glColor4f(1, 1, 1, 0.3);
    glRasterPos3f(x,y,z)
    for i in range (0,len(text)) :
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10,ord(text[i]))


def DrawInfo () :
    global length
    PrintWindow(koordinatkubus[3][0],koordinatkubus[3][1],koordinatkubus[3][2],"x = \n" + str(round(koordinatkubus[3][0],2)) +",\n y = " + str(round(koordinatkubus[3][1],2)) + ",\n z = " + str(round(koordinatkubus[3][2],2)))
    PrintWindow(length+10,0.0,0.0,"X")
    PrintWindow(0.0,length+10,0.0,"Y")
    PrintWindow(0.0,0.0,length+10,"Z")
    i = -500
    while (i <= length):
        PrintInfoGuide(i,0,0,str(i))
        i = i + 50
    return


def display() :
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()

    glRotatef(ph,1,0,0);
    glRotatef(th,0,1,0);

    DrawCube3D()
    DrawInfo()
    DrawAxis()
    DrawGuide()

    LogicDraw()
    glFlush()
    glutSwapBuffers()

    return

def reshape (widthtemp , heighttemp) : #Menjaga aspect ratio dari "world"
    global width,height
    widthtemp = width
    heighttemp = height
    asp = widthtemp / heighttemp
    glViewport(0,0, (widthtemp), (heighttemp))
    LogicDraw()



def keyboardSpecial(key, x, y):
    global th
    global ph

    if (key == GLUT_KEY_RIGHT) :
        th = th + 5
    elif (key == GLUT_KEY_LEFT) :
        th = th - 5
    elif (key == GLUT_KEY_UP) :
        ph = ph + 5
    elif (key == GLUT_KEY_DOWN) :
        ph = ph - 5

    th = th % 360
    ph = ph % 360

    LogicDraw()
    glutPostRedisplay()

    return


def keyboardKey (bkey , x , y) :
    global fov
    global movex,movey,movez
    global dim
    global length
    key = bkey.decode("utf-8")
    if (key == 's') :
        movey = movey - 5
    elif (key == 'w') :
        movey = movey + 5
    elif (key == 'd') :
         movex = movex + 5
    elif (key == 'a') :
        movex = movex - 5
    elif (key == 'z') :
        if (dim > 10):
            dim = dim - 10
        else:
            dim = dim + 10
    elif (key == 'x') :
        dim = dim +10
    elif (key == 't') :
         glutLeaveMainLoop()

    LogicDraw()
    glutPostRedisplay()


def Draw3DWorld () :
    global command
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow("3D SYSTEM BETA")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutSpecialFunc(keyboardSpecial)
    glutKeyboardFunc(keyboardKey)
    glutMainLoop()
    if(command =='quit'):
        #sys.exit
        glutLeaveMainLoop()

    return


def init():
    glClearColor(0.0,0.0,0.0,1.0)
    gluOrtho2D(-500.0,500.0,-500.0,500.0)

def Draw2DAxis() :
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0,1.0,1.0)
    glBegin(GL_LINES)

    glVertex2f(-1*length,0.0)
    glVertex2f(length,0.0)
    glVertex2f(0.0,-1*length)
    glVertex2f(0.0,length)
    glEnd()
    glFlush()

def plotmatrix():
    Draw2DAxis()

    glBegin(GL_POLYGON)
    glColor3f(1.0,0.0,0.0)
    for i in range(0,len(matrix)-1):
        glVertex2f(matrix[i][0],matrix[i][1])
        glVertex2f(matrix[i+1][0],matrix[i+1][1])
    glVertex2f(matrix[len(matrix)-1][0],matrix[len(matrix)-1][1])
    glVertex2f(matrix[0][0],matrix[0][1])
    glEnd()
    glFlush()

def Draw2DWorld():
    global command
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutCreateWindow("2D SYSTEM BETA")
    glutDisplayFunc(plotmatrix)
    init()
    glutMainLoop()
    if(command =='quit'):
        #sys.exit
        glutLeaveMainLoop()
    return


def main3():
    Draw2DWorld()
    display()

def main2():
    Draw3DWorld()
    display()

def main1() :
    global dx,dy,dz
    global koordinatkubus
    global msk
    global command
    print("Selamat Datang di TUBES 2 ALGEO!")
    msk = int(input("Silakan input apakah Anda mau 2D atau 3D!\n"))
    if (msk == 3):
        thread.start() #Window 3d World
        #thread.join()
        #thread2.start()
        command = ''
        #command = input('Silakan masukan perintah :\n')
        while (command != 'quit'):
            command = input('Command : ')
            if(command == 'translate'):
                translate()
                #glutPostRedisplay()
            elif(command == 'dilate'):
                dilate()
            elif(command == 'rotate'):
                rotate()

            elif(command == 'reflect'):
                reflect()
                glutPostRedisplay()
            elif(command == 'shear'):
                shear()
                glutPostRedisplay()
            elif(command == 'stretch'):
                stretch()
                glutPostRedisplay()
            elif(command == 'reset'):
                reset()
                glutPostRedisplay()
            elif(command == 'multiple'):
                multiple()
                glutPostRedisplay()
            elif(command == 'custom'):
                custom()
                glutPostRedisplay()
            elif(command == 'quit'):
                #sys.exit()
                glutLeaveMainLoop()
                break


    elif (msk == 2):
        MakeMatrix()
        thread3.start() #window 2d World
        command = ''
        #command = input('Silakan masukan perintah :\n')
        while (command != 'quit'):
            command = input('Command : ')
            if(command == 'translate'):
                translate()
                glutPostRedisplay()
            elif(command == 'dilate'):
                dilate()
                glutPostRedisplay()
            elif(command == 'rotate'):
                rotate()
                glutPostRedisplay()
            elif(command == 'reflect'):
                reflect()
                glutPostRedisplay()
            elif(command == 'shear'):
                shear()
                glutPostRedisplay()
            elif(command == 'stretch'):
                stretch()
                glutPostRedisplay()
            elif(command == 'reset'):
                reset()
                glutPostRedisplay()
            elif(command == 'custom'):
                custom()
                glutPostRedisplay()
            elif(command == 'multiple'):
                multiple()
                glutPostRedisplay()
            elif(command == 'quit'):
                #sys.exit()
                glutLeaveMainLoop()
                break

    return

thread = threading.Thread(target = main2)
thread2 = threading.Thread(target = main1)
thread3 = threading.Thread(target = main3)
thread2.start()

'''
if __name__ == '__main__':
    main1()
    main2()
'''
