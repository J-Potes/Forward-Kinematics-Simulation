"""
FK

@author: 
    Juan Jose Potes Gomez
    Julie Alejandra Ibarra
    Cristian Camilo Jimenez
"""
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
from scipy.optimize import fsolve


# Funcion para pasar angulo de radianes a grados y viceversa
def conv_ang(angulo, tipo):
    if tipo == "rad":
        conv = (angulo * np.pi)/180
        return conv
    if tipo == "grad":
        conv = (angulo * 180)/np.pi
        return conv

# Funcion que grafica un circulo con OpenGL
def circle(xc,yc,radio,clr,nsides):
    n = 0
    glBegin(GL_LINE_STRIP)
    glColor3f(clr[0], clr[1], clr[2])
    while(n <= nsides):
        angle = 2*np.pi*n/nsides
        x = xc+radio*np.cos(angle)
        y = yc+radio*np.sin(angle)
        glVertex2f(x,y)
        n += 1
    glEnd()

# Funcion que grafica una linea con openGL
def linea(x1,y1,x2,y2,clr):
    glBegin(GL_LINES)
    glColor3f(clr[0], clr[1], clr[2])
    glVertex2f(x1,y1)
    glVertex2f(x2,y2)
    glEnd()

# Funcion para graficar el plano 2d de referencia
def plano():
    linea(0,-ejeY,0,ejeY,[0.8,0.8,0.8])
    linea(-ejeX,0,ejeX,0,[0.8,0.8,0.8])

# Funcion que grafica las lineas entre los puntos de la malla
def lineas_union():
    global puntos
    for i in range(1, len(puntos)):
        x0 = puntos[i-1].pos[0]
        y0 = puntos[i-1].pos[1]
        x1 = puntos[i].pos[0]
        y1 = puntos[i].pos[1]
        linea(x0,y0,x1,y1,[1,1,0])
        
        
# Definicion de clase punto
class Punto:
    # Constructor de la clase
    def __init__(self, pos, rad, color):
        self.pos = pos
        self.rad = rad
        self.color = color
    
    # Metodo para mostrar la particula en la posicion respectiva
    def graficar(self):
        circle(self.pos[0],self.pos[1],self.rad,self.color,20)

# Funcion que halla la posicion del segundo punto respecto al angulo
def mover_1(theta):
    puntos[1].pos[0] = puntos[0].pos[0] + (d1 * np.cos(theta))
    puntos[1].pos[1] = puntos[0].pos[1] + (d1 * np.sin(theta))

# Funcion que retorna las ecuaciones para el sistema de ecuaciones del tercer punto
def func(p):
    f1 = (p[0] - puntos[1].pos[0])**2 + (p[1] - puntos[1].pos[1])**2 - d2**2
    f2 = (p[0] - puntos[3].pos[0])**2 + (p[1] - puntos[3].pos[1])**2 - d3**2
    return [f1, f2]

# Funcion que resuelve el sistema de ecuaciones para hallar la posicion del punto 3
def mover_2():
    # A fsolve se le envian las funciones del sistema y unos sugeridos que haran que retorne la solucion del sistema mas cercana a estos
    res = fsolve(func, [10, 10])
    puntos[2].pos[0] = res[0]
    puntos[2].pos[1] = res[1]

# Funcion para graficar los puntos y las lineas entre ellos
def graficar_sistema():
    global puntos
    # Se grafican los puntos
    for i in range(0, len(puntos)):
        puntos[i].graficar()
    # Se grafican las lineas
    lineas_union()

# Ejes del plano de coordenadas 2D
ejeX = 15
ejeY = 15

# Propiedades de los puntos
r = 0.15
clr = [0,1,0]

# Variables del tiempo
ht = 0.003
t = 0
t_max = 100

# Angulo inicial y velocidad angular
ang = conv_ang(60,"rad")
vel_ang = 1 #rad/s

# Distancias entre puntos
d1 = 5
d2 = 10
d3 = 10

# Se declara la lista de puntos
puntos = np.empty([4],dtype=object)

# Los puntos fijos
puntos[0] = Punto([0,0],r,clr)
puntos[3] = Punto([10,0],r,clr)

# Se declaran los puntos intermedios con posiciones en 0
puntos[1] = Punto([0,0],r,clr)
puntos[2] = Punto([0,0],r,clr)
# Se llama a las funciones mover para posicionar los puntos intermedios en su lugar respectivo
mover_1(ang)
mover_2()

# Funcion principal
def main():
    global t, ang, vel_ang
    running = True
    pygame.init()
    display=(600,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluOrtho2D(-10,ejeX,-10,ejeY)
    
    # Ciclo para que se vaya visualizando la simulacion
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running=False
                break
            
        # Se ejecuta mientras que el tiempo total sea menor al tiempo maximo definido
        if( running == True and t <= t_max):
            # Se limpia la pantalla de OpenGL
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            
            # plano()
            # circle(puntos[1].pos[0],puntos[1].pos[1],d2,[0,1,1],50)
            # circle(puntos[3].pos[0],puntos[3].pos[1],d3,[1,0,1],50)
            
            graficar_sistema()
            
            # El angulo aumenta respecto a la velocidad angular
            ang = (ht * vel_ang) + ang
            
            mover_1(ang)
            mover_2()
            
            pygame.display.flip() # Mostrar pantalla
            pygame.time.wait(1)
            print("Tiempo procesado: ",round(t,3)," s")
            t+=ht
        else:
            running = False
            break

    print("Tiempo total simulado = ",round(t,3)," s")
    pygame.quit()

main()