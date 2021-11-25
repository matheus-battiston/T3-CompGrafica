# **********************************************************************
# PUCRS/FACIN
# COMPUTAÃ‡ÃƒO GRÃFICA
#
# Teste de colisÃ£o em OpenGL
#
# Marcio Sarroglia Pinho
# pinho@inf.pucrs.br
# **********************************************************************
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import Ponto
from Linha import Linha
import time
import sys
from PIL import Image
Angulo = 0.0
angulo = 0
angulo2 = 0
posx = -19
posz = 0
textura = None
rota_paralelepipedo = 0
# **********************************************************************
#  init()
#  Inicializa os parÃ¢metros globais de OpenGL
# / **********************************************************************
def init():
    global textura
    # Define a cor do fundo da tela (BRANCO)
    glClearColor(0.5, 0.5, 0.5, 1.0)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_TEXTURE_2D);
    textura = loadTexture()

texture_num = 2
textures = [1001, 1011]
def loadTexture():
        global texture_num, textures
        glEnable(GL_TEXTURE_2D);
        glGenTextures(2, textures)
        level = 0
        border = 0

        # Create Texture
        glBindTexture(GL_TEXTURE_2D, int(textures[0]))  # 2d texture (x and y size)

        image = Image.open("grassy_d.png")

        ix = image.size[0]
        iy = image.size[1]
        img_data = np.array(list(image.getdata()), np.int8)
        formato = GL_RGB
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, level, formato,ix, iy,border, formato,GL_UNSIGNED_BYTE,img_data);

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

        glBindTexture(GL_TEXTURE_2D, int(textures[1]))  # 2d texture (x and y size)

        image = Image.open('TIjolo_med.jpg')

        ix = image.size[0]
        iy = image.size[1]
        img_data = np.array(list(image.getdata()), np.int8)
        formato = GL_RGB
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, level, formato, ix, iy, border, formato, GL_UNSIGNED_BYTE, img_data);

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);



        return textures


def cilindro():
    global angulo,angulo2,posx,posz,rota_paralelepipedo
    quadric = gluNewQuadric()
    glPushMatrix()
    glTranslated(posx-1,-0.2,posz)
    glRotatef(90+angulo+rota_paralelepipedo,0,1,0)
    glRotatef(-20+angulo2,1,0,0)
    gluCylinder(quadric, 0.2, 0.2, 2, 5, 5);

    glPopMatrix()

def desenha_canhao():
    global angulo
    global posx,posz
    global rota_paralelepipedo
    glPushMatrix()
    glTranslated(posx,-0.5,posz)
    glRotatef(90+rota_paralelepipedo, 0, 1, 0)

    glBegin(GL_QUADS);
    glVertex3f(-1, -0.5, 1.5);
    glVertex3f(1, -0.5, 1.5);
    glVertex3f(1, 0.5, 1.5);
    glVertex3f(-1, 0.5, 1.5);

    glVertex3f(-1, -0.5, -1.5);
    glVertex3f(-1, 0.5, -1.5);
    glVertex3f(1, 0.5, -1.5);
    glVertex3f(1, -0.5, -1.5);

    glVertex3f(-1, 0.5, -1.5);
    glVertex3f(-1, 0.5, 1.5);
    glVertex3f(1, 0.5, 1.5);
    glVertex3f(1, 0.5, -1.5);

    glVertex3f(-1, -0.5, -1.5);
    glVertex3f(1, -0.5, -1.5);
    glVertex3f(1, -0.5, 1.5);
    glVertex3f(-1, -0.5, 1.5);

    glVertex3f(1, -0.5, -1.5);
    glVertex3f(1, 0.5, -1.5);
    glVertex3f(1, 0.5, 1.5);
    glVertex3f(1, -0.5, 1.5);

    glVertex3f(-1, -0.5, -1.5);
    glVertex3f(-1, -0.5, 1.5);
    glVertex3f(-1, 0.5, 1.5);
    glVertex3f(-1, 0.5, -1.5);
    glEnd();
    glPopMatrix()


#  reshape( w: int, h: int )
#  trata o redimensionamento da janela OpenGL
#
# **********************************************************************
def reshape(w: int, h: int):
    global AspectRatio
    # Evita divisÃ£o por zero, no caso de uam janela com largura 0.
    if h == 0:
        h = 1
    # Ajusta a relaÃ§Ã£o entre largura e altura para evitar distorÃ§Ã£o na imagem.
    # Veja funÃ§Ã£o "PosicUser".
    AspectRatio = w / h
    # Reset the coordinate system before modifying
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    glViewport(0, 0, w, h)

    PosicUser()


