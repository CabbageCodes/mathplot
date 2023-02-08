import pygame
import time as Time
from pygame import gfxdraw
import numpy as np
from math import atan2, cos, degrees, radians, sin, exp, sqrt, floor, pi

def isInRect(pos,box,pad = [0,0]):
    return -pad[0] <= pos[0] - box[0] <= box[2] + pad[0] and -pad[1] <= pos[1] - box[1] <= box[3] + pad[1]

def D10(number):
    return floor(number * 10)/10
def D100(number):
    return floor(number * 100)/100
def D1000(number):
    return floor(number * 1000)/1000

def Move(rotation, steps, position):
    xPosition = cos(radians(rotation)) * steps + position[0]
    yPosition = sin(radians(rotation)) * steps + position[1]
    return (xPosition, yPosition)

def DrawThickLine(surface, point1, point2, thickness, color):
    angle = degrees(atan2(point1[1] - point2[1], point1[0] - point2[0]))

    vertices = list()
    vertices.append(Move(angle-90, thickness, point1))
    vertices.append(Move(angle+90, thickness, point1))
    vertices.append(Move(angle+90, thickness, point2))
    vertices.append(Move(angle-90, thickness, point2))

    pygame.gfxdraw.aapolygon(surface, vertices, color)
    pygame.gfxdraw.filled_polygon(surface, vertices, color)

def DrawDisk(surface, point, radius, color):
    gfxdraw.aacircle(surface, floor(0.5+point[0]), floor(0.5+point[1]), radius, color)
    gfxdraw.filled_circle(surface, floor(0.5+point[0]), floor(0.5+point[1]), radius, color)

def GiveTaylorPoly(func,point,termnum):
    x = point
    pstr = str(point)
    stra = str(eval(func.derivlist[0]))
    factorial = 1
    for i in range(1,termnum):
        factorial *= i
        coef = eval(func.derivlist[i])/factorial
        stra += " + " + str(coef) + " * (x-" + pstr + ")**" + str(i)
    return stra

def GiveTaylorText(func,point,termnum):
    x = point

    if point < 0:
        pstr = "("+str(D100(point))+")"
    else:
        pstr = str(D100(point))
    stra = str(D100(eval(func.derivlist[0])))
    factorial = 1
    for i in range(1,termnum):
        factorial *= i
        coef = eval(func.derivlist[i])/factorial
        if x != 0.0:
            stra += " + " + str(D100(coef)) + " * (x-" + pstr + ")"
            if i > 1:
                stra += "^" + str(i)
        else:
            stra += " + " + str(D100(coef)) + " * x"
            if i > 1:
                stra += "^" + str(i)
    return stra

def GiveTaylorList(func,point,termnum):
    lista = [point,[]]
    x = point
    lista[1].append([eval(func.derivlist[0]),0])
    factorial = 1
    for i in range(1,termnum):
        factorial *= i
        coef = eval(func.derivlist[i]) / factorial
        lista[1].append([coef,i])
    return lista

