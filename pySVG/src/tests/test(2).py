import pysvg

from pysvg.structure import *
from pysvg.objecthelper import *
from pysvg.transformhelper import *
from pysvg.stylehelper import *

def getExtremum(items, function, operator):
    i = 0
    current = items[i]
    extremum = function(current)
    while i < len(items) - 1:
        i += 1
        current = items[i]
        if operator(function(current), extremum):
            extremum = function(current)
    return extremum
    
class MyGroup(Group):
    
    def addElement(self, element):
        element.style_dict = self.style_dict
        Group.addElement(self, element)

class Line(BaseElement):

    def __init__(self, x1=None,y1=None,x2=None,y2=None,style_dict=None,focusable=None):
        if not style_dict:
            style_dict = {}
        if not 'stroke-width' in style_dict:
            style_dict['stroke-width'] = 1
        if not 'stroke' in style_dict:
            style_dict['stroke'] = 'black'
        BaseElement.__init__(self,"<line ", style_dict,focusable)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    @classmethod
    def from_points(cls, start, end, style_dict=None,focusable=None):
        return cls(start[0], start[1], end[0], end[1], style_dict, focusable)


    def get_width(self):
        return abs(self.x1 - self.x2)

    def get_height(self):
        return abs(self.y1 - self.y2)

    def get_bottom_left(self):
        if self.x1 < self.x2:
            if self.y1 < self.y2:
                return (self.x1, self.y1)
            else:
                return (self.x1, self.y2)
        else:
            if self.y1 < self.y2:
                return (self.x2, self.y1)
            else:
                return (self.x2, self.y2)

    def get_top_right(self):
        if self.x1 < self.x2:
            if self.y1 < self.y2:
                return (self.x2, self.y2)
            else:
                return (self.x2, self.y1)
        else:
            if self.y1 < self.y2:
                return (self.x1, self.y2)
            else:
                return (self.x1, self.y1)

    def normalize_to_point(self, (x,y)):
        self.x1 += x
        self.x2 += x
        self.y1 += y
        self.y2 += y

class Ellipse(ellipse):

    def getWidt(self):
        return abs(2 * self.rx)

    def getHeight(self):
        return abs(2 * self.ry)

    def get_bottom_left(self):
        return (self.cx - self.rx, self.cy - self.ry)

class Rectangle(BaseElement):

    def __init__(self,x=None,y=None,width=None,height=None, rx=0, ry=0,style_dict=None,focusable=None):
        if not style_dict:
            style_dict = {}
        if not 'stroke-width' in style_dict:
            style_dict['stroke-width'] = 1
        if not 'stroke' in style_dict:
            style_dict['stroke'] = 'black'
        if not 'fill' in style_dict:
            style_dict['fill'] = 'none'
        BaseElement.__init__(self,"<rect ", style_dict, focusable)
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.rx=rx
        self.ry=ry
        self.inner_box = MyGroup(style_dict={})
        self.inner_box.style_dict['stroke'] = '#FF0000'
        self.inner_box.style_dict['stroke-width'] = 1
        self.inner_box.style_dict['stroke-dasharray'] = 1.6
        self.inner_box.style_dict['stroke-opacity'] = 0.5
        
    def get_edge_points(self):
        result = [(self.x,self.y)]
        result.append((self.x+self.width,self.y))
        result.append((self.x+self.width,self.y+self.height))
        result.append((self.x,self.y+self.height))
        return result
        
    def get_inner_edge_points(self):
        result = []
        result.append((self.x + self.rx, self.y + self.ry))
        result.append((self.x + self.width - self.rx, self.y + self.ry))
        result.append((self.x + self.width - self.rx, self.y + self.height - self.ry))
        result.append((self.x + self.rx, self.y + self.height - self.ry))
        return result
        
    def show_inner_box(self, show_box):
        if show_box:
            self.create_inner_box()
            self.getXML = self.getXML_with_inner
        else:
            self.getXML = BaseElement.getXML
            
    def create_inner_box(self):
        self.inner_box.elements = []
        edges = self.get_inner_edge_points()
        self.inner_box.addElement(Line.from_points(edges[0], edges[1]))
        self.inner_box.addElement(Line.from_points(edges[1], edges[2]))
        self.inner_box.addElement(Line.from_points(edges[2], edges[3]))
        self.inner_box.addElement(Line.from_points(edges[3], edges[0]))
        
        
    def getXML_with_inner(self):
        myXML = BaseElement.getXML(self)
        myXML += self.inner_box.getXML()
        return myXML

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def transform_to_include(self, elements):
        self.x = getExtremum([e.get_bottom_left()[0] for e in elements], lambda p:p, lambda n,c: n < c)
        self.y = getExtremum([e.get_bottom_left()[1] for e in elements], lambda p:p, lambda n,c: n < c)
        self.x -= self.rx
        self.y -= self.ry
        most_right = getExtremum([e.get_top_right()[0] for e in elements], lambda p:p, lambda n,c: n > c)
        most_top = getExtremum([e.get_top_right()[1] for e in elements], lambda p:p, lambda n,c: n > c)
        self.width = most_right + self.rx - self.x
        self.height = most_top + self.ry - self.y
        

    def get_bottom_left(self):
        return (self.x, self.y)

    def get_top_right(self):
        return (self.x + self.width, self.y + self.height)

    def normalize_to_point(self, (x,y)):
        self.x += x
        self.y += y