# **********************************************************************
def DefineLuz():
    # Define cores para um objeto dourado
    LuzAmbiente = [0.4, 0.4, 0.4]
    LuzDifusa = [0.7, 0.7, 0.7]
    LuzEspecular = [0.9, 0.9, 0.9]
    PosicaoLuz0 = [2.0, 3.0, 0.0]  # PosiÃ§Ã£o da Luz
    Especularidade = [1.0, 1.0, 1.0]

    # ****************  Fonte de Luz 0

    glEnable(GL_COLOR_MATERIAL)

    # Habilita o uso de iluminaÃ§Ã£o
    glEnable(GL_LIGHTING)

    # Ativa o uso da luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, LuzAmbiente)
    # Define os parametros da luz nÃºmero Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, LuzAmbiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LuzDifusa)
    glLightfv(GL_LIGHT0, GL_SPECULAR, LuzEspecular)
    glLightfv(GL_LIGHT0, GL_POSITION, PosicaoLuz0)
    glEnable(GL_LIGHT0)

    # Ativa o "Color Tracking"
    glEnable(GL_COLOR_MATERIAL)

    # Define a reflectancia do material
    glMaterialfv(GL_FRONT, GL_SPECULAR, Especularidade)

    # Define a concentraÃ§Ã£oo do brilho.
    # Quanto maior o valor do Segundo parametro, mais
    # concentrado serÃ¡ o brilho. (Valores vÃ¡lidos: de 0 a 128)
    glMateriali(GL_FRONT, GL_SHININESS, 51)


# **********************************************************************
# DesenhaCubos()
# Desenha o cenario
#
# **********************************************************************
def DesenhaCubo():

    glutSolidCube(1)

userx = -23
usery = 0
userz = 0
lookx = 0
looky = 0
lookz = 0
def PosicUser():
    global userx
    global usery
    global userz
    global lookx
    global looky
    global lookz
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # print ("AspectRatio", AspectRatio)
    gluPerspective(40, AspectRatio, 0.01, 50)  # Projecao perspectiva

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(userx, 3, userz, lookx, looky, lookz, 0, 1.0, 0.0)


# **********************************************************************
# void DesenhaLadrilho(int corBorda, int corDentro)
# Desenha uma cÃ©lula do piso.
# O ladrilho tem largula 1, centro no (0,0,0) e estÃ¡ sobre o plano XZ
# **********************************************************************
def DesenhaLadrilho():
    global textura
    glBindTexture(GL_TEXTURE_2D, 1001);
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-0.5, 0.0, -0.5)
    glTexCoord2f(1.0, 0.0)

    glVertex3f(-0.5, 0.0, 0.5)
    glTexCoord2f(1.0, 1.0)

    glVertex3f(0.5, 0.0, 0.5)
    glTexCoord2f(1.0, 0.0)

    glVertex3f(0.5, 0.0, -0.5)
    glEnd()

    glColor3f(1, 1, 1)  # desenha a borda da QUAD
    glBegin(GL_LINE_STRIP)
    glNormal3f(0, 1, 0)
    glTexCoord2f(0.0, 0.0)

    glVertex3f(-0.5, 0.0, -0.5)
    glTexCoord2f(0.0, 0.0)

    glVertex3f(-0.5, 0.0, 0.5)
    glTexCoord2f(0.0, 0.0)

    glVertex3f(0.5, 0.0, 0.5)
    glTexCoord2f(1.0, 0.0)

    glVertex3f(0.5, 0.0, -0.5)
    glEnd()

# **********************************************************************
def DesenhaPiso():
    glPushMatrix()
    glTranslated(-20, -1, -10)
    for x in range(-24, 24):
        glPushMatrix()
        for z in range(-12, 12):
            DesenhaLadrilho()
            glTranslated(0, 0, 1)
        glPopMatrix()
        glTranslated(1, 0, 0)
    glPopMatrix()

def desenhap():
    glPushMatrix()
    glTranslated(0, -0.5, -10)
    for x in range(0, 15):
        glPushMatrix()
        for z in range(-12, 12):
            DesenhaParedao()
            glTranslated(0, 0, 1)
        glPopMatrix()
        glTranslated(0, 1, 0)
    glPopMatrix()

def DesenhaParedao():
    glBindTexture(GL_TEXTURE_2D, 1011);

    glBegin(GL_QUADS);
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, 0.5);
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, -0.5, 0.5);
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.5, 0.5);
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.5, 0.5);

    glTexCoord2f(1.0, 0.0); glVertex3f(-0.5, -0.5, -0.5);
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.5, 0.5, -0.5);
    glTexCoord2f(0.0, 1.0); glVertex3f(0.5, 0.5, -0.5);
    glTexCoord2f(0.0, 0.0); glVertex3f(0.5, -0.5, -0.5);

    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.5, -0.5);
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0.5, 0.5);
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, 0.5, 0.5);
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.5, -0.5);

    glTexCoord2f(1.0, 1.0); glVertex3f(-0.5, -0.5, -0.5);
    glTexCoord2f(0.0, 1.0); glVertex3f(0.5, -0.5, -0.5);
    glTexCoord2f(0.0, 0.0); glVertex3f(0.5, -0.5, 0.5);
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.5, -0.5, 0.5);

    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, -0.5, -0.5);
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.5, -0.5);
    glTexCoord2f(0.0, 1.0); glVertex3f(0.5, 0.5, 0.5);
    glTexCoord2f(0.0, 0.0); glVertex3f(0.5, -0.5, 0.5);

    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, -0.5);
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.5, -0.5, 0.5);
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.5, 0.5, 0.5);
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.5, -0.5);
    glEnd();

