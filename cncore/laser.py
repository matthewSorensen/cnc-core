import svgwrite
import tempfile 
import os
import subprocess

# operations:
# * manage file handles
# * manage file conversions transparently
# * colors / laser semantics
# * access to the underlying svg
# * higher-level drawing operations


class LaserOutput:
    # This is really only applicable to universal laser systems at the moment
    CUT = svgwrite.rgb(255, 0, 0, '%')
    SCORE =  svgwrite.rgb(0, 0, 255, '%')
    RASTER = svgwrite.rgb(0, 0, 0, '%')
    ALT = svgwrite.rgb(0,255,0,'%')

    def __init__(self, filename):
        rest, _ = os.path.splitext(filename)
        self._svg_filename_ = rest + '.svg'
        self._dxf_filename_ = rest + '.dxf'
        self._drawing_ = None

        
    def __enter__(self):
        self._drawing_ = svgwrite.Drawing(filename = self._svg_filename_,size = ("1000mm", "1000mm"),  profile = "full")
        return self

    def __exit__(self,exc_type, exc_value, traceback):
        self._drawing_.save()
        with tempfile.NamedTemporaryFile() as f:
            subprocess.call(["inkscape",self._svg_filename_, '--export-ps=' + f.name])
            subprocess.call(["pstoedit","-dt", "-f", "dxf:-polyaslines -mm",f.name, self._dxf_filename_])

        return False

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
