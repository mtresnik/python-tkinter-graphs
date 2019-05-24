import tkinter as tk
import random
import math

node_num = 0
class Node():
	def __init__(self):
		global node_num
		self.id = node_num
		node_num += 1

	def __str__(self):
		return str(self.id)

class Connection():
	def __init__(self, node1, node2, weight):
		self.node1 = node1
		self.node2 = node2
		self.weight = weight
	def __str__(self):
		return "[" +str(self.node1) + "]--" +str(self.weight) + "-->[" + str(self.node2) + "]"
	def contains(self, node):
		if node == self.node1 or node == self.node2:
			return True
		return False
	def isOrigin(self, node):
		if node == self.node1:
			return True
		return False
layer_num = 0
class Layer():
	def __init__(self, nodes=[]):
		global layer_num
		self.nodes = nodes
		self.id = layer_num
		layer_num+=1

	def __str__(self):
		nodeStr = "["
		for i in range(0, len(self.nodes)):
			nodeStr += str(self.nodes[i])
			if i < len(self.nodes) - 1:
				nodeStr += ", "
		nodeStr += "]"
		return "L" + str(self.id) + ":" + nodeStr

class Graph():
	def __init__(self, nodes=[], connections=[], layers=[]):
		self.nodes = nodes
		self.connections = connections
		self.layers = layers

	def addNode(self, node):
		if node in self.nodes:
			return
		self.nodes.append(node)

	def addConnection(self, connection):
		if connection in self.connections:
			return
		self.addNode(connection.node1)
		self.addNode(connection.node2)
		self.connections.append(connection)

	def addLayer(self, layer):
		if layer in self.layers:
			return
		for i in range(0, len(layer.nodes)):
			self.addNode(layer.nodes[i])
		self.layers.append(layer)

	def nodeConnectMap(self):
		retMap = {}
		for i in range(0, len(self.nodes)):
			tempCon = []
			for j in range(0, len(self.connections)):
				if self.connections[j].isOrigin(self.nodes[i]):
					tempCon.append(self.connections[j])
			retMap[self.nodes[i]] = tempCon
		return retMap

	def nodeConnectContainsMap(self):
		retMap = {}
		for i in range(0, len(self.nodes)):
			tempCon = []
			for j in range(0, len(self.connections)):
				if self.connections[j].contains(self.nodes[i]):
					tempCon.append(self.connections[j])
			retMap[self.nodes[i]] = tempCon
		return retMap

	def nodeConnectMapString(self):
		retString = ""
		connMap = self.nodeConnectMap()
		for i in range(0, len(self.nodes)):
			retString += str(self.nodes[i])
			retString += ":"
			connStr = "["
			for j in range(0, len(connMap[self.nodes[i]])):
				currCon = connMap[self.nodes[i]][j]
				connStr += str(currCon)
				if j < len(connMap[self.nodes[i]]) - 1:
					connStr += ", "
			connStr += "]"
			retString += connStr
			if i < len(self.nodes) - 1:
				retString += "\n"
		return retString

	def __str__(self):
		retString = ""
		nodeStr = "["
		for i in range(0, len(self.nodes)):
			nodeStr += str(self.nodes[i])
			if i < len(self.nodes) - 1:
				nodeStr += ", "
		nodeStr += "]"
		retString += "Nodes:" + nodeStr + "\n"
		connStr = "["
		for i in range(0, len(self.connections)):
			connStr += str(self.connections[i])
			if i < len(self.connections) - 1:
				connStr += ", "
		connStr += "]"
		retString += "Connections:" + connStr + "\n"
		retString += "Layers:\n"
		for i in range(0, len(self.layers)):
			retString += str(self.layers[i])
			if i < len(self.layers) - 1:
				retString += "\n"
		return retString

