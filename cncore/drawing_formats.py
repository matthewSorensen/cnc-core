# This module almost isn't required, but there are enough differences
# that we do in fact need it.  Future work might add clever on-demand
# loading of the various modules.

from dxfwrite import DXFEngine as dxf
import svgwrite

class DXFWriter:

    CUT = 'cut'
    SCORE =  'score'
    RASTER = 'raster'
    ALT = 'alt'
    
    def __init__(self,filename):
        self._filename_ = filename
        self._drawing_ = None
    
    def __enter__(self):
        self._drawing_ = dxf.drawing(self._filename_)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._drawing_.save()


    def line(self,start,end, mode):
        self._drawing_.add(dxf.line(start,end,layer = mode))

    def polyline(self, points, mode, closed = False, fill = False):
        polyline = dxf.polyline(layer = mode)
        polyline.add_vertices(points)
        polyline.close(closed)
        self._drawing_.add(polyline)

    def circle(self, center, radius, mode, fill = False):
        circle = dxf.circle(radius, center)
        self._drawing_.add(circle)
        
class SVGWriter:

    CUT = svgwrite.rgb(255, 0, 0, '%')
    SCORE =  svgwrite.rgb(0, 0, 255, '%')
    RASTER = svgwrite.rgb(0, 0, 0, '%')
    ALT = svgwrite.rgb(0,255,0,'%')
    
    def __init__(self,filename):
        self._filename_ = filename
        self._drawing_ = None

    def __enter__(self):
        self._drawing_ = svgwrite.Drawing(filename = self._filename_, size = ("1000mm","1000mm"), profile = "full")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._drawing_.save()

    def mm(self,obj):
        """ A rather nice, if crude, hammer to make things look more mm-ish """
        try:
            return [self.mm(x) for x in obj]
        except Exception:
            return 3.543307 * obj

    def polyline(self, points, mode, closed = False, fill = False):
        points = self.mm(points)
        if closed:
            points.append(points[0])
        if fill == False:
            fill = 'none'
        self._drawing_.add(svgwrite.shapes.Polyline(points, stroke = mode, fill = fill))

    def line(self,start,end, mode):
        self.polyline([start,end], mode)

    def circle(self, center, radius, mode, fill = False):
        if fill == False:
            fill = 'none'
        circ = svgwrite.shapes.Circle(center = self.mm(center), r = self.mm(radius), fill = fill, stroke = mode)
        self._drawing_.add(circ)