class Circle(BaseElement):

    def __init__(self,cx=None,cy=None,r=None,style_dict=None,focusable=None):
        if not style_dict:
            style_dict = {}
        if not 'stroke-width' in style_dict:
            style_dict['stroke-width'] = 1
        if not 'stroke' in style_dict:
            style_dict['stroke'] = 'black'
        if not 'fill' in style_dict:
            style_dict['fill'] = 'none'
        BaseElement.__init__(self,"<circle ", style_dict, focusable)
        self.cx = cx
        self.cy = cy
        self.r=r

    def _getDiameter(self):
        return 2 * self.r

    def get_width(self):
        return self._getDiameter()

    def get_height(self):
        return self._getDiameter()

    def get_bottom_left(self):
        return (self.cx - self.r, self.cy - self.r)

    def get_top_right(self):
        return (self.cx + self.r, self.cy + self.r)

    def normalize_to_point(self, (x,y)):
        self.cx += x
        self.cy += y

class PolyLine(polyline):

    def getWidth(self):
        xs = [p[0] for p in self.points]
        max_x = xs.pop()
        min_x = max_x
        while len(xs) > 0:
            current = xs.pop()
            if current > max_x:
                max_x = current
            if current < min_x:
                min_x = current
        return abs(max_x - min_x)

    def getHeight(self):
        ys = [p[1] for p in self.points]
        max_y = ys.pop()
        min_y = max_y
        while len(ys) > 0:
            current = ys.pop()
            if current > max_y:
                max_y = current
            if current < min_y:
                min_y = current
        return abs(max_y - min_y)

    def get_bottom_left(self):
        x = getExtremum([p[0] for p in self.points], lambda p:p, lambda n,c: n < c)
        y = getExtremum([p[1] for p in self.points], lambda p:p, lambda n,c: n < c)
        return (x,y)

class Text(BaseElement):

    def __init__(self,content, x ,y,  rotate=None, style_dict=None, editable=None, focusable=None,**args):
        BaseElement.__init__(self,"<text ", style_dict, focusable,endTag="</text>\n")
        self.x=x
        self.y=y
        self.rotate=rotate
        self.editable=editable
        self.content=content

    def getXML(self):
        """
        Return a XML representation of the current element.
        This function can be used for debugging purposes. It is also used by getXML in SVG

        @return:  the representation of the current element as an xml string
        """
        xml=self.startXML
        for item in dir(self):
          if item.find('_')==-1 and item.find('XML') ==-1 and item.find('content')==-1:
            if getattr(self,item) != None:
              xml+=item+"=\"%s\" " %(getattr(self,item))
          elif item=='style_dict':
              if getattr(self,item) != None:
                xml+=self.getXMLFromStyle()
        xml+=">"
        xml+=self.content
        xml+=self.endXML
        return xml


class Shape(SVG):

    anchor_points = {}
    zero = (0,0)

    def __init__(self, *args, **kwargs):
        SVG.__init__(self,*args, **kwargs)

    def getXML(self, full = True):
        if full:
            xml=SVG_HEADER
        else:
            xml = ""
        if self.height!= None:
            xml += 'height="%s" ' % (self.height)
        if self.width!= None:
            xml += 'width="%s" ' % (self.width)
        if self.viewBox!= None:
            xml += 'viewBox="%s" ' % (self.viewBox)
        xml += END_TAG_LINE
        for element in self.elements:
            xml += element.getXML()
        if full:
            xml += SVG_FOOTER
        return xml

    def getWidt(self):
        i = 0
        current = self.elements[i]
        max = current.getWidth()
        while i < len(self.elements) - 1:
            i += 1
            current = self.elements[i]
            if current.getWidth() > max:
                max = current.getWidth()
        return max

    def getHeight(self):
        i = 0
        current = self.elements[i]
        max = current.getHeight()
        while i < len(self.elements) - 1:
            i += 1
            current = self.elements[i]
            if current.getHeight() > max:
                max = current.getWidth()
        return max

    def centerToPoint(self, shape, point):
        pass

    def addNormalized(self, element):
        element.normalize_to_point(self.zero)
        self.addElement(element)


if __name__ == "__main__":
    """
    This just draws a few random shapes and then creates a rectangle that
    spans all of them. Finally, the show_inner_box is switched on.
    """
    shape = Shape()
    shape.zero = (100, 150)
    shape.addNormalized(Line(x1=-50, y1=-100, x2=50, y2=100))
    r = Rectangle(x=20,y=10,width=25, height=76, rx =23, ry=2)
    shape.addNormalized(r)
    c = Circle(cx = -20, cy = 8, r= 34)
    shape.addNormalized(c)
    shape.addNormalized(Circle( cx = 20, cy = 200, r = 89))
    outer = Rectangle(rx = 10, ry = 10)
    outer.transform_to_include(shape.elements)
    outer.show_inner_box(True)
    shape.addElement(outer)
    shape.saveSVG("test.svg")
    print "done"