def testGraph():
	g = Graph()
	for i in range(0, 8):
		g.addNode(Node())
	g.addConnection(Connection(g.nodes[0], g.nodes[1], weight=3))
	g.addConnection(Connection(g.nodes[0], g.nodes[2], weight=10))
	g.addConnection(Connection(g.nodes[1], g.nodes[0], weight=4))
	g.addConnection(Connection(g.nodes[1], g.nodes[2], weight=20))
	g.addConnection(Connection(g.nodes[1], g.nodes[3], weight=30))
	g.addConnection(Connection(g.nodes[1], g.nodes[4], weight=40))
	g.addConnection(Connection(g.nodes[2], g.nodes[3], weight=6))
	g.addConnection(Connection(g.nodes[2], g.nodes[5], weight=50))
	g.addConnection(Connection(g.nodes[3], g.nodes[1], weight=6))
	g.addConnection(Connection(g.nodes[3], g.nodes[4], weight=5))
	g.addConnection(Connection(g.nodes[3], g.nodes[5], weight=15))
	g.addConnection(Connection(g.nodes[4], g.nodes[6], weight=10))
	g.addConnection(Connection(g.nodes[5], g.nodes[3], weight=12))
	g.addConnection(Connection(g.nodes[6], g.nodes[5], weight=3))
	g.addConnection(Connection(g.nodes[5], g.nodes[7], weight=10))
	g.addConnection(Connection(g.nodes[6], g.nodes[7], weight=12))
	l1 = Layer([g.nodes[0], g.nodes[1]])
	l2 = Layer([g.nodes[2], g.nodes[3], g.nodes[4]])
	l3 = Layer([g.nodes[5], g.nodes[6]])
	l4 = Layer([g.nodes[7]])
	g.addLayer(l1)
	g.addLayer(l2)
	g.addLayer(l3)
	g.addLayer(l4)
	return g

