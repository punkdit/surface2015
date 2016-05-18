#!/usr/bin/env python

import sys
import os

from math import *
from random import *

from pyx import canvas, path, deco, trafo, style, text, color, unit, epsfile, deformer, bitmap

from PIL import Image

north = [text.halign.boxcenter, text.valign.top]
northeast = [text.halign.boxright, text.valign.top]
northwest = [text.halign.boxleft, text.valign.top]
south = [text.halign.boxcenter, text.valign.bottom]
southeast = [text.halign.boxright, text.valign.bottom]
southwest = [text.halign.boxleft, text.valign.bottom]
east = [text.halign.boxright, text.valign.middle]
west = [text.halign.boxleft, text.valign.middle]
center = [text.halign.boxcenter, text.valign.middle]


st_dashed = [style.linestyle.dashed]
st_dotted = [style.linestyle.dotted]

st_Thick = [style.linewidth.Thick]


text.set(mode="latex")
text.set(docopt="10pt")
text.preamble(r'\usepackage{amsmath,amsfonts,amssymb}')
#text.preamble(r"\def\I{\mathbb{I}}")
text.preamble(r"\def\ket #1{|#1\rangle}")


rgb = color.rgb
rgbfromhexstring = color.rgbfromhexstring

red, green, blue, yellow, orange = (
    rgbfromhexstring("#d00000"),
    rgbfromhexstring("#006000"),
    rgb.blue, 
    rgb(0.75, 0.75, 0),
    rgb(0.75, 0.55, 0),
    )

blue = rgb(0., 0., 0.8)
pale_blue = rgb(0.7, 0.7, 1.0)
pink = rgb(1., 0.4, 0.4)
white = rgb(1., 1., 1.)
grey = rgb(0.8, 0.8, 0.8)

brown = rgbfromhexstring("#AA6C39"),

light_shade = rgb(0.85, 0.65, 0.1)

#shade = brown
#shade = orange
shade = grey



g_curve = [green, style.linewidth.THick]

st_tau = [style.linewidth.Thick, red, style.linecap.round]
#st_vac = [style.linewidth.thick, red]+st_dotted


def anyon(x, y, r=0.07):
    c.fill(path.circle(x, y, r), [white])
    c.stroke(path.circle(x, y, r), [style.linewidth.thick])


N = 20

def dopath(ps, extra=[], fill=[], closepath=False, smooth=0.0):
    if not ps:
        print "dopath: empty"
        return
    ps = [path.moveto(*ps[0])]+[path.lineto(*p) for p in ps[1:]]
    if closepath:
        ps.append(path.closepath())
    p = path.path(*ps)
    extra = list(extra)
    if smooth:
        extra.append(deformer.smoothed(smooth))
    if fill:
        c.fill(p, extra+fill)
    c.stroke(p, extra)


def ellipse(x0, y0, rx, ry, extra=[], fill=[]):
    ps = []
    for i in range(N):
        theta = 2*pi*i / (N-1)
        ps.append((x0+rx*sin(theta), y0+ry*cos(theta)))
    dopath(ps, extra, fill)



stack = []
def push():
    global c
    stack.append(c)
    c = canvas.canvas()

def pop(*args):
    global c
    c1 = stack.pop()
    c1.insert(c, *args)
    c = c1



class Turtle(object):
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        self.ps = [(x, y)]
        self.pen = True

    def penup(self):
        self.pen = False
        self.ps = []
        return self

    def pendown(self):
        self.pen = True
        self.ps = [(self.x, self.y)]
        return self

    def fwd(self, d):
        self.x += d*sin(self.theta)
        self.y += d*cos(self.theta)
        if self.pen:
            self.ps.append((self.x, self.y))
        return self

    def reverse(self, d):
        self.fwd(-d)
        return self

    def right(self, dtheta, r=0.):
        theta = self.theta
        self.theta += dtheta
        if r==0.:
            return self
        N = 20
        x, y = self.x, self.y
        x0 = x - r*sin(theta-pi/2)
        y0 = y - r*cos(theta-pi/2)
        for i in range(N):
            theta += (1./(N))*dtheta
            x = x0 - r*sin(theta+pi/2)
            y = y0 - r*cos(theta+pi/2)
            if self.pen:
                self.ps.append((x, y))
        self.x = x
        self.y = y
        return self

    def left(self, dtheta, r=0.):
        self.right(-dtheta, -r)
        return self

    def stroke(self, extra=[], fill=[], closepath=False):
        dopath(self.ps, extra, fill, closepath, smooth=0.)
        return self



def occluded(ps0, pss, radius=0.2):

    ps = []

    flag = True
    for i, p in enumerate(ps0):

        flag1 = True
        x, y = p
        for ps1 in pss:
            x1, y1 = ps1[i]
            if abs(x1-x)<radius:
                flag1 = False
        #print int(flag1),

        if flag1 == flag:
            ps.append(p)
        elif ps:
            yield flag, ps
            ps = [p]
        flag = flag1

    if ps:
        yield flag, ps


def draw(ps0, pss, descs, radius=0.25):

    descs = list(descs)
    desc = descs.pop(0) if descs else True
    _ps = []
    for flag, ps in occluded(ps0, pss, radius):
        #print '/',
        if flag or desc:
            _ps += ps
        else:
            yield _ps
            _ps = []
        if not flag:
            desc = descs.pop(0) if descs else True
    if _ps:
        yield _ps