class Poly:
    def __init__(self,params):
        self.center = params[0]
        if self.center < 0:
            self.centertext = "(" + str(D100(self.center)) + ")"
        else:
            self.centertext = str(D100(self.center))
        self.coefs = params[1]
        self.degree = len(self.coefs)
        self.linecolor = [255,255,255]
        self.coefcolor = [255,150,150]
        self.initext = "g(x) = "
        self.clickhitboxes = []

        self.draw_id = 0

        self.coefspace = 0
        self.termspace = 0
        self.plusspace = 0

    def giveformula(self):
        stra = ""
        for k in range(self.degree):
            stra += str(self.coefs[k][0]) + "* (x - " + str(self.center) + ") **" + str(k)
            if k < self.degree - 1:
                stra += " + "
        return stra
    def setparams(self,params):
        self.center = params[0]
        self.coefs = params[1]
        self.degree = len(self.coefs)
        if self.center < 0:
            self.centertext = "(" + str(D100(self.center)) + ")"
        else:
            self.centertext = str(D100(self.center))
    def drawtext(self,env):
        self.clickhitboxes = []
        if self.center == 0.0:
            txt = "x"
            text_term = env.big_font.render(txt,True,[255,255,255])
        else:
            # txt = "(x - " + self.centertext + ")"
            txt = "(x - p)"
            text_term = env.big_font.render(txt,True,[255,255,255])
        term_textsize = env.big_font.size(txt)
        coef_textsize = env.big_font.size("a")
        self.coefspace = coef_textsize[0] + 20
        self.termspace = term_textsize[0] + 20
        self.plusspace = self.coefspace

        initxt = env.big_font.render(self.initext,True,[255,255,255])
        inisize = env.big_font.size(self.initext)
        inioffset = 30 + 20 + inisize[0]
        Xoffset = 30
        Yoffset = 30 + self.draw_id * (env.textY + 10)
        pygame.draw.line(env.screen,self.linecolor,[Xoffset,Yoffset],[Xoffset + 30,Yoffset + env.textY],4)
        text_plus = env.big_font.render("+",True,[255,255,255])
        env.screen.blit(initxt,[Xoffset + 50,Yoffset])
        for k in range(self.degree):
            text_coef = env.big_font.render("a",True,self.coefcolor)
            txt_exp = env.main_font.render(str(k),True,[255,255,255])
            txt_sub = env.main_font.render(str(k),True,self.coefcolor)
            termoffset = Xoffset + inioffset + k * (self.coefspace + self.termspace + self.plusspace) - (k>0)*self.termspace
            env.screen.blit(text_coef,[termoffset,Yoffset])
            self.clickhitboxes.append([termoffset,Yoffset,coef_textsize[0]+15,coef_textsize[1]+15])
            env.screen.blit(txt_sub,[termoffset+coef_textsize[0],Yoffset + env.textY * 0.5])
            if k > 0:
                DrawDisk(env.screen,[termoffset+self.coefspace,Yoffset + env.textY/2],2,[255,255,255])
                env.screen.blit(text_term,[termoffset + self.coefspace+10,Yoffset])
            if k > 1:
                env.screen.blit(txt_exp,[termoffset + self.coefspace + term_textsize[0] + 10,Yoffset - 5])
            if k < self.degree - 1:
                if k == 0:
                    env.screen.blit(text_plus,[termoffset + self.coefspace,Yoffset])
                else:
                    env.screen.blit(text_plus,[termoffset + self.coefspace + term_textsize[0] + 20,Yoffset])

