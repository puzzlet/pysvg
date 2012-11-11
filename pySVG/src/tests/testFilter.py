'''
Created on 25.06.2010

@author: kerim
'''
from pysvg.filter import  *
from pysvg.structure import *
from pysvg.style import Style
from pysvg.builders import *

sh=ShapeBuilder()
c1 = sh.createCircle(cx=20, cy=20, r=15, fill="yellow")
c1.set_id("gesicht")
c2 = sh.createCircle(cx=15, cy=15, r=2, fill="black")
c2.set_id("auge-links")
c3 = sh.createCircle(cx=25, cy=15, r=2, fill="black")
c3.set_id("auge-rechts")
l1 = sh.createLine(x1=20, y1=18, x2=20, y2=23, strokewidth=2)
l1.set_id("nase")
p1 = Path("M 13 26 A 5 3 0 0 0 27 26")
p1.set_id("mund")
p1.set_stroke("black")
p1.set_stroke_width("2")
p1.set_fill("none")

mySymbol = Symbol()
mySymbol.set_id("smilie")
mySymbol.addElement(c1)
mySymbol.addElement(c2)
mySymbol.addElement(c3)
mySymbol.addElement(l1)
mySymbol.addElement(p1)

filter6 = Filter(x="-.3",y="-.5", width=1.9, height=1.9)
filtBlur = FeGaussianBlur(stdDeviation="4")
filtBlur.set_in("SourceAlpha")
filtBlur.set_result("out1")
filtOffset = FeOffset()
filtOffset.set_in("out1")
filtOffset.set_dx(4)
filtOffset.set_dy(-4)
filtOffset.set_result("out2")

filtMergeNode1 = FeMergeNode()
filtMergeNode1.set_in("out2")

filtMergeNode2 = FeMergeNode()
filtMergeNode2.set_in("SourceGraphic")
filtMerge = FeMerge()
filtMerge.addElement(filtMergeNode1)
filtMerge.addElement(filtMergeNode2)
filter6.addElement(filtBlur) # here i get an error from python. It is not allowed to add a primitive filter
filter6.addElement(filtOffset)
filter6.addElement(filtMerge)
filter6.set_id("Filter6")


d=Defs()
d.addElement(mySymbol)
d.addElement(filter6)

s = Svg(width="380px", height="370px")
s.addElement(d)



myUse = Use()
myUse.set_xlink_href("#smilie")
myUse.set_transform("translate(250,250) scale(2.7)")
myUse.set_filter("url(#Filter6)")
s.addElement(myUse)    
    
s.save('./testoutput/filter.svg')