def bump(x0, alpha=0.4):
    x1 = 0.5 - 0.5*cos(pi*x0)
    x = alpha*x0 + (1-alpha)*x1
    return x

def timeslice(x, y, transparency=0., label="", W=3):
    dopath([(-1.1, y0), (-0.1, y1), (W + .2, y1), (W -0.8, y0)],
        fill=[shade, color.transparency(0.3)],
        extra=[trafo.translate(x, y)], closepath=True)
    if label:
        c.text(W+0.2, 0., label, west+[trafo.translate(x, y)])



#############################################################################
#
#


c = canvas.canvas()

w = 2.0
h = 2.0

ns = [2, 3, 3, 2]


for i in range(len(ns)):

    n = ns[i]
    x0 = i*w
    x1 = (i+1)*w
    for j0 in range(n):
        y0 = j0*h - h*(n-1)/2.
        c.fill(path.circle(x0, y0, 0.1))
    
        if i==len(ns)-1:
            continue

        n1 = ns[i+1]
        for j1 in range(n1):
            y1 = j1*h - h*(n1-1)/2.

            c.stroke(path.line(x0, y0, x1, y1))



c.writePDFfile("pic-trellis.pdf")


#############################################################################
#
#

seed(0)


w = 2.0
h = 2.0

ns = [2, 3, 3, 2]


weights = {}
weights = {
    (0, 1, 1): 2, (2, 2, 0): 4, (2, 1, 1): 4, (2, 1, 0): 0, (0, 0, 2): 2, (1, 1, 0): 2, (0, 1, 2): 2, (2, 0, 1): 4, (0, 0, 1): 3, (1, 2, 1): 3, (1, 0, 1): 1, (1, 1, 1): 4, (1, 0, 0): 3, (1, 2, 0): 1, (0, 0, 0): 4, (2, 0, 0): 1, (1, 2, 2): 3, (0, 1, 0): 1, (1, 1, 2): 2, (1, 0, 2): 2, (2, 2, 1): 1}

mweights = {
    (0,0):0, (0,1):0,
    (1,0):1, (1,1):2, (1, 2):2,
    (2,0):3, (2,1):2, (2, 2):3,
    (3,0):2, (3,1):4,
}

#for i in range(1, len(ns)):
#    n0 = ns[i-1]
#    n1 = ns[i]
#    for j0 in range(n0):
#        w = weights[i-1, j0, j1]


for frame in range(5):

  c = canvas.canvas()
  for i in range(len(ns)):

    n = ns[i]
    x0 = i*w
    x1 = (i+1)*w

    if i+1 == frame:
        c.stroke(path.line(x0, -1.2*h, x0, 1.2*h), st_dashed)

    for j0 in range(n):
        y0 = j0*h - h*(n-1)/2.

        c.fill(path.circle(x0, y0, 0.1))
    
        if i==len(ns)-1:
            continue

        n1 = ns[i+1]
        for j1 in range(n1):
            y1 = j1*h - h*(n1-1)/2.

            alpha = 0.95
            x11 = (1-alpha)*x0 + alpha*x1
            y11 = (1-alpha)*y0 + alpha*y1
            c.stroke(path.line(x0, y0, x11, y11), [deco.earrow()])

            alpha = 0.25
            x = (1-alpha)*x0 + alpha*x1
            y = (1-alpha)*y0 + alpha*y1
            #weight = randint(0, 4)
            #weights[i, j0, j1] = weight

            R = 0.17
            c.fill(path.circle(x, y, R), [white])
            c.stroke(path.circle(x, y, R) )
            c.text(x, y, "$%d$"%weights[i, j0, j1], center)


  for i in range(len(ns)):

    n = ns[i]
    x0 = i*w
    x1 = (i+1)*w

    for j0 in range(n):
        y0 = j0*h - h*(n-1)/2.

        if i < frame:
            R = 0.34
            p = path.rect(x0-0.5*R, y0-0.5*R, R, R)
            c.fill(p, [white])
            c.stroke(p)
            c.text(x0, y0, "$%d$"%mweights[i, j0], center)


  c.writePDFfile("pic-minpath-%d.pdf"%frame)



#############################################################################
#
#

c = canvas.canvas()


w = 2.0
h = 1.0

a = {0:1, 1:1}
coords = {}

idx = 0
for i in range(5):
    for j in range(2):
        x = j*w
        y = i*h + 0.5*j*h
        coords[idx] = (x, y)
        idx += 1

def conv(alpha, (x0, y0), (x1, y1)):
    return (1.0-alpha)*x0+alpha*x1, (1.0-alpha)*y0+alpha*y1


for idx in range(8):
    x0, y0 = coords[idx]
    x1, y1 = coords[idx+1]
    x2, y2 = coords[idx+2]
    x1, y1 = conv(0.85, (x0, y0), (x1, y1))
    x2, y2 = conv(0.70, (x0, y0), (x2, y2))

    if idx>0:
        c.stroke(path.line(x0, y0, x1, y1), [deco.earrow()])
    c.stroke(path.line(x0, y0, x2, y2), [deco.earrow()])

    
for idx in range(8):
    x, y = coords[idx]

    p = path.circle(x, y, 0.3)
    c.fill(p, [white])
    c.stroke(p)

    value = a.get(idx)
    if value is None:
        value = a[idx-1] + a[idx-2]
    a[idx] = value
    c.text(x, y, "$%d$"%value, center)

c.text(0.5*w, 4.3*h, "...", center)



c.writePDFfile("pic-fibonacci.pdf")