class PlotEnv:
    def __init__(self,dims,bgcolor):
        self.dims = dims
        self.xdim = dims[0]
        # self.xmidpoint = floor(self.xdim/2)
        self.ydim = dims[1]
        # self.ymidpoint = floor(self.ydim/2)
        self.bgcolor = bgcolor
        pygame.init()
        self.main_font = pygame.font.Font('computer-modern\cmunorm.ttf',20)
        self.big_font = pygame.font.Font('computer-modern\cmunorm.ttf',30)
        pygame.display.set_caption('My function plotter')
        self.screen = pygame.display.set_mode(self.dims) #,pygame.RESIZABLE)
        self.funcs = []
        self.taylors = []
        self.plotrect = [20,160,self.xdim-40,self.ydim-180]
        self.plotlimitX = [-10,10]
        self.plotlimitY = [-10,10]
        self.initial_limits = [0,0]
        self.drawaxes = 1
        self.axescolor = [255,255,255]
        self.axesthickness = 1
        self.sliders = []

        self.redraw = 1

        self.pointnum = 5000
        self.pointnum = 5000

        self.old_origin = [0,0]

        self.draw_grid = 1
        self.grid_size = 1
        self.grid_color = [50,50,50]

        self.typing_mode = 0
        self.add_text = ""
        self.text_target_func = 0

        self.graph_colors = [
            [103,167,214],
            [166,241,170],
            [227,94,177],
            [249,224,128],
            [133,215,228],
            [176,137,224],
            [236,148,125],
            [198,211,150]
        ]
        self.total_graphs = 0
        self.graph_names = [
            "f",
            "g",
            "h",
            "u",
            "v",
            "a",
            "b",
            "c"
        ]

        inisize = self.big_font.size("f(x) = ")
        self.textY = inisize[1]

    def add_func(self,func1):
        func1.draw_id = len(self.funcs)
        func1.set_hitbox(self)
        func1.fmenu.setpos([func1.hitbox[0],func1.hitbox[1]+80 + (10 + self.textY) * func1.draw_id])
        func1.fmenu.setbuttons(self)
        func1.setpoints(self.give_range_long())
        func1.setgraph(self)
        self.funcs.append(func1)
        self.set_graph_limits()
        self.redraw = 1

        func1.setgraphparam(self.graph_colors[self.total_graphs],1)
        func1.initext = self.graph_names[self.total_graphs] + "(x) = "
        self.total_graphs += 1

    def add_taylor(self,tay1):
        tay1.func.draw_id = len(self.taylors)
        tay1.taylorpoly.draw_id = len(self.taylors)
        tay1.func.set_hitbox(self)
        tay1.func.fmenu.setpos([tay1.func.hitbox[0],tay1.func.hitbox[1] + 80])
        tay1.func.fmenu.setbuttons(self)
        tay1.func.setpoints(self.give_range_long())
        tay1.func.setgraph(self)
        # tay1.func.draw_id = len(self.taylors)
        self.taylors.append(tay1)
        self.set_graph_limits()
        tay1.update_point(tay1.slider.pos,self)
        self.redraw = 1

        tay1.func.setgraphparam(self.graph_colors[self.total_graphs],1)
        tay1.taylorpoly.linecolor = tay1.func.color
        tay1.taylorpoly.initext = self.graph_names[self.total_graphs] + "(x) = "
        self.total_graphs += 1

    def set_plot_limits(self,limX,limY):
        self.plotlimitX = limX
        self.plotlimitY = limY
        d = self.plotlimitX[1] - self.plotlimitX[0]
        self.initial_limits = [limX[0] - 2*d,limX[1] + 2*d]

        self.old_origin = self.point_to_screen([0,0])

    def translate_pos(self,pos,old_pos,old_lims):
        self.plotlimitX[0] = old_lims[0] - (pos[0]-old_pos[0]) * (self.plotlimitX[1] - self.plotlimitX[0])/self.plotrect[2]
        self.plotlimitX[1] = self.plotlimitX[0] + old_lims[1] - old_lims[0]

        self.plotlimitY[0] = old_lims[2] + (pos[1]-old_pos[1]) * (self.plotlimitY[1] - self.plotlimitY[0])/self.plotrect[3]
        self.plotlimitY[1] = self.plotlimitY[0] + old_lims[3] - old_lims[2]
        self.set_graph_limits()

        new_origin = self.point_to_screen([0,0])

        for f in self.funcs:
            if f.type == "static":
                for i in range(0,self.pointnum):
                    f.graph[i][1] += new_origin[1] - self.old_origin[1]
                    f.graph[i][0] += new_origin[0] - self.old_origin[0]
            else:
                f.reset_graph(self)
        for t in self.taylors:
            if t.func.type == "static":
                for i in range(0,self.pointnum):
                    t.func.graph[i][1] += new_origin[1] - self.old_origin[1]
                    t.func.graph[i][0] += new_origin[0] - self.old_origin[0]
            else:
                t.func.reset_graph(self)
        self.old_origin = new_origin




    def give_range(self):
        return np.linspace(self.plotlimitX[0],self.plotlimitX[1],1000)
    def give_range_long(self):
        return np.linspace(self.initial_limits[0],self.initial_limits[1],self.pointnum)
    def add_slider(self,slider1):
        self.sliders.append(slider1)
    def setallpoints(self):
        for f in self.funcs:
            f.setpoints(self.give_range_long())
            f.setgraph(self)

        for t in self.taylors:
            t.func.setpoints(self.give_range_long())
            t.func.setgraph(self)
        self.set_graph_limits()
    def set_graph_limits(self):
        a = floor(self.pointnum * (self.plotlimitX[0] - self.initial_limits[0])/(self.initial_limits[1] - self.initial_limits[0]))
        b = floor(self.pointnum * (self.plotlimitX[1] - self.initial_limits[0])/(self.initial_limits[1] - self.initial_limits[0]))
        for f in self.funcs:
            f.graphrange[0] = a
            f.graphrange[1] = b
        for t in self.taylors:
            t.func.graphrange[0] = a
            t.func.graphrange[1] = b
    def drawme(self):
        self.screen.fill(self.bgcolor)
        if self.draw_grid:
            # horizontal
            y_coord = floor(self.plotlimitY[0])
            while y_coord <= self.plotlimitY[1]:
                y_screen = self.point_to_screen([0,y_coord])[1]
                pygame.draw.line(self.screen,self.grid_color,[self.plotrect[0],y_screen],[self.plotrect[0]+self.plotrect[2],y_screen])
                y_coord += 1
            # vertical
            x_coord = floor(self.plotlimitX[0])
            while x_coord <= self.plotlimitX[1]:
                x_screen = self.point_to_screen([x_coord,0])[0]
                pygame.draw.line(self.screen,self.grid_color,[x_screen,self.plotrect[1]],[x_screen,self.plotrect[1] + self.plotrect[3]])
                x_coord += 1
        if self.drawaxes:
            x1 = self.point_to_screen([self.plotlimitX[0],0])
            # x1[0] += self.axespadding[0]
            x2 = self.point_to_screen([self.plotlimitX[1],0])
            x3 = [x2[0] - 20,x2[1] + 10]
            x4 = [x2[0] - 20,x2[1] - 10]
            # x2[0] -= self.axespadding[0]
            pygame.draw.line(self.screen,self.axescolor,x1,x2,self.axesthickness)
            pygame.draw.line(self.screen,self.axescolor,x2,x3,self.axesthickness)
            pygame.draw.line(self.screen,self.axescolor,x2,x4,self.axesthickness)

            y1 = self.point_to_screen([0,self.plotlimitY[0]])
            # y1[1] -= self.axespadding[1]
            y2 = self.point_to_screen([0,self.plotlimitY[1]])
            y3 = [y2[0] - 10,y2[1] + 20]
            y4 = [y2[0] + 10,y2[1] + 20]
            # y2[1] += self.axespadding[1]
            pygame.draw.line(self.screen,self.axescolor,y1,y2,self.axesthickness)
            pygame.draw.line(self.screen,self.axescolor,y3,y2,self.axesthickness)
            pygame.draw.line(self.screen,self.axescolor,y4,y2,self.axesthickness)


        for f in self.funcs:
            f.plot(self)
            if f.do_drawtext:
                f.drawtext(self)


        for t in self.taylors:
            t.plot(self)
            t.taylorpoly.drawtext(self)

        for s in self.sliders:
            s.draw(self)
            if s.do_drawtext:
                s.drawtext(self)

        for t in self.taylors:
            t.slider.draw(self)
            if t.slider.do_drawtext:
                t.slider.drawtext(self)

        for f in self.funcs:
            if f.fmenu.visible:
                f.fmenu.draw(self)

        for t in self.taylors:
            if t.func.fmenu.visible:
                t.func.fmenu.draw(self)

        for t in self.taylors:
            if t.adjust_coefs:
                t.coefslider.draw(self)

        if self.typing_mode:
            helptxt = self.big_font.render("Type function:",True,[255,255,255])
            helptxt_size = self.big_font.size("Type function:")
            addtxt = self.big_font.render(self.add_text,True,[255,255,255])
            addtxt_size = self.big_font.size(self.add_text)

            pygame.draw.rect(self.screen,self.bgcolor,[100,100,helptxt_size[0],helptxt_size[1]+10])
            pygame.draw.rect(self.screen,self.bgcolor,[100,100+helptxt_size[1]+10,addtxt_size[0],addtxt_size[1]])
            self.screen.blit(helptxt,[100,100])
            self.screen.blit(addtxt,[100,100+helptxt_size[1]+10])

    def erase_taylor(self,taylor):
        if taylor in self.taylors:
            self.taylors.remove(taylor)
            self.redraw = 1
            for f in self.funcs:
                f.taylor_targets.remove(taylor)
            self.total_graphs += -1



    def point_to_screen(self,point):
        xcoord = self.plotrect[0] + self.plotrect[2]*(point[0] - self.plotlimitX[0])/(self.plotlimitX[1] - self.plotlimitX[0])
        ycoord = self.plotrect[1] + self.plotrect[3] - self.plotrect[3] * (point[1] - self.plotlimitY[0])/(self.plotlimitY[1] - self.plotlimitY[0])
        return [xcoord,ycoord]
    def screen_to_point(self,spoint):
        xcoord = self.plotlimitX[0] + (self.plotlimitX[1]-self.plotlimitX[0])*(spoint[0] - self.plotrect[0])/self.plotrect[2]
        ycoord = self.plotlimitY[0] + (self.plotlimitY[1]-self.plotlimitY[0])*(self.plotrect[1] + self.plotrect[3] - spoint[1])/self.plotrect[3]
        if xcoord > self.plotlimitX[1]:
            xcoord = self.plotlimitX[1]
        elif xcoord < self.plotlimitX[0]:
            xcoord = self.plotlimitX[0]
        return [xcoord,ycoord]


