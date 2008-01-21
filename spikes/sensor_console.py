import Tkinter
import widgets
import math

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
		self._rect_label = self._canvas.create_text(10, HEIGHT-10, text="blah")

		self.update_canvas_callback()

		self.fake_update_distance_callback()
		
	def update_canvas_callback(self):
		# Do it again, and again, and again ...
		self._canvas.after(30, self.update_canvas_callback)

		# Draw our distance meter
		self._canvas.coords(self._rect, 0, HEIGHT-20, 100, HEIGHT-(self._distance/6.54*(HEIGHT-20)))
		self._canvas.itemconfig(self._rect_label, text=str(self._distance))

	def fake_update_distance_callback(self):
		self._canvas.after(30, self.fake_update_distance_callback)

		self._distance += 0.1 
		self._distance = self._distance % 6.0


if __name__ == '__main__':
	root = Tkinter.Tk()

	dm = DistanceMeter(root)

	root.mainloop()
