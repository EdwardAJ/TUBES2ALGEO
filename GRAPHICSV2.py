import OpenGL
import math, string
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


import sys

#Gunakan tombol panah kanan,kiri,atas,bawah untuk menggerakan kamera
#Gunakan 'W' untuk zoom in dan 'S' untuk zoom out
#Gunakan 'D' untuk menambah dimensi (garis guide terlihat lebih lurus) dan 'A' untuk mengurangi dimensi
#Gunakan 'L' untuk menambah panjang axis X,Y,dan Z sebanyak 5 poin dan 'K' untuk mengurangi panjang sebanyak 5 poin/satuan


#Deklarasi Variabel Global
dim = 8.0 #dimensi
width = 1200 #lebar window
height = 675 #tinggi window
th = 0 #azimut / horizon angle
ph = 0 #elevation angle
fov = 55 #field of view (sudut pandang)
asp = width / height #aspect ratio
length = 10.0 #panjang axis

#Deklarasi Array dan Variabel2nya yang dibutuhkan
Neff = 100
#PosX[Neff] , Array berisi posisi X yang dimasukkan oleh user
#PosY[Neff] , Array berisi posisi Y yang dimasukkan oleh user
#PosZ[Neff] , Array berisi posisi Z yang dimasukkan oleh user
#Perintah[Neff], Array berisi perintah yang dimasukkan oleh user, kalau perintah tidak sesuai maka program looping ulang

#Deklarasi Input Awal
msk = "halo"


def LogicDraw() :
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, asp , dim / 4 , dim * 4)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    return

def DrawShape2D (x,y) :
    glBegin(GL_QUADS)
    glcolor3f(0.0,1.0,0.0)
    glVertex3f(x,y,0)
    glEnd()

def DrawCube3D () :
    #Kode Untuk Membuat Kubus
    #Membuat Grafik Khusus 3D
    glBegin(GL_QUADS)

    #Menyebutkan titik sudut kubus pada setiap sisi, beserta warna pada setiap sisi
    #Sisi atas kubus, warna hijau
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f( 1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0,  1.0)
    glVertex3f( 1.0, 1.0, 1.0)

    #Sisi bawah kubus, warna kuning
    glColor3f(1.0, 0.5, 0.0)
    glVertex3f( 1.0, -1.0,  1.0)
    glVertex3f(-1.0, -1.0,  1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f( 1.0, -1.0, -1.0)

    #Sisi depan kubus
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f( 1.0,  1.0, 1.0)
    glVertex3f(-1.0,  1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f( 1.0, -1.0, 1.0)

    #Sisi belakang kubus
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f( 1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0,  1.0, -1.0)
    glVertex3f( 1.0,  1.0, -1.0)

    #Sisi kiri kubus
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0,  1.0,  1.0)
    glVertex3f(-1.0,  1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0,  1.0)

    #Sisi kanan kubus
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0,  1.0, -1.0)
    glVertex3f(1.0,  1.0,  1.0)
    glVertex3f(1.0, -1.0,  1.0)
    glVertex3f(1.0, -1.0, -1.0)

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
    PrintWindow(1.0,1.0,1.0,"1.0,1.0,1.0")
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
        fov = fov + 1
    elif (key == 'w') :
        fov = fov - 1
    elif (key == 'd') :
        dim = dim + 1
    elif (key == 'a') :
        dim = dim - 1
    elif (key == 'l') :
        length = length + 5
    elif (key == 'k') :
        length = length - 5

    LogicDraw()
    glutPostRedisplay()




def Draw3DWorld () :
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow("3D SYSTEM BETA")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutSpecialFunc(keyboardSpecial)
    glutKeyboardFunc(keyboardKey)
    glutMainLoop()
    return

def main () :
    global msk
    print("Selamat Datang di TUBES 2 ALGEO!")
    msk = input("Silakan input apakah Anda mau 2D atau 3D!\n")
    if (msk == "3D") :
        Draw3DWorld()

    return

if __name__ == '__main__': main()