# **********************************************************************
# display()
# Funcao que exibe os desenhos na tela#
# **********************************************************************
def display():
    global Angulo
    global rota_paralelepipedo
    # Limpa a tela com  a cor de fundo
    print(rota_paralelepipedo)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    DefineLuz()
    PosicUser()
    DesenhaPiso()

    glMatrixMode(GL_MODELVIEW)

    desenhap()
    cilindro()
    desenha_canhao()
    Angulo += 1
    glutSwapBuffers()


# **********************************************************************
# animate()
# Funcao chama enquanto o programa esta ocioso
# Calcula o FPS e numero de interseccao detectadas, junto com outras informacoes
#
# **********************************************************************
# Variaveis Globais
nFrames, TempoTotal, AccumDeltaT = 0, 0, 0
oldTime = time.time()


def animate():
    global nFrames, TempoTotal, AccumDeltaT, oldTime

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1

    if AccumDeltaT > 1.0 / 30:  # fixa a atualizaÃ§Ã£o da tela em 30
        AccumDeltaT = 0
        glutPostRedisplay()


# **********************************************************************
#  keyboard ( key: int, x: int, y: int )
#
# **********************************************************************
ESCAPE = b'\x1b'

def keyboard(*args):
    global rota_paralelepipedo

    global angulo,angulo2
    # print (args)
    # If escape is pressed, kill everything.

    if args[0] == ESCAPE:  # Termina o programa qdo
        os._exit(0)  # a tecla ESC for pressionada

    if args[0] == b' ':
        init()
    if args[0] == b'd':
        if angulo > -60:
            angulo -= 1
    if args[0] == b'a':
        if angulo < 60:
            angulo += 1
    if args[0] == b's':
        if angulo2 < 20:

            angulo2 +=1
    if args[0] == b'w':
        if angulo2 > -60:
            angulo2 -=1

    global posx,posz

    if args[0] == b'i':
        if posx < -2 and rota_paralelepipedo == 0:
            posx +=1
        elif rota_paralelepipedo == 90 and posz >-9:
            posz-=1
        elif rota_paralelepipedo == -90 and posz <12:
            posz+=1
    if args[0] == b'k':
        if posx > -19 and rota_paralelepipedo == 0:
            posx -=1
        elif rota_paralelepipedo == 90 and posz < 12:
            posz +=1
        elif rota_paralelepipedo == -90 and posz > -9:
            posz -=1

    if args[0] == b'2':
        rota_paralelepipedo = 0
    if args[0] == b'1':
        rota_paralelepipedo = 90
    if args[0] == b'3':
        rota_paralelepipedo = -90

    # ForÃ§a o redesenho da tela
    glutPostRedisplay()


# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )
# **********************************************************************

def arrow_keys(a_keys: int, x: int, y: int):
    global userx
    global userz
    global usery
    global lookx
    global looky
    global lookz
    if a_keys == GLUT_KEY_UP:  # Se pressionar UP
        userx += 1
        lookx += 1

    if a_keys == GLUT_KEY_DOWN:  # Se pressionar DOWN
        userx -=1
        lookx -=1
    if a_keys == GLUT_KEY_LEFT:  # Se pressionar LEFT
        userz-=1
        lookz -=1

    if a_keys == GLUT_KEY_RIGHT:  # Se pressionar RIGHT
        userz +=1
        lookz +=1

    glutPostRedisplay()


def mouse(button: int, state: int, x: int, y: int):
    glutPostRedisplay()


def mouseMove(x: int, y: int):
    glutPostRedisplay()


# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowPosition(0, 0)

# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(650, 500)
# Cria a janela na tela, definindo o nome da
# que aparecera na barra de tÃ­tulo da janela.
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("OpenGL 3D")

# executa algumas inicializaÃ§Ãµes
init()

# Define que o tratador de evento para
# o redesenho da tela. A funcao "display"
# serÃ¡ chamada automaticamente quando
# for necessÃ¡rio redesenhar a janela
glutDisplayFunc(display)
glutIdleFunc(animate)

# o redimensionamento da janela. A funcao "reshape"
# Define que o tratador de evento para
# serÃ¡ chamada automaticamente quando
# o usuÃ¡rio alterar o tamanho da janela
glutReshapeFunc(reshape)

# Define que o tratador de evento para
# as teclas. A funcao "keyboard"
# serÃ¡ chamada automaticamente sempre
# o usuÃ¡rio pressionar uma tecla comum
glutKeyboardFunc(keyboard)

# Define que o tratador de evento para
# as teclas especiais(F1, F2,... ALT-A,
# ALT-B, Teclas de Seta, ...).
# A funcao "arrow_keys" serÃ¡ chamada
# automaticamente sempre o usuÃ¡rio
# pressionar uma tecla especial
glutSpecialFunc(arrow_keys)

# glutMouseFunc(mouse)
# glutMotionFunc(mouseMove)


try:
    # inicia o tratamento dos eventos
    glutMainLoop()
except SystemExit:
    pass