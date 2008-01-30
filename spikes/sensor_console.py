import Tkinter
#import widgets
import math
import daq
import time

# Globals!
WIDTH = 800
HEIGHT = 600
AngleWindow = 200, 0, 800, 1000
dist_buff = [0, 0]
gyro_buff = [0, 0, 0]
f = open("anglesensorlog.tsv", "w")

class DistanceMeter(Tkinter.Canvas):
	def __init__(self, root):
		self._distance = 0.0
		self._gyroV = 0.0
		self._gyroA = 0.0
		self._gyroavg = 0.0
		self._lasttime = time.time()
		self._lastextent = 45.0
		self._direction = 0
		
		# Tkinter setup
		self._canvas = Tkinter.Canvas(root, width=WIDTH, height=HEIGHT)
		self._canvas.pack()

		self._rect = self._canvas.create_rectangle(0, 0, 100, 400, fill="blue")
		self._arc= self._canvas.create_arc(AngleWindow, start = 0, extent = 0)
		self._rect_label = self._canvas.create_text(100, HEIGHT-10, text="blah")
		self._rect_labelgyroV = self._canvas.create_text(300, HEIGHT-10, text="blah")
		self._rect_labelgyroA = self._canvas.create_text(300, HEIGHT-30, text="blah")
		
		f.write("Time\Gyro OUT\n")
		self.update_canvas_callback()

		self.update_distance_callback()
		self.update_angle_callback()
		
	def update_canvas_callback(self):
		# Do it again, and again, and again ...
		self._canvas.after(30, self.update_canvas_callback)

		# Draw our distance meter
		#self._canvas.coords(self._rect, 0, HEIGHT-20, 100, HEIGHT-(self._distance/6.45*(HEIGHT-20)))
		self._canvas.coords(self._rect, 0, HEIGHT-20, 100, HEIGHT-((self._distance/6.45)*(HEIGHT-20)))

		self._canvas.itemconfig(self._rect_label, text=str(self._distance)+ " meters")
		self._canvas.itemconfig(self._rect_labelgyroV, text=str(self._gyroV)+ " V")
		self._canvas.itemconfig(self._rect_labelgyroA, text=str(self._gyroA))

	def update_distance_callback(self):
		self._canvas.after(10, self.update_distance_callback)

		r = daq.read_daq()
		
		r[0] = r[0]/2.54*6.45
		
		dist_buff[1] = dist_buff[0]
		dist_buff[0] = r[0]
		
		self._distance = (dist_buff[0] + dist_buff[1])/2
		
		
	def update_angle_callback(self):
		self._canvas.after(20, self.update_angle_callback)
		
		r = daq.read_daq()
		self._gyroV = r[1]
		
		gyro_buff[2] = gyro_buff[1]
		gyro_buff[1] = gyro_buff[0]
		gyro_buff[0] = (r[1] - 1.48) * 10
		self._gyroavg = (gyro_buff[0] + gyro_buff[1] + gyro_buff[2]) / 3
		timenow = time.time()
		
		#Accumulator
		self._gyroA = self._gyroA + gyro_buff[0] * (timenow-self._lasttime)
		self._lasttime = timenow
		#Positive = Moving Right
		dir = gyro_buff[0] - gyro_buff[1]
		
		if dir < -2 and self._direction == 1:
			self._direction = 0
			self._gyroA = abs(self._gyroA)/2 + 2
		
		if dir > 2 and self._direction == 0:
			self._direction = 1
			self._gyroA = abs(self._gyroA)/-2 - 2	
			#self._gyroA = 0
		
		self._canvas.itemconfig(self._arc, start=self._gyroA*10+90)
		
		f.write("%f\t%f\t%f\t%f\n" % (timenow, gyro_buff[0], self._gyroavg, self._gyroA*10))
		
		

if __name__ == '__main__':



	root = Tkinter.Tk()

	dm = DistanceMeter(root)

	root.mainloop()
