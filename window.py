from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from HalfEdge import *

import numpy as np


class GLUTWindow(object):
    def __init__(self, s: Solid) -> None:
        '''建立一个窗口实例'''
        # 初始化与实例绑定的数据
        self.s = s
        self.width = 800                                    # 窗口宽
        self.height = 600                                   # 窗口高
        self.x = 300
        self.y = 200                                        # 窗口位置
        self.PERSPECTIVE = False                            # 是否透视
        self.znear = 0.1                                    # 视锥体参数，决定近裁平面
        self.zfar = 20.0                                    # 视锥体参数
        self.scale = np.array([1.0, 1.0, 1.0])              # 缩放参数
        self.cameraPosition = np.array([0.0, 0.0, 2.0])     # 相机位置
        self.cameraFront = np.array([0.0, 0.0, 0.0])        # 相机朝向
        self.cameraUp = np.array([0.0, 1.0, 0.0])           # 上方向
        self.yaw = -90.0
        self.pitch = 0.0                                    # 欧拉角

        self.left_button_down = False                       # 记录鼠标左键状态
        self.mouse_x = 0.0
        self.mouse_y = 0.0                                  # 记录鼠标位置

        # 按给定值初始化窗口，RGBA颜色模式、双缓存、深度缓存
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(self.x, self.y)
        glutCreateWindow(title='Euler Operator')

        # 初始化画布
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)

        # 注册回调函数
        glutDisplayFunc(self.displayCallback)               # 注册绘图回调函数
        glutReshapeFunc(self.reshapeCallback)               # 注册窗口变形回调函数
        glutMouseFunc(self.mouseClickCallback)              # 注册鼠标点击回调函数
        glutMotionFunc(self.mouseMotionCallback)            # 注册鼠标拖动回调函数
        glutKeyboardFunc(self.keyboardCallback)             # 注册键盘输入回调函数
        # glutMouseWheelFunc(self.mouseWheelCallback)

        
    def displayCallback(self):
        '''渲染回调函数'''
        # 清空颜色深度缓存
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 设置投影
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if self.width > self.height:
            if self.PERSPECTIVE:
                glFrustum(-0.8*self.znear*self.width/self.height, 0.8*self.znear*self.width/self.height, -0.8*self.znear, 0.8*self.znear, self.znear, self.zfar)
            else:
                glOrtho(-0.8*self.width/self.height, 0.8*self.width/self.height, -0.8, 0.8, self.znear, self.zfar)
        else:
            if self.PERSPECTIVE:
                glFrustum(-0.8*self.znear, 0.8*self.znear, -0.8*self.znear*self.height/self.width, 0.8*self.znear*self.height/self.width, self.znear, self.zfar)
            else:
                glOrtho(-0.8, 0.8, -0.8*self.height/self.width, 0.8*self.height/self.width, self.znear, self.zfar)

        # 设置模型视图
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # 设置缩放
        glScale(*self.scale*0.5)

        # 设置视点及视口
        gluLookAt(
            *self.cameraPosition,
            *self.cameraFront,
            *self.cameraUp)

        glViewport(0, 0, self.width, self.height)

        # 绘制
        tess = gluNewTess()
        gluTessCallback(tess, GLU_TESS_BEGIN, self.tessBeginCallback)
        gluTessCallback(tess, GLU_TESS_END, self.tessEndCallback)
        gluTessCallback(tess, GLU_TESS_VERTEX, self.vertexCallback)

        # describe non-convex polygon
        i = 0.05
        
        
        for face in self.s.sfaces:
            # face = self.s.sfaces[0]
            glColor4f(i, i, i, 1.0)
            i += 0.05
            gluTessBeginPolygon(tess, 0)

            gluTessBeginContour(tess)
            he = face.flout.ledge
            v = he.vtx
            # print(he.vtx.vcoord)
            gluTessVertex(tess, he.vtx.vcoord, he.vtx)
            while(he.nxt.vtx != v):
                he = he.nxt
                # print(he.vtx.vcoord)
                gluTessVertex(tess, he.vtx.vcoord, he.vtx)
            gluTessEndContour(tess)

            for loop in face.floops:

                gluTessBeginContour(tess)
                he = loop.ledge
                v = he.vtx
                # print(he.vtx.vcoord)
                gluTessVertex(tess, he.vtx.vcoord, he.vtx)
                while(he.prv.vtx != v):
                    he = he.prv
                    # print(he.vtx.vcoord)
                    gluTessVertex(tess, he.vtx.vcoord, he.vtx)
                gluTessEndContour(tess)

            gluTessEndPolygon(tess)

        # delete tessellator after processing
        gluDeleteTess(tess)

        # 显示绘制内容
        glutSwapBuffers()

    def reshapeCallback(self, width, height):
        '''窗口变形回调函数'''
        # never place calls to glViewport or projection matrix setup in the window reshape handler. 
        self.width = width
        self.height = height
        glutPostRedisplay()

    def mouseClickCallback(self, button, state, x, y):
        '''鼠标点击回调函数'''
        # 记录鼠标点击时的坐标
        self.mouse_x, self.mouse_y = x, y

        # 设置鼠标不同按键的功能，并记录过程
        if button == GLUT_LEFT_BUTTON:
            self.left_button_down = ( state == GLUT_DOWN )
        elif button == GLUT_RIGHT_BUTTON:
            pass
        elif button == GLUT_MIDDLE_BUTTON:
            pass
        elif button == 3 and state == GLUT_UP:
            self.scale += 0.05
            glutPostRedisplay()
        elif button == 4 and state == GLUT_UP:
            self.scale -= 0.05
            glutPostRedisplay()
        
    def mouseMotionCallback(self, x, y):
        '''鼠标拖动回调函数'''
        # 左键拖动时转动视角
        if self.left_button_down:
            # 记录鼠标偏移量
            x_offset = x - self.mouse_x
            y_offset = self.mouse_y - y

            self.mouse_x = x
            self.mouse_y = y

            # 设置灵敏度
            sensitivity = 0.1
            x_offset *= sensitivity
            y_offset *= sensitivity

            self.yaw   += x_offset
            self.pitch += y_offset

            if(self.pitch > 89.0):
                self.pitch = 89.0
            if(self.pitch < -89.0):
                self.pitch = -89.0

            # 根据偏移量更改相机参数以实现视角转动
            self.cameraPosition[0] = np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
            self.cameraPosition[1] = np.sin(np.radians(self.pitch))
            self.cameraPosition[2] = np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))

            self.cameraPosition = -2 * self.cameraPosition / np.linalg.norm(self.cameraPosition)

            glutPostRedisplay()

    def keyboardCallback(self, key, x, y):
        '''键盘输入回调函数'''
        # 输入空格时切换是否透视
        if key == b' ':
            self.PERSPECTIVE = not self.PERSPECTIVE
            glutPostRedisplay()

    def run(self):
        '''进入渲染循环'''
        glutMainLoop()

    def tessBeginCallback(self, which):
        glBegin(which)

    def tessEndCallback(self):
        glEnd()

    def vertexCallback(self, vertex):
        glVertex(*vertex.vcoord)