class MathFunc:
    def __init__(self,formula,draw_id):
        self.formula = formula.replace("^","**")
        self.color = [255,255,255]
        self.thickness = 2
        self.points = [0,1]
        self.graph = []
        self.derivlist = []
        self.evalmax = 1000000
        self.evalmin = -1000000
        self.snaps = []
        self.do_drawtext = 0
        self.drawtextmode = "up right"
        self.text = self.formula
        self.initext = "f(x) = "
        self.draw_id = draw_id
        self.hitbox = [0,0,0,0]
        self.graphrange = [0,0]

        self.type = "static"

        self.fmenu = FMenu([])

        self.has_taylor = 0
        self.taylor_targets = []

    def add_button(self,button,env):
        self.fmenu.buttons.append(button)
        self.fmenu.setbuttons(env)

    def set_hitbox(self,env):
        textsize = env.big_font.size(self.initext + self.formula)
        if self.drawtextmode == "up right":
            self.hitbox = [env.xdim - 20 - textsize[0] - 50,20 + (10+textsize[1]) * (self.draw_id),60,60]
        elif self.drawtextmode == "up left taylor":
            self.hitbox = [20,20 + (10+textsize[1]) * (self.draw_id),60,60]

    def drawtext(self,env):
        mystr = self.initext + self.text
        text1 = env.big_font.render(mystr,True,[255,255,255])
        textsize = env.big_font.size(mystr)

        if self.drawtextmode == "up right":
            env.screen.blit(text1,[env.xdim - 10 - textsize[0], 20])
            pygame.draw.line(env.screen,self.color,[env.xdim - 10 - textsize[0] - 50, 20],[env.xdim - 10 - textsize[0] - 20, 20 + textsize[1]],4)

        elif self.drawtextmode == "up left":
            pygame.draw.line(env.screen,self.color,[30, 20 + textsize[1]/2],[60, 20 + textsize[1]/2],4)
            env.screen.blit(text1,[80, 20])
        elif self.drawtextmode == "up right poly fixed":
            degree = self.text.count("x")
        
    def setfunc(self,formula,env):
        self.formula = formula.replace("^","**")
        if self.formula == "exp(x)":
            self.setderivlist(["exp(x)","exp(x)","exp(x)","exp(x)","exp(x)","exp(x)"])
        elif self.formula == "cos(x)":
            self.setderivlist(["cos(x)","-sin(x)","-cos(x)","sin(x)","cos(x)"])
        self.set_hitbox(env)
        if self.type == "static":
            self.setgraph(env)
        else:
            self.reset_graph(env)
    def setderivlist(self,derivlist):
        self.derivlist = derivlist
    def evaluate(self,point):
        x = point
        if x > self.evalmax:
            x = self.evalmax
        elif x < self.evalmin:
            x = self.evalmin
        return eval(self.formula)
    def setgraphparam(self,color,thickness):
        self.color = color
        self.thickness = thickness
    def setpoints(self,points):
        self.points = points
    def setgraph(self,env):
        self.graph = []
        for p in self.points:
            self.graph.append(env.point_to_screen([p,self.evaluate(p)]))
    def reset_graph(self,env):
        for k in range(max(0,self.graphrange[0]),min(self.graphrange[1]+1,env.pointnum-1)):
            self.graph[k] = env.point_to_screen([self.points[k],self.evaluate(self.points[k])])

    # def translate_graph(self):

    def plot(self,env):
        # pygame.draw.aalines(env.screen,self.color,0,self.graph)
        for p in range(max(0,self.graphrange[0]),min(env.pointnum-2,self.graphrange[1])):
            p1 = self.graph[p]
            p2 = self.graph[p+1]
            # pygame.gfxdraw.line(env.screen,p1[0],p1[1],p2[0],p2[1],self.color,self.thickness)
            if 0 <= p1[1] - env.plotrect[1] <= env.plotrect[3] and 0 <= p2[1] - env.plotrect[1] <= env.plotrect[3]:
                # DrawThickLine(env.screen,p1,p2,self.thickness,self.color)
                pygame.draw.line(env.screen,self.color,p1,p2,self.thickness+2)

