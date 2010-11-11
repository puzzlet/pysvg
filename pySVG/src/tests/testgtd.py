'''
Created on 11.11.2010

@author: kerim
'''
from pysvg import parser
from pysvg.structure import svg
from pysvg.shape import rect
from pysvg.core import TextContent 

def main():
    anSVG = parser.parse('./sourceimages/gtdsample.svg')
    
    print anSVG.getAllElements()
    for element in anSVG.getAllElements():
        if isinstance(element, TextContent)==False:
            print element.get_id()
    
    for element in anSVG.getAllElementsOfHirarchy():
         if isinstance(element, TextContent)==False:
            print element.get_id()
    
    for element in anSVG.getElementsByType(rect):
        print element.get_id()
        print element.getAttributes()
    
    
    

if __name__ == "__main__":
    main()