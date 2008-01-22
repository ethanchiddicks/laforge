import Tkinter
#import widgets
import math
import daq

# Globals!
WIDTH = 800
HEIGHT = 600

class DistanceMeter(Tkinter.Canvas):
	def __init__(self, root):
		self._distance = 0.0
		
		# Tkinter setup
		self._canvas = Tkinter.Canvas(root, width=WIDTH, height=HEIGHT)
		self._canvas.pack()

		self._rect = self._canvas.create_rectangle(0, 0, 100, 400, fill="blue")
		self._line = self._canvas.create_line(400, 0, 400, 400)
		self._rect_label = self._canvas.create_text(100, HEIGHT-10, text="blah")

		self.update_canvas_callback()

		self.update_distance_callback()
		
	def update_canvas_callback(self):
		# Do it again, and again, and again ...
		self._canvas.after(30, self.update_canvas_callback)

		# Draw our distance meter
		#self._canvas.coords(self._rect, 0, HEIGHT-20, 100, HEIGHT-(self._distance/6.45*(HEIGHT-20)))
		self._canvas.coords(self._rect, 0, HEIGHT-20, 100, HEIGHT-((self._distance/6.45)*(HEIGHT-20)))

		self._canvas.itemconfig(self._rect_label, text=str(self._distance))

	def update_distance_callback(self):
		self._canvas.after(10, self.update_distance_callback)

		r = daq.read_daq()

		#print r[0]
		#print r[0]/2.54
		#print (r[0]/2.54)*6.45
		#print "---"

		self._distance = (r[0]/2.54)*6.45


if __name__ == '__main__':



	root = Tkinter.Tk()

	dm = DistanceMeter(root)

	root.mainloop()
