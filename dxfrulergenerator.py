import os
from dxfwrite import DXFEngine as dxf

class Ruler:  
    
    def __init__(self, ruler_length, ruler_width=30, tick_width=.25):
        self.length = ruler_length
        self.width = ruler_width # ruler width
        self.tick_width = tick_width # width of each engraved line
        self.tick_offset = 5 - self.tick_width / 2

    # creates a black layer and then draws the ruler's external shape
    def _draw_ruler(self):
        self.file.add_layer('CUT', color = 7)
        self.file.add(dxf.rectangle([0, 0], 10 * self.length + 10, self.width, layer = 'CUT'))
        return self

    # creates a blue layer and calls the method that draws milimiter lines once for every centimeter
    def _draw_centimeter(self):
        self.file.add_layer('SCAN', color = 5)
        for cm in range(self.length + 1):
            self._draw_milimeter(cm)
        return self

    #Desenha cada marcação de um centímetro, com diferentes tamanhos para 0 e 5 milimetros
    def _draw_milimeter(self, cm):
        for mm in range(10):
            x_pos = self.tick_offset + 10 * cm + mm
            if mm == 0: # draws a longer line at centimeter start
                y_pos = 20
                self.file.add(dxf.text(str(cm), [x_pos - 1, 20], height = 2, rotation = 90, layer = 'SCAN'))
            elif mm == 5: # draws middle sized line at half centimeter
                y_pos = 25
            else: # draws short line at every other milimeter
                y_pos = 27.5
            self.file.add(dxf.rectangle([x_pos, y_pos], self.tick_width, self.width - y_pos, layer = 'SCAN'))
            if cm == self.length: break
        return self
    
    def draw(self):
        if not os.path.lexists(os.path.join('.', 'rulers')):
            os.mkdir(os.path.join('.', 'rulers'))
        self.file = dxf.drawing(os.path.join('.', 'rulers', 'ruler_%dcm.dxf' %self.length))
        self.file.header['$INSUNITS'] = 4
        self._draw_ruler()
        self._draw_centimeter()
        self.file.save()
        return self

if __name__ == '__main__':
    ruler_length = int(input('Ruler length (in centimeters): '))
    ruler = Ruler(ruler_length)
    ruler.draw()