class Application(tk.Frame):
	def __init__(self, master, graph):
		super().__init__(master)
		self.master = master
		self.pack()
		self.graph = graph
		self.create_widgets()

	def create_widgets(self):
		self.winfo_toplevel().title("Graph Utility")
		self.defButton = tk.Button(self)
		self.defButton["text"] = "Randomize Colors"
		self.defButton["command"] = self.randomColorButton
		self.defButton.pack(side="top")
		padd_left = 20
		padd_right = padd_left
		rect_width = 50
		rect_height = rect_width
		max_nodes = 0
		for i in range(0, len(self.graph.layers)):
			max_nodes = max(max_nodes, len(self.graph.layers[i].nodes))
		self.width = 100*(len(self.graph.layers) +2)
		self.height = rect_height*(max_nodes + 6)
		self.canvas = tk.Canvas(self, width=self.width, height=self.height)
		self.canvas.pack()
		self.layerRects = {}
		self.nodeRects = {}

		padd_left = 20
		padd_right = padd_left
		rect_width = 50
		rect_height = rect_width
		h_space = (self.width - padd_left - padd_right - len(self.graph.layers)*rect_width)/((len(self.graph.layers) - 1))
		# Draw Rectangles
		self.drawRects(padd_left, padd_right, rect_width, rect_height, h_space)
		# Draw Arrows
		drawLines = self.getLines(rect_width, rect_height)
		for i in range(0, len(drawLines)):
			self.canvas.create_line(drawLines[i]["start"], drawLines[i]["end"], arrow=tk.LAST, smooth=True, splinesteps=200)
			x0, y0 = drawLines[i]["start"]
			x1, y1 = drawLines[i]["end"]
			x = (x0+x1)/2 - 5
			y = (y0+y1)/2 + 15
			label = tk.Label(self, text=str(drawLines[i]["weight"]), font=("Helvetica", 8))
			label.place(x=x, y=y)
				# self.canvas.create_line(origin_center, to_center, arrow=tk.LAST)
	def randomColorButton(self):
		# print(self.nodeRects)
		for i in range(0, len(self.graph.layers)):
			tempCol = self.randcolor()
			currlayer = self.graph.layers[i]
			for j in range(0, len(self.layerRects[currlayer])):
				currRectId = self.layerRects[currlayer][j]["drawRect"]
				self.canvas.itemconfigure(currRectId, fill=tempCol)


	def drawRects(self, padd_left, padd_right, rect_width, rect_height, h_space):
		layerSpacing = {}
		# Draw Rects
		for i in range(0, len(self.graph.layers)):
			tempDict = {}
			tempDict["v_space"] = rect_height
			tempDict["padd_top"] = (self.height - rect_height*len(self.graph.layers[i].nodes) - tempDict["v_space"]*(len(self.graph.layers[i].nodes) - 1)) / 2
			tempDict["padd_bottom"] = tempDict["padd_top"]
			tempDict["color"] = self.randcolor()
			layerSpacing[self.graph.layers[i]] = tempDict
			tempRects = []
			x0 = padd_left + i*rect_width + i*h_space
			x1 = x0 + rect_width
			for j in range(0, len(self.graph.layers[i].nodes)):
				y0 = tempDict["padd_top"] + j*rect_height + j*tempDict["v_space"]
				y1 = y0 + rect_height
				temp_rect = self.canvas.create_rectangle(x0, y0, x1, y1, fill=tempDict["color"])
				rectDict = {}
				coords = (x0, y0, x1, y1)
				center_x = (x0 + x1)/2
				center_y = (y0 + y1)/2
				rectDict["center"] = (center_x, center_y)
				rectDict["coords"] = (x0, y0, x1, y1)
				rectDict["dim"]= (rect_width, rect_height)
				rectDict["drawRect"] = temp_rect
				self.nodeRects[self.graph.layers[i].nodes[j]] = rectDict
				tempRects.append(rectDict)
			self.layerRects[self.graph.layers[i]] = tempRects

	def getLines(self, rect_width, rect_height):
		# Draw Arrows
		lineMap = {}
		connMap = self.graph.nodeConnectMap()
		RIGHT, TOP, LEFT, BOTTOM = 0, 1, 2, 3
		for i in range(0, len(self.graph.nodes)):
			currNode = self.graph.nodes[i]
			origin_center = self.nodeRects[currNode]["center"]
			oX, oY = origin_center
			currConn = connMap[currNode]
			dirArr = []
			for j in range(0, len(currConn)):
				theta = None
				to_center = self.nodeRects[currConn[j].node2]["center"]
				tX, tY = to_center
				if oX == tX:
					if oY < tY:
						theta = 270
					else:
						theta = 90
				elif oY == tY:
					if oX <= tX:
						theta = 0
					else:
						theta = 180
				else:
					dx = tX - oX
					dy = -1*(tY - oY)
					atan = math.atan(dy/dx)*180/math.pi
					if tX < oX:
						atan += 180
					elif atan < 0:
						atan += 360
					theta = atan
				dirDict = {}
				dirDict["connection"] = currConn[j]
				dirDict["theta"] = theta
				dirDict["origin_center"] = origin_center
				dirDict["to_center"] = to_center
				toNode = currConn[j].node2
				if currConn[j].node1 != currNode:
					continue
				dirDict["origin_node"] = currNode
				dirDict["to_node"] = toNode
				if theta > 45 and theta <= 135:
					dirDict["d0"] = TOP
				elif theta > 135 and theta <= 225:
					dirDict["d0"] = LEFT
				elif theta > 225 and theta <= 315:
					dirDict["d0"] = BOTTOM
				else:
					dirDict["d0"] = RIGHT
				dirDict["d1"] = (dirDict["d0"] + 2) % 4
				dirArr.append(dirDict)
			lineDict = {}
			lineDict["directions"] = dirArr
			lineDict["right"] = []
			lineDict["top"] = []
			lineDict["left"] = []
			lineDict["bottom"] = []
			lineMap[currNode] = lineDict
		for i in range(0, len(self.graph.nodes)):
			origin_node = self.graph.nodes[i]
			connections = lineMap[origin_node]["directions"]
			for j in range(0, len(connections)):
				dirDict = connections[j]
				if origin_node != dirDict["connection"].node1:
					continue
				to_node = dirDict["connection"].node2
				if dirDict["d0"] == TOP:
					lineMap[origin_node]["top"].append(dirDict)
					lineMap[to_node]["bottom"].append(dirDict)
				elif dirDict["d0"] == RIGHT:
					lineMap[origin_node]["right"].append(dirDict)
					lineMap[to_node]["left"].append(dirDict)
				elif dirDict["d0"] == BOTTOM:
					lineMap[origin_node]["bottom"].append(dirDict)
					lineMap[to_node]["top"].append(dirDict)
				else:
					lineMap[origin_node]["left"].append(dirDict)
					lineMap[to_node]["right"].append(dirDict)	

		# print(self.graph.nodeConnectMapString())
		for i in range(0, len(self.graph.nodes)):
			currNode = self.graph.nodes[i]
			lineDict = lineMap[currNode]
			currRect = self.nodeRects[currNode]
			x0, y0, x1, y1 = currRect["coords"]
			lineDict["top_conn"] = []
			top_pad = rect_width / (len(lineDict["top"]) + 1) 
			for j in range(0, len(lineDict["top"])):
				tempX = x0 + top_pad + j*top_pad
				tempY = y0
				tempDict = {}
				tempDict["coords"] = (tempX, tempY)
				tempDict["occupied"] = False
				tempDict["origin_node"] = lineDict["top"][j]["connection"].node1
				tempDict["to_node"] = lineDict["top"][j]["connection"].node2
				lineDict["top_conn"].append(tempDict)
			lineDict["left_conn"] = []
			left_pad = rect_height / (len(lineDict["left"]) + 1)
			for j in range(0, len(lineDict["left"])):
				tempY = y0+left_pad + j*left_pad
				tempX = x0
				tempDict = {}
				tempDict["coords"] = (tempX, tempY)
				tempDict["occupied"] = False
				tempDict["origin_node"] = lineDict["left"][j]["connection"].node1
				tempDict["to_node"] = lineDict["left"][j]["connection"].node2
				lineDict["left_conn"].append(tempDict)
			lineDict["right_conn"] = []
			right_pad = rect_height / (len(lineDict["right"]) + 1)
			for j in range(0,len(lineDict["right"])):
				tempY = y0+right_pad + j*right_pad
				tempX = x1
				tempDict = {}
				tempDict["coords"] = (tempX, tempY)
				tempDict["occupied"] = False
				tempDict["origin_node"] = lineDict["right"][j]["connection"].node1
				tempDict["to_node"] = lineDict["right"][j]["connection"].node2
				lineDict["right_conn"].append(tempDict)
			lineDict["bottom_conn"] = []
			bottom_pad = rect_width / (len(lineDict["bottom"]) + 1)
			for j in range(0, len(lineDict["bottom"])):
				tempX = x0+bottom_pad + j*bottom_pad
				tempY = y1
				tempDict = {}
				tempDict["coords"] = (tempX, tempY)
				tempDict["occupied"] = False
				tempDict["origin_node"] = lineDict["bottom"][j]["connection"].node1
				tempDict["to_node"] = lineDict["bottom"][j]["connection"].node2
				lineDict["bottom_conn"].append(tempDict)
		toDraw = []
		for i in range(0, len(self.graph.nodes)):
			currNode = self.graph.nodes[i]
			lineDict = lineMap[currNode]
			connections = lineDict["directions"]
			for j in range(0, len(connections)):
				currConn = connections[j]
				if currConn["connection"].node1 != currNode:
					continue
				toNode = currConn["connection"].node2
				toLineDict = lineMap[toNode]
				LARGE_NUM = 200000
				for k in range(0, len(lineDict["top_conn"])):
					if lineDict["top_conn"][k]["occupied"] == True:
						continue
					fX, fY = lineDict["top_conn"][k]["coords"]
					mindist = LARGE_NUM
					minconn_top = None
					Lindex = -1
					for L in range(0, len(toLineDict["bottom_conn"])):
						if toLineDict["bottom_conn"][L]["occupied"] == True:
							continue
						if toLineDict["bottom_conn"][L]["to_node"] != toNode:
							continue
						tX, tY = toLineDict["bottom_conn"][L]["coords"]
						dist = math.sqrt(math.pow(fX - tX, 2) + math.pow(fY - tY, 2))
						if dist < mindist:
							mindist = dist
							Lindex = L
							minconn_top = {}
							minconn_top["coords"] = (fX, fY, tX, tY)
							minconn_top["start"] = (fX, fY)
							minconn_top["end"] = (tX, tY)
							minconn_top["origin_node"] = currNode
							minconn_top["to_node"] = toNode
							minconn_top["weight"] = currConn["connection"].weight
					if minconn_top != None:
						minconn_top["arrow_dir"] = tk.FIRST
						toDraw.append(minconn_top)
						lineDict["top_conn"][k]["occupied"] = True
						lineDict["top_conn"][k]["arrow"] = minconn_top
						toLineDict["bottom_conn"][Lindex]["occupied"] = True
						toLineDict["bottom_conn"][Lindex]["arrow"] = minconn_top
				for k in range(0, len(lineDict["bottom_conn"])):
					if lineDict["bottom_conn"][k]["occupied"] == True:
						continue
					fX, fY = lineDict["bottom_conn"][k]["coords"]
					mindist = LARGE_NUM
					minconn_bottom = None
					Lindex = -1
					for L in range(0, len(toLineDict["top_conn"])):
						if toLineDict["top_conn"][L]["occupied"] == True:
							continue
						if toLineDict["top_conn"][L]["to_node"] != toNode:
							continue
						tX, tY = toLineDict["top_conn"][L]["coords"]
						dist = math.sqrt(math.pow(fX - tX, 2) + math.pow(fY - tY, 2))
						if dist < mindist:
							mindist = dist
							Lindex = L
							minconn_bottom = {}
							minconn_bottom["coords"] = (fX, fY, tX, tY)
							minconn_bottom["start"] = (fX, fY)
							minconn_bottom["end"] = (tX, tY)
							minconn_bottom["origin_node"] = currNode
							minconn_bottom["to_node"] = toNode
							minconn_bottom["weight"] = currConn["connection"].weight
					if minconn_bottom != None:
						minconn_bottom["arrow_dir"] = tk.LAST
						toDraw.append(minconn_bottom)
						lineDict["bottom_conn"][k]["occupied"] = True
						lineDict["bottom_conn"][k]["arrow"] = minconn_bottom
						toLineDict["top_conn"][Lindex]["occupied"] = True
						toLineDict["top_conn"][Lindex]["arrow"] = minconn_bottom
				for k in range(0, len(lineDict["left_conn"])):
					if lineDict["left_conn"][k]["occupied"] == True:
						continue
					fX, fY = lineDict["left_conn"][k]["coords"]
					mindist = LARGE_NUM
					minconn_left = None
					Lindex = -1
					for L in range(0, len(toLineDict["right_conn"])):
						if toLineDict["right_conn"][L]["occupied"] == True:
							continue
						if toLineDict["right_conn"][L]["to_node"] != toNode:
							continue
						tX, tY = toLineDict["right_conn"][L]["coords"]
						dist = math.sqrt(math.pow(fX - tX, 2) + math.pow(fY - tY, 2))
						if dist < mindist:
							mindist = dist
							Lindex = L
							minconn_left = {}
							minconn_left["coords"] = (fX, fY, tX, tY)
							minconn_left["start"] = (fX, fY)
							minconn_left["end"] = (tX, tY)
							minconn_left["origin_node"] = currNode
							minconn_left["to_node"] = toNode
							minconn_left["weight"] = currConn["connection"].weight
					if minconn_left != None:
						minconn_left["arrow_dir"] = tk.LAST
						toDraw.append(minconn_left)
						lineDict["left_conn"][k]["occupied"] = True
						lineDict["left_conn"][k]["arrow"] = minconn_left
						toLineDict["right_conn"][Lindex]["occupied"] = True
						toLineDict["right_conn"][Lindex]["arrow"] = minconn_left
				for k in range(0, len(lineDict["right_conn"])):
					if lineDict["right_conn"][k]["occupied"] == True:
						continue
					fX, fY = lineDict["right_conn"][k]["coords"]
					mindist = LARGE_NUM
					minconn_right = None
					Lindex = -1
					for L in range(0, len(toLineDict["left_conn"])):
						if toLineDict["left_conn"][L]["occupied"] == True:
							continue
						if toLineDict["left_conn"][L]["to_node"] != toNode:
							continue
						tX, tY = toLineDict["left_conn"][L]["coords"]
						dist = math.sqrt(math.pow(fX - tX, 2) + math.pow(fY - tY, 2))
						if dist < mindist:
							mindist = dist
							Lindex = L
							minconn_right = {}
							minconn_right["coords"] = (fX, fY, tX, tY)
							minconn_right["start"] = (fX, fY)
							minconn_right["end"] = (tX, tY)
							minconn_right["origin_node"] = currNode
							minconn_right["to_node"] = toNode
							minconn_right["weight"] = currConn["connection"].weight
					if minconn_right != None:
						minconn_right["arrow_dir"] = tk.FIRST
						toDraw.append(minconn_right)
						lineDict["right_conn"][k]["occupied"] = True
						lineDict["right_conn"][k]["arrow"] = minconn_right
						toLineDict["left_conn"][Lindex]["occupied"] = True
						toLineDict["left_conn"][Lindex]["arrow"] = minconn_right
		# print(toDraw)
		for i in range(0, len(self.graph.nodes)):
			currNode = self.graph.nodes[i]
			lineDict = lineMap[currNode]
			connections = lineDict["directions"]
			for j in range(0, len(lineDict["left_conn"])):
				currArr = lineDict["left_conn"][j]["arrow"]
				for k in range(0, len(lineDict["left_conn"])):
					subArr = lineDict["left_conn"][k]["arrow"]
					if i == k:
						continue
					x0, y0, x1, y1 = currArr["coords"]
					x2, y2, x3, y3 = subArr["coords"]
					res = testCollisions(x0,y0,x1,y1,x2,y2,x3,y3)
					if res == False:
						continue
					# currArr["start"], currArr["end"], subArr["start"], subArr["end"]
					# start -> start
					x0, y0 = currArr["start"]
					x1, y1 = currArr["end"]
					x2, y2 = subArr["start"]
					x3, y3 = subArr["end"]
					try:
						if testCollisions(x2, y2, x1, y1, x0, y0, x3, y3) == False:
							temp = currArr["start"]
							currArr["start"] = subArr["start"]
							subArr["start"] = temp
							tweight = currArr["weight"]
							currArr["weight"] = subArr["weight"]
							subArr["weight"] = tweight
							continue
					except:
						e = None
					try:
						if testCollisions(x0, y0, x3, y3, x2, y2, x1, y1) == False:
							temp = currArr["end"]
							currArr["end"] = subArr["end"]
							subArr["end"] = temp
							continue
					except:
						e = None
					try:
						if testCollisions(x3, y3, x1, y1, x2, y2, x0, y0) == False:
							temp = currArr["start"]
							currArr["start"] = subArr["end"]
							subArr["end"] = temp
							continue
					except:
						e = None
					try:
						if testCollisions(x0, y0, x2, y2, x1, y1, x3, y3) == False:
							temp = currArr["start"]
							currArr["start"] = subArr["end"]
							subArr["end"] = temp
							continue
					except:
						e = None
		
			for j in range(0, len(lineDict["right_conn"])):
				currArr = lineDict["right_conn"][j]["arrow"]
				for k in range(0, len(lineDict["right_conn"])):
					subArr = lineDict["right_conn"][k]["arrow"]
					if i == k:
						continue
					x0, y0, x1, y1 = currArr["coords"]
					x2, y2, x3, y3 = subArr["coords"]
					res = testCollisions(x0,y0,x1,y1,x2,y2,x3,y3)
					if res == False:
						continue
					# currArr["start"], currArr["end"], subArr["start"], subArr["end"]
					# start -> start
					x0, y0 = currArr["start"]
					x1, y1 = currArr["end"]
					x2, y2 = subArr["start"]
					x3, y3 = subArr["end"]
					try:
						if testCollisions(x2, y2, x1, y1, x0, y0, x3, y3) == False:
							temp = currArr["start"]
							currArr["start"] = subArr["start"]
							subArr["start"] = temp
							continue
					except:
						e = None
					try:
						if testCollisions(x0, y0, x3, y3, x2, y2, x1, y1) == False:
							temp = currArr["end"]
							currArr["end"] = subArr["end"]
							subArr["end"] = temp
							continue
					except:
						e = None
					try:
						if testCollisions(x3, y3, x1, y1, x2, y2, x0, y0) == False:
							temp = currArr["start"]
							currArr["start"] = subArr["end"]
							subArr["end"] = temp
							continue
					except:
						e = None
					try:
						if testCollisions(x0, y0, x2, y2, x1, y1, x3, y3) == False:
							temp = currArr["start"]
							currArr["start"] = subArr["end"]
							subArr["end"] = temp
							continue
					except:
						e = None
		return toDraw

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

def testCollisions(x0,y0,x1,y1,x2,y2,x3,y3):
	if x1 == x0 or x2 == x3:
		return True
	m0 = (y1 - y0)/(x1 - x0)
	m1 = (y3 - y2)/(x3 - x2)
	if m0 == m1:
		return False
	x = (m0*x0 - m1*x2 +y2 - y0) / (m0 - m1)
	minx = min(x0, x1)
	minx1 = min(x2,x3)
	minx = min(minx, minx1)
	maxX = max(x0, x1)
	maxX1 = max(x2, x3)
	maxX = max(maxX, maxX1)
	if minx < x and x < maxX:
		return True
	return False


def testDraw(graph):
	root = tk.Tk()
	app = Application(master=root, graph=graph)
	app.mainloop()

def main():
	g = testGraph()
	testDraw(g)

if __name__ == "__main__":
	main()
