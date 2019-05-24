import tkinter as tk
import random

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.winfo_toplevel().title("Random Squares Utility")
		self.defButton = tk.Button(self)
		self.defButton["text"] = "Randomize Rects"
		self.defButton["command"] = self.defButtonAction
		self.defButton.pack(side="top")
		self.canvas = tk.Canvas(self, width=500, height=500)
		self.canvas.pack()
		self.rects = []
		rectNum = 20
		for i in range(0, rectNum):
			temp_rect = self.canvas.create_rectangle(self.randcoords(), fill=self.randcolor())
			self.rects.append(temp_rect)

	def defButtonAction(self):
		# print("Random Locs Clicked")
		for i in range(0, len(self.rects)):
			self.canvas.coords(self.rects[i], self.randcoords())
			self.canvas.itemconfigure(self.rects[i], fill=self.randcolor())

	def randcoords(self):
		try:
			a0 = random.randint(0, self.canvas.winfo_width() - 50)
			b0 = random.randint(50, self.canvas.winfo_height() - 50)
		except:
			a0 = random.randint(0, 500 - 50)
			b0 = random.randint(0, 500 - 50)
		a1 = a0 + 50
		b1 = b0 + 50
		return a0, b0, a1, b1

	def randcolor(self):
		return '#%02x%02x%02x' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

root = tk.Tk()
app = Application(master=root)
app.mainloop()