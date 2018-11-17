import OpenGL
import math, string
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from copy import copy, deepcopy

import sys
import threading

#Gunakan tombol panah kanan,kiri,atas,bawah untuk menggerakan kamera
#Gunakan 'W' untuk zoom in dan 'S' untuk zoom out
#Gunakan 'D' untuk menambah msk (garis guide terlihat lebih lurus) dan 'A' untuk mengurangi msk
#Gunakan 'L' untuk menambah panjang axis X,Y,dan Z sebanyak 5 poin dan 'K' untuk mengurangi panjang sebanyak 5 poin/satuan


#Deklarasi Variabel Global
dim = 30.0 #msk
width = 1200 #lebar window
height = 675 #tinggi window
th = 0 #azimut / horizon angle
ph = 0 #elevation angle
fov = 55 #field of view (sudut pandang)
asp = width / height #aspect ratio
length = 500.0 #panjang axis
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

    if(msk == 2):
        dx = float(input('dx :'))
        dy = float(input('dy :'))
        b = [[1,0,0],[0,1,0],[dx,dy,1]]
        matrix = matmult(matrix,b)
    elif(msk == 3):
        dx = float(input('dx :'))
        dy = float(input('dy :'))
        dz = float(input('dz :'))
        b = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[dx,dy,dz,1]]
        koordinatkubus = matmult(koordinatkubus,b)
    #print(koordinatkubus)
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
        b = [[k,0,0,0],[0,k,0,0],[0,0,k,0],[0,0,0,k]]
        koordinatkubus = matmult(koordinatkubus,b)
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
        if(sumbu == 'x'):
            b = [[1,0,0,0],[0,math.cos(degree),-math.sin(degree),0],[0,math.sin(degree),math.cos(degree),0],[0,0,0,1]]
            koordinatkubus = matmult(koordinatkubus,b)
        elif(sumbu == 'y'):
            b = [[math.cos(degree),0,math.sin(degree),0],[0,1,0,0],[-math.sin(degree),0,math.cos(degree),0],[0,0,0,1]]
            koordinatkubus = matmult(koordinatkubus,b)
        elif(sumbu == 'z'):
            b = [[math.cos(degree),-math.sin(degree),0,0],[math.sin(degree),math.cos(degree),0,0],[0,0,1,0],[0,0,0,1]]
            koordinatkubus = matmult(koordinatkubus,b)
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
        if(param == 'x'):
            c = [[1,0,0,0],[k,1,0,0],[k,0,1,0],[0,0,0,1]]
            koordinatkubus = matmult(koordinatkubus,c)
        elif(param == 'y'):
            c = [[1,k,0,0],[0,1,0,0],[0,k,1,0],[0,0,0,1]]
            koordinatkubus = matmult(koordinatkubus,c)
        elif(param == 'z'):
            c = [[1,0,k,0],[0,1,k,0],[0,0,1,0],[0,0,0,1]]
            koordinatkubus = matmult(koordinatkubus,c)
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
        if(param == 'x'):
            c = [[k,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
            koordinatkubus = matmult(koordinatkubus,c)
        elif(param == 'y'):
            c = [[1,0,0,0],[0,k,0,0],[0,0,1,0],[0,0,0,1]]
            koordinatkubus = matmult(koordinatkubus,c)
        elif(param == 'z'):
            c = [[1,0,0,0],[0,1,0,0],[0,0,k,0],[0,0,0,1]]
            koordinatkubus = matmult(koordinatkubus,c)
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
        j = [[a,d,g,0],[b,e,h,0],[c,f,i,0],[0,0,0,1]]
        matrix = matmult(matrix,j)
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
    zip_b = zip(*b)
    zip_b = list(zip_b)
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b))
             for col_b in zip_b] for row_a in a]

def LogicDraw() :
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, asp , dim / 4 , dim * 4)
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
    for i in range (-1*int(length),int(length)) :
        glVertex3d(0.0,0.0,i)
        glVertex3d(length,0.0,i)

    for i in range (-1*int(length), int(length)) :
        glVertex3d(0.0,0.0,i)
        glVertex3d(-1*length,0.0,i)

    for i in range (-1*int(length),int(length)) :
        glVertex3d(0.0,i,0.0)
        glVertex3d(length,i,0.0)

    for i in range (-1*int(length),int(length)) :
        glVertex3d(0.0,i,0.0)
        glVertex3d(-1*length,i,0.0)


    #Mari kita gambar guide lines, sejajar sumbu z

    for i in range (-1*int(length),int(length)) :
        glVertex3d(i,0.0,0.0)
        glVertex3d(i,0.0,length)

    for i in range (-1*int(length), int(length)) :
        glVertex3d(i,0.0,0.0)
        glVertex3d(i,0.0,-1*length)

    for i in range (-1*int(length),int(length)) :
        glVertex3d(0.0,i,0.0)
        glVertex3d(0.0,i,length)

    for i in range (-1*int(length),int(length)) :
        glVertex3d(0.0,i,0.0)
        glVertex3d(0.0,i,-1*length)

    #Mari kita gambar guide lines, sejajar sumbu y

    for i in range (-1*int(length),int(length)) :
        glVertex3d(i,0.0,0.0)
        glVertex3d(i,length,0.0)

    for i in range (-1*int(length), int(length)) :
        glVertex3d(i,0.0,0.0)
        glVertex3d(i,-1*length,0.0)

    for i in range (-1*int(length),int(length)) :
        glVertex3d(0.0,0.0,i)
        glVertex3d(0.0,length,i)

    for i in range (-1*int(length),int(length)) :
        glVertex3d(0.0,0.0,i)
        glVertex3d(0.0,-1*length,i)


    glEnd()

def PrintWindow (x, y ,z, text) :
    glColor3f(1,1,1)
    glRasterPos3f(x,y,z)
    for i in range (0,len(text)) :
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18,ord(text[i]))


def DrawInfo () :
    global length
    PrintWindow(koordinatkubus[3][0],koordinatkubus[3][1],koordinatkubus[3][2],"x = \n" + str((koordinatkubus[3][0])) +",\n y = " + str((koordinatkubus[3][1])) + ",\n z = " + str((koordinatkubus[3][2])))
    PrintWindow(length,0.0,0.0,"X")
    PrintWindow(0.0,length,0.0,"Y")
    PrintWindow(0.0,0.0,length,"Z")
    return


def display() :
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()

    Vx = -2*dim*math.sin(math.radians(th))*math.cos(math.radians(ph))
    Vy = 2*dim
    Vz = 2*dim*math.cos(math.radians(th)) * math.cos(math.radians(ph))

    gluLookAt(Vx,Vy,Vz, #EyePosition
              0,0,0,#Origin
              0,math.cos(math.radians(ph)),0) #Up vector

    DrawCube3D()
    DrawInfo()
    DrawAxis()
    DrawGuide()

    LogicDraw()
    glFlush()
    glutSwapBuffers()



    return

def reshape (widthtemp , heighttemp) :
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
    global dim
    global length
    key = bkey.decode("utf-8")
    if (key == 's') :
        fov = fov + 5
    elif (key == 'w') :
        fov = fov - 5
    elif (key == 'd') :
        dim = dim + 10
    elif (key == 'a') :
        dim = dim -10
    elif (key == 'l') :
        length = length + 50
    elif (key == 'k') :
        length = length - 50
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
            elif(command == 'multiple'):
                multiple()
                glutPostRedisplay()
            elif(command == 'custom'):
                custom()
                glutPostRedisplay()
            elif(command == 'quit'):
                #sys.exit
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
                #sys.exit
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
