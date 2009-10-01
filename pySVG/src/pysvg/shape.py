#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
(C) 2008, 2009 Kerim Mansour
For licensing information please refer to license.txt
'''
from attributes import *
from core import *

  
        
class rect(BaseShape, PointAttrib, DimensionAttrib):
    """
    Class representing the rect element of an svg doc.
    """
    def __init__(self, x=None, y=None, width=None, height=None, rx=None, ry=None):
        BaseElement.__init__(self,'rect')
        self.set_x(x)
        self.set_y(y)
        self.set_height(height)
        self.set_width(width)
        self.set_rx(rx)
        self.set_ry(ry)
        
    def set_rx(self, rx):
        self._attributes['rx']=rx
    def get_rx(self):
        return self._attributes.get('rx')
    
    def set_ry(self, ry):
        self._attributes['ry']=ry
    def get_ry(self):
        return self._attributes.get('ry')

class circle(BaseShape):
    """
    Class representing the circle element of an svg doc.
    """
    def __init__(self, cx=None,cy=None,r=None):
        BaseElement.__init__(self,'circle')
        self.set_cx(cx)
        self.set_cy(cy)
        self.set_r(r)
    
    def set_cx(self, cx):
        self._attributes['cx']=cx
    def get_cx(self):
        return self._attributes.get('cx')
    
    def set_cy(self, cy):
        self._attributes['cy']=cy
    def get_cy(self):
        return self._attributes.get('cy')
    
    def set_r(self, r):
        self._attributes['r']=r
    def get_r(self):
        return self._attributes.get('r')

class ellipse(BaseShape):
    """
    Class representing the ellipse element of an svg doc.
    """
    def __init__(self, cx=None,cy=None,rx=None,ry=None):
        BaseElement.__init__(self,'ellipse')
        self.set_cx(cx)
        self.set_cy(cy)
        self.set_rx(rx)
        self.set_ry(ry)
        
    def set_cx(self, cx):
        self._attributes['cx']=cx
    def get_cx(self):
        return self._attributes.get('cx')
    
    def set_cy(self, cy):
        self._attributes['cy']=cy
    def get_cy(self):
        return self._attributes.get('cy')
    
    def set_rx(self, rx):
        self._attributes['rx']=rx
    def get_rx(self):
        return self._attributes.get('rx')
    
    def set_ry(self, ry):
        self._attributes['ry']=ry
    def get_ry(self):
        return self._attributes.get('ry')

class line(BaseShape, PointToAttrib):
    """
    Class representing the line element of an svg doc.
    Note that this element is NOT painted VISIBLY by default UNLESS you provide
    a style including STROKE and STROKE-WIDTH
    """
    def __init__(self, X1=None, Y1=None, X2=None, Y2=None):
        """
        Creates a line
        @type  X1: string or int
        @param X1:  starting x-coordinate
        @type  Y1: string or int
        @param Y1:  starting y-coordinate
        @type  X2: string or int
        @param X2:  ending x-coordinate
        @type  Y2: string or int
        @param Y2:  ending y-coordinate
        """
        BaseElement.__init__(self,'line')
        self.set_x1(X1)
        self.set_y1(Y1)
        self.set_x2(X2)
        self.set_y2(Y2)
        
    def set_x1(self, x1):
        self._attributes['x1']=x1
    def get_x1(self):
        return self._attributes.get('x1')
    
    def set_y1(self, y1):
        self._attributes['y1']=y1
    def get_y1(self):
        return self._attributes.get('y1')
    
    def set_x2(self, x2):
        self._attributes['x2']=x2
    def get_x2(self):
        return self._attributes.get('x2')
    
    def set_y2(self, y2):
        self._attributes['y2']=y2
    def get_y2(self):
        return self._attributes.get('y2')

    
class path(BaseShape, ExternalAttrib, MarkerAttrib):
    """
    Class representing the path element of an svg doc.
    """
    def __init__(self, pathData="",pathLength=None,style=None, focusable=None):
        BaseElement.__init__(self,'path')
        if pathData!='' and not pathData.endswith(' '):
            pathData+=' '
        self.set_d(pathData)
        if style!=None:
            self.set_style(style)

    def set_d(self, d):
        self._attributes['d']=d
    def get_d(self):
        return self._attributes.get('d')
    
    def set_pathLength(self, pathLength):
        self._attributes['pathLength']=pathLength
    def get_pathLength(self):
        return self._attributes.get('pathLength')

    def __append__(self,command, params, relative=True):
        d = self.get_d()
        if relative==True:
            d+=command.lower()
        else:
            d+=command.upper()
        for param in params:
            d+=' %s ' %(param)
        self.set_d(d)
        
    def appendLineToPath(self,endx,endy, relative=True):
        self.__append__('l',[endx,endy], relative)
  
    def appendHorizontalLineToPath(self,endx, relative=True):
        self.__append__('h',[endx], relative)
      
    def appendVerticalLineToPath(self,endy, relative=True):
        self.__append__('v',[endy], relative)
  
    def appendMoveToPath(self,endx,endy, relative=True):
        self.__append__('m',[endx,endy], relative)
    
    def appendCloseCurve(self):
        d = self.get_d()
        d+="z"
        self.set_d(d)
        
    def appendCubicCurveToPath(self, controlstartx, controlstarty, controlendx, controlendy, endx,endy,relative=True):
        self.__append__('c',[controlstartx, controlstarty, controlendx, controlendy, endx,endy], relative)
  
    def appendCubicShorthandCurveToPath(self,  controlendx, controlendy, endx,endy,relative=True):
        self.__append__('s',[controlendx, controlendy, endx,endy], relative)
    
    def appendQuadraticCurveToPath(self, controlx, controly, endx,endy,relative=True):
        self.__append__('q',[controlx, controly, endx,endy], relative)
  
    def appendQuadraticShorthandCurveToPath(self, endx,endy,relative=True):
        self.__append__('t',[endx,endy], relative)
    
    def appendArcToPath(self,rx,ry,x,y,x_axis_rotation=0,large_arc_flag=0,sweep_flag=1 ,relative=True):
        self.__append__('a',[rx,ry,x_axis_rotation,large_arc_flag,sweep_flag,x,y], relative)

class polyline(BaseShape):
    """
    Class representing the polyline element of an svg doc.
    """
    def __init__(self, points=None):
        BaseElement.__init__(self,'polyline')
        self.set_points(points)
        
    def set_points(self, points):
        self._attributes['points']=points
    def get_points(self):
        return self._attributes.get('points')
    
class polygon(polyline):
    """
    Class representing the polygon element of an svg doc.
    """
    def __init__(self, points=None):
        BaseElement.__init__(self,'polygon')
        self.set_points(points)