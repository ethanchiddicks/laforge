import Tkinter

root = Tkinter.Tk()
root.title("Keysym Logger")

def reportEvent(event):
	print 'keysym=%s, keysym_num=%s' % (event.keysym, event.keysym_num)

canvas  = Tkinter.Canvas(root, width=200, height=500, highlightthickness=2)

canvas.bind('<KeyPress>', reportEvent)

canvas.pack(expand=1, fill="both")
canvas.focus_set()

item = canvas.create_line(0, 0, 100, 100, tags="uno")


root.mainloop()
