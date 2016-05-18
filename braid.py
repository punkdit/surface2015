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









# hole spacing
w = 1.0
W = 3*w

# total hight
H = 2.8

my = 0.25
x0, y0 = 0.3*W, 0.3*H
x1, y1 = x0+0.3*W, y0+my*0.3*W
y0, y1 = -.3, .3

N = 100

def cos_up(theta): # 0 -> 1 -> 0
    return 0.5 - 0.5*cos(theta)

def cos_dn(theta): # 0 -> -1 -> 0
    return -cos_up(theta)


c = canvas.canvas()
for frame in range(2):

    X = 5.5*w*frame

    ps0 = []
    ps1 = []
    ps2 = []
    for i in range(N+1):
        r = 1.*i/N
        y = r*H
        #r = bump(r)
    
        x = 2*w*cos_up(pi*r)
        ps0.append((x, y))
    
        if frame == 0:
            x = w + cos_dn(2*pi*r)
        else:
            x = w + cos_up(2*pi*r)
        ps1.append((x, y))
    
        x = 2*w + 2*w*cos_dn(pi*r)
        ps2.append((x, y))
    
    tr = [trafo.translate(X, 0.)]
    
#    if frame == 0:
#        c.text(-4.0*w, 0.5*H, r"$\sigma_i\sigma_{i+1}\sigma_i =$", tr)
#    else:
#        c.text(-3.0*w, 0.5*H, r"$=$", tr)
#        c.text(+4.5*w, 0.5*H, r"$=\sigma_{i+1}\sigma_i\sigma_{i+1}$", tr)
    if frame:
        c.text(-2.0*w, 0.5*H, r"$=$", tr)

#    #c.text(-1.*w, 0.5*H, "$...$", tr)
#    #c.text(3.*w, 0.5*H, "$...$", tr)
#    c.text(-1.*w, -0.6, "$...$", tr)
#    c.text(2.7*w, -0.6, "$...$", tr)
#    for i in range(3):
#        c.text(i*w, -0.6, "$i$ $i+1$ $i+2$".split()[i], center+tr)
    
    timeslice(X, 0., 0., W=3*w)
    
    for ps in draw(ps0, [ps1, ps2], [True, True]):
        dopath(ps, st_Thick+tr)
    
    for ps in draw(ps1, [ps0, ps2], [frame, not frame]):
        dopath(ps, st_Thick+tr)
    
    for ps in draw(ps2, [ps0, ps1], [False, False]):
        dopath(ps, st_Thick+tr)
    
    timeslice(X, H, 0.3, W=3*w)
    
    for i in range(3):
        c.fill(path.circle(i*w, 0., 0.06), tr)
        c.fill(path.circle(i*w, H, 0.06), tr)


c.writePDFfile("pic-braid.pdf")


###############################################################################
#
#

w = 2.0

c = canvas.canvas()
for frame in range(2):

    X = 3.0*w*frame

    ps0 = []
    ps1 = []
    ps2 = []
    for i in range(N+1):
        r = 1.*i/N
        y = r*H
        #r = bump(r)
    
        x = 2*w*cos_up(pi*r)
        ps0.append((x, y))
    
        if frame == 0:
            x = w + cos_dn(2*pi*r)
        else:
            x = w + cos_up(2*pi*r)
        ps1.append((x, y))
    
        x = 2*w + 2*w*cos_dn(pi*r)
        ps2.append((x, y))
    
    tr = [trafo.translate(X, 0.)]
    
    if frame:
        c.text(-0.5*w, 0.5*H, r"$=$", tr)

    for i in range(3):
        c.text(i*w, -0.3, "$x$ $y$ $z$".split()[i], center+tr)
        if frame==0:
          c.text(i*w, H + 0.3, 
            r"$(x>y)>(x>z)$_$x>y$_$x$".replace(">", r"\triangleright ").split("_")[i], center+tr)
        else:
          c.text(i*w, H + 0.3, 
            r"$x>(y>z)$_$x>y$_$x$".replace(">", r"\triangleright ").split("_")[i], center+tr)
    
    for ps in draw(ps0, [ps1, ps2], [True, True]):
        dopath(ps, st_Thick+tr)
    
    for ps in draw(ps1, [ps0, ps2], [frame, not frame]):
        dopath(ps, st_Thick+tr)
    
    for ps in draw(ps2, [ps0, ps1], [False, False]):
        dopath(ps, st_Thick+tr)
    
    for i in range(3):
        c.fill(path.circle(i*w, 0., 0.06), tr)
        c.fill(path.circle(i*w, H, 0.06), tr)


c.writePDFfile("pic-braid-shelf.pdf")

###############################################################################
#
#

c = canvas.canvas()

w = 0.8
h = 0.5

def box(x, y):
    p = path.rect(x-0.5*w, y, 2*w, h)
    c.fill(p, [white])
    c.stroke(p)
    c.text(x+0.5*w, y+0.5*h, "$R$", center)


for frame in range(2):

    X = 5.0*w*frame
    tr = [trafo.translate(X, 0.)]

    for i in range(3):
        c.stroke(path.line(i*w, 0., i*w, 7*h), tr)

    for j in range(3):

        box(X + ((j+frame)%2)*w, 2*j*h+h)

    if frame == 0:
        c.text(3.5*w, 3.5*h, "$=$", center)


c.writePDFfile("pic-yb.pdf")