class GraphSlider:
    def __init__(self,func):
        self.func = func
        self.pos = 0
        self.snapradius = 0.1
        self.radiusouter = 10
        self.radiusinner = 6
        self.colorouter = [240,60,160]
        self.colorinner = [255,255,255]
        self.text = "p = "
        self.do_drawtext = 1
    def snap(self):
        for snap in self.func.snaps:
            if abs(self.pos - snap) < self.snapradius:
                self.pos = snap
    def drawtext(self,env):
        point = env.point_to_screen([self.pos,0])
        mystr = self.text + str(D1000(self.pos))
        if D100(self.pos) != self.pos:
            mystr += "..."
        text1 = env.main_font.render(mystr,True,[255,255,255])
        textsize = env.main_font.size(mystr)
        env.screen.blit(text1,[point[0] + 15, point[1] - textsize[1] - 4])
    def draw(self,env):
        point1 = env.point_to_screen([self.pos,self.func.evaluate(self.pos)])
        point2 = env.point_to_screen([self.pos,0])

        # DrawDisk(env.screen,point,self.radiusouter,self.colorouter)


        f1 = 0
        if isInRect(point1,env.plotrect):
            f1 = 1
            DrawDisk(env.screen,point1,self.radiusinner,self.colorinner)
        elif point1[1] < env.plotrect[1]:
            point1[1] = env.plotrect[1]
        elif point1[1] > env.plotrect[1] + env.plotrect[3]:
            point1[1] = env.plotrect[1] + env.plotrect[3]

        if isInRect(point2,env.plotrect):
            f1 = 1
            DrawDisk(env.screen,point2,self.radiusinner,self.colorinner)
        elif point2[1] < env.plotrect[1]:
            point2[1] = env.plotrect[1]
        elif point2[1] > env.plotrect[1] + env.plotrect[3]:
            point2[1] = env.plotrect[1] + env.plotrect[3]

        if f1:
            pygame.draw.line(env.screen,self.colorinner,point1,point2,2)


    def isontop(self,env,spoint):
        point = env.point_to_screen([self.pos,self.func.evaluate(self.pos)])
        point2 = env.point_to_screen([self.pos,0])
        return (point[0]-spoint[0])**2+(point[1]-spoint[1])**2 < (self.radiusouter+5)**2 or (point2[0]-spoint[0])**2+(point2[1]-spoint[1])**2 < (self.radiusouter+5)**2

class Slider:
    def __init__(self,poly):
        self.visible = 0
        self.color = [100,100,100]
        self.range = [-3,3]
        self.screenpos = [0,0]
        self.width = 40
        self.length = 200
        self.poly = poly
        self.coef_pick = 0

        self.Sval = 0
        self.Srect = [0,0,0,0]
        self.Scolor = [255,255,255]
        self.set_Spos()
    def snap(self):
        for i in range(-10,10):
            if abs(self.Sval * 2 - i) < 0.2:
                self.Sval = i/2
    def set_Spos(self):
        self.Srect[1] = self.screenpos[1] + self.length - (self.length) * (self.Sval - self.range[0])/(self.range[1] - self.range[0]) - 4
        self.Srect[0] = self.screenpos[0]
        self.Srect[2] = self.width
        self.Srect[3] = 8
    def screen_to_val(self,point):
        val = self.range[1] + (self.range[0] - self.range[1]) * (point[1] - self.screenpos[1])/(self.length)
        if val > self.range[1]:
            val = self.range[1]
        elif val < self.range[0]:
            val = self.range[0]
        return val
    def draw(self,env):
        pygame.draw.rect(env.screen,[0,0,0],[self.screenpos[0],self.screenpos[1],self.width,self.length])
        pygame.draw.rect(env.screen,self.color,[self.screenpos[0]+self.width/2 - 4,self.screenpos[1],8,self.length])

        pygame.draw.rect(env.screen,self.Scolor,self.Srect)

        fullsize = env.big_font.size("a0 = " + str(D1000(self.poly.coefs[self.coef_pick][0])))
        coef_textsize = env.big_font.size("a")

        pygame.draw.rect(env.screen,[0,0,0],[self.Srect[0] + self.Srect[2] + 20, self.Srect[1] - env.textY/2 + 5,fullsize[0],fullsize[1] - 10])

        text1 = env.big_font.render("a",True,self.poly.coefcolor)
        # coef_textsize = env.big_font.size("a")
        text2 = env.main_font.render(str(self.coef_pick),True,self.poly.coefcolor)
        env.screen.blit(text1,[self.Srect[0] + self.Srect[2] + 20, self.Srect[1]  - env.textY/2])
        env.screen.blit(text2,[self.Srect[0] + self.Srect[2] + 20 + coef_textsize[0], self.Srect[1]])
        str1 = " = " + str(D1000(self.poly.coefs[self.coef_pick][0]))
        text3 = env.big_font.render(str1,True,[255,255,255])
        env.screen.blit(text3,[self.Srect[0] + self.Srect[2] + 60, self.Srect[1] - env.textY/2])


class FMenu:
    def __init__(self,buttons):
        self.buttons = buttons
        self.visible = 0
        self.menupos = [0,0]

    def setpos(self,pos):
        self.menupos = pos

    def setbuttons(self,env):
        bpos = self.menupos[1]
        for b in self.buttons:
            b.pos = [self.menupos[0],bpos]
            b.rect = [self.menupos[0],bpos,b.rect[2],b.rect[3]]
            bpos += b.rect[3] + 5
            b.set_rect_dims(env)

    def draw(self,env):
        for b in self.buttons:
            b.draw(env)

class Button:
    def __init__(self,type,tied_objects,text = "", rect = [0,0,0,0]):
        self.type = type
        self.tied_objects = tied_objects
        self.text = text
        self.pos = [0,0]
        self.rect = rect
        self.color = [120,120,120]
        self.textcolor = [255,255,255]
    def set_rect_dims(self,env):
        textsize = env.main_font.size(self.text)
        self.rect[2] = textsize[0] + 15
        self.rect[3] = textsize[1] + 5

    def draw(self,env):
        pygame.draw.rect(env.screen,self.color,self.rect)
        text1 = env.main_font.render(self.text,True,self.textcolor)
        env.screen.blit(text1,[self.pos[0]+5,self.pos[1]+5])

    def get_pressed(self):
        if self.type == "add taylor":
            # newtaylor = Poly(GiveTaylorList(self.tied_objects[0],0,3))
            newtaylor = Taylor(self.tied_objects[0],3,self.tied_objects[1])
            self.tied_objects[1].add_taylor(newtaylor)
            self.tied_objects[0].has_taylor = 1
            self.tied_objects[0].taylor_targets.append(newtaylor)

        elif self.type == "change func":
            self.tied_objects[1].typing_mode = 1
            self.tied_objects[1].add_text = ""
            self.tied_objects[1].text_target_func = self.tied_objects[0]

        elif self.type == "add degree":
            if self.tied_objects[0].degree < len(self.tied_objects[0].origfunc.derivlist):
                self.tied_objects[0].degree += 1
            self.tied_objects[0].update_point(self.tied_objects[0].center,self.tied_objects[1])

        elif self.type == "lower degree":
            if self.tied_objects[0].degree > 1:
                self.tied_objects[0].degree += -1
            self.tied_objects[0].update_point(self.tied_objects[0].center,self.tied_objects[1])

        elif self.type == "delete taylor":
            self.tied_objects[1].erase_taylor(self.tied_objects[0])

class Taylor:
    def __init__(self,origfunc,degree,env):
        self.origfunc = origfunc
        self.degree = degree
        self.center = 0
        self.taylorpoly = Poly(GiveTaylorList(origfunc,self.center,degree))


        self.func = MathFunc("x",0)
        self.func.type = "non-static"
        self.func.drawtextmode = "up left taylor"
        self.func.add_button(Button("add degree",[self,env],text = "Add term"),env)
        self.func.add_button(Button("lower degree",[self,env],text = "Remove term"),env)
        self.func.add_button(Button("delete taylor",[self,env],text = "Delete"),env)
        self.func.formula = self.taylorpoly.giveformula()

        self.func.setgraphparam([255,255,255],1)

        self.taylorpoly.linecolor = self.func.color

        self.coefslider = Slider(self.taylorpoly)

        self.coefslider.screenpos[1] = 120
        self.coefslider.coef_pick = -1

        self.adjust_coefs = 0

        if len(self.origfunc.taylor_targets) == 0:
            self.slider = GraphSlider(origfunc)
        else:
            self.slider = self.origfunc.taylor_targets[0].slider

    def plot(self,env):
        self.func.plot(env)

    def update_point(self,newp,env):
        self.center = newp
        self.taylorpoly.setparams(GiveTaylorList(self.origfunc,self.center,self.degree))
        self.func.setfunc(self.taylorpoly.giveformula(),env)
        env.redraw = 1

        if self.adjust_coefs:
            self.coefslider.Sval = self.taylorpoly.coefs[self.coefslider.coef_pick][0]
            self.coefslider.set_Spos()