from Tkinter import *
from dialog import *
from multiprocessing import Process
import Proc_52_52
import zmq
import os
from tkFileDialog import *
from NET4 import *
from other import *
from dialog import *

class APP:
	def __init__(self):
		self.root = Tk()
		self.root.title("MAin 52x52 BackProp")
		self.lframe = Frame(self.root)
		self.rframe = Frame(self.root)
		self.StartButtonName = StringVar()
		self.StartButtonName.set("Start Network")
		self.StartButton = Button(self.root, textvariable = self.StartButtonName, command=self.StartNN)
		self.StartButton.pack()
		self.TestButton = Button(self.root, text = "Load Nn and Test", command = self.TestNN)
		self.TestButton.pack()
		self.TestText = StringVar()
		self.MainProcText = StringVar()
		self.NNStructureText = StringVar()
		self.PorogText = StringVar()
		self.IterationText = StringVar()
		self.StepLearningText = StringVar()
		self.RealErrorText = StringVar()
		self.MeanError = StringVar()
		self.MainProcText.set("%s\n%s"%(0, 1))
		Label(self.root, textvariable = self.TestText).pack()
		Label(self.root, textvariable = self.MainProcText).pack()
		self.canvas = Canvas(self.lframe)
		self.canvas1 = Canvas(self.rframe)
		self.ButtonFrame = Frame(self.canvas1)
		self.lframe.pack(side = LEFT)
		Label(self.canvas, textvariable = self.IterationText).pack()
		Label(self.canvas, textvariable = self.PorogText).pack()
		Label(self.canvas, textvariable = self.StepLearningText).pack()
		Label(self.canvas, textvariable = self.RealErrorText).pack()
		Label(self.canvas, textvariable = self.MeanError).pack()
		self.canvas.pack()
		self.ButtonScrollBar = Scrollbar(self.rframe, orient = 'vertical', command = self.canvas1.yview)
		self.canvas1.configure(yscrollcommand = self.ButtonScrollBar.set)
		self.ButtonScrollBar.pack(side = 'left', fill = Y)
		self.canvas1.pack(side = 'left')
		self.canvas1.create_window((0, 0), window = self.ButtonFrame, anchor = 'nw')
		def conf(event):
			self.canvas1.configure(scrollregion = self.canvas1.bbox('all'))
		self.ButtonFrame.bind('<Configure>', conf)
		self.rframe.pack(side=RIGHT)
		self.Mainproc = None
		self.startedProc = []
		self.ProcessButtons = []
		self.ProcessData = []
		self.startedProc = []
		self.ButtonsText = []
		
		context = zmq.Context()
		self.socket = context.socket(zmq.SUB)
		self.socket.bind("tcp://127.0.0.1:5352")
		self.socket.setsockopt(zmq.SUBSCRIBE, '')
		self.socket.RCVTIMEO = 25
		#self.socket_send = context.socket(zmq.PUB)
		#self.socket_send.connect("tcp://127.0.0.1:5645")

		self.Exit = False
		self.learningrate = 0.1
		self.MainLoop()

	def StartNN(self, x = [1]):
		if self.StartButtonName.get() == "Start Network":
			self.StartButtonName.set("Pause Network")
			

		else:
			pass
		#d = DialogCreateNNWithHiden(self.root)
		#if d != None:
		self.dMSE = []
		self.root.title("MAin 1x1 BackProp %s"%x)
		self.Mainproc = Process(target=Proc_52_52.main, args=("%s\t%s\t%s"%(52, 52, x), "main"))
		self.Mainproc.start()

	def sort_b(self, l):
		n = 0
		while n < len(l):
			for i in range(0,len(l)-1):
				if l[i] > l[i+1]:
					l[i],l[i+1] = l[i+1],l[i]
			n += 1
		return l[:]
		
	def TestNN(self):
		
		options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
		options['initialdir'] = os.getcwd()
		options['initialfile'] = 'myfile.txt'
		options['parent'] = self.root
		options['title'] = 'This is a title'
		p = askopenfile( **options)
		Net = NET(1,1)
		Net.LoadNet(p.name)
		d = DialogTestNN(self.root)
		res = IntListToTrans_52(d.value)
		#print len(res)
		t = Net.TestNet(res)
		print ("sizeinput = %s\n out = %s"%(Net.inputsize, t))
		t1 = t.tolist()
		s1 = []
		for i in xrange(len(t1)):
			s1.append((float(t1[i]), i+1))
		dd = dict(s1)	
		s = dd.keys()
		s = self.sort_b(s)
		r = []
		for i in range(1,7):
			r.append(dd[s[-i]])
			print (dd[s[-i]], s[-i])
		k = "%s\n%s"%(TransToIntList(t.tolist()), r)
		self.TestText.set("%s"%k)
	
	"""def TestNNAfter(self):
		
		dirlist = os.listdir(path)
		l = []
		for i in dirlist:
			if os.path.isfile(i):
				if i[-3:] == "xml":
					l.append(os.path.basename(i))
		l1=[]
		for i in xrange(len(l)):
			l1.append(l[i][:-4].split("  "))
		for i in xrange(len(l1)):
			l1[i][0] = float(l1[i][0])
		d = dict(l1[:])
		l2 = d.keys()
		l2 = self.sort_b(l2[:])
		Net = NET(1,1)
		Net.LoadNet("%s  %s.xml"%(l2[0], d[l2[0]]))
		inx = read_file_data_r_maxima("data.txt")
		out=inx[:]
		res = [0 for i in xrange(len(out)/5)]
		j=0
		for i in xrange(0, len(out), 5):
			res[j] = tuple(IntListToTrans_45(out[i:i+5]))
			j+=1
		print res[-1]
		t = Net.TestNet(res[-1])
		print "sizeinput = %s\n out = %s\nLen(input) = %s"%(Net.inputsize, t, len(res[-1]))
		t1 = t.tolist()
		s1 = []
		for i in xrange(len(t1)):
			s1.append((float(t1[i]), i+1))
		dd = dict(s1)	
		s = dd.keys()
		s = self.sort_b(s)
		r = []
		for i in range(1,6):
			r.append(dd[s[-i]])
			print dd[s[-i]], s[-i]
		k = "%s\n%s"%(TransToIntList_45(t.tolist()), r)
		self.TestText.set("%s"%k)"""
		

	def UpdateButtons(self):
		if self.startedProc != []:
			try:
				msg = self.socket.recv()
				k = msg.split(" ")
				self.ButtonsText[int(k[0])].set("Net: %s, %s, %s\nError: %s\nProgress: %s"%(self.ParamForText[int(k[0])][0], self.ParamForText[int(k[0])][1], self.ParamForText[int(k[0])][2], float(k[1]), int(k[2])))
				self.root.update()
			except: pass
		
	def UmpdateMainProcNN(self):
		if self.StartButtonName.get() != "Start Network" and self.Mainproc != None:
			try:
				msg = self.socket.recv()
				#print msg
				m = msg.split(" ")
				if m[0] == 'main':
					#print m
					self.MainProcText.set("%s\n%s"%(m[2], m[1]))
					self.PorogText.set("Structure Hiden layer of NN: %s"%m[4])
					self.IterationText.set("Iteration i = %s"%m[3])
					self.MeanError.set("Mean of Errors = %s"%m[5])
					self.RealErrorText.set("Real Error = %s"%m[6])
					self.dMSE.append(float(m[1]))
			except: pass
		self.root.update()

	def MainLoop(self):
		
		def DellFiles(fend, all = False):
			path = os.getcwd()
			dirlist = os.listdir(path)
			l = []
			for i in dirlist:
				if os.path.isfile(i):
					if i[-len(fend):] == fend:
						l.append(os.path.basename(i))
			l1=[]
			for i in xrange(len(l)):
				l1.append(l[i][:-(len(fend)+1)].split("  "))
			for i in xrange(len(l1)):
				l1[i][0] = float(l1[i][0])
			d = dict(l1[:])
			l2 = d.keys()
			l2 = self.sort_b(l2[:])
			for i in l:
				if all == True:
					os.remove(i)
				elif i.find("%s"%l2[0]) == -1:
					os.remove(i)
					
		path = os.getcwd()
		while self.Exit == False:
			if self.Mainproc != None:
				#print self.Mainproc.is_alive()
				if self.Mainproc.is_alive() == False and self.startedProc == []:
					dirlist = os.listdir(path)
					l = []
					for i in dirlist:
						if os.path.isfile(i):
							if i[-3:] == "xml":
								l.append(os.path.basename(i))
					l1=[]
					for i in xrange(len(l)):
						l1.append(l[i][:-4].split("  "))
					for i in xrange(len(l1)):
						l1[i][0] = float(l1[i][0])
					d = dict(l1[:])
					l2 = d.keys()
					l2 = self.sort_b(l2[:])
					if l2[0]<0.000000000000001:
						self.Exit = True
						break
					fw = open("dMSE.err","w")
					fw.write("%s"%self.dMSE[:-1])
					fw.close()
					self.dMSE = []
					param = self.ParamFromText(d[l2[0]])
					alter = self.Alternate(param[2])
					self.AddProcAndButton(param[0], param[1], alter[:])
				p = 0
				if self.startedProc != []:
					for i in self.startedProc:
						if i.is_alive() == True:
							p+=1
					if p == 0:
						dirlist = os.listdir(path)
						l = []
						for i in dirlist:
							if os.path.isfile(i):
								if i[-3:] == "upd":
									l.append(os.path.basename(i))
						l1=[]
						for i in xrange(len(l)):
							l1.append(l[i][:-4].split("  "))
						for i in xrange(len(l1)):
							l1[i][0] = float(l1[i][0])
						d = dict(l1[:])
						l2 = d.keys()
						l2 = self.sort_b(l2[:])
						
						self.StartNN(d[l2[0]].split("_")[1])
						self.root.title("MAin 52x52 BackProp %s"%d[l2[0]].split("_")[1])
						self.startedProc = []
						DellFiles("xml")
						DellFiles("upd", True)
						DellFiles("work")
			self.UpdateButtons()
			self.root.update()
			self.UmpdateMainProcNN()

	def AddProcAndButton(self, inp, out, alter):
		#manager = Manager()
		
		self.startedProc = []
		self.ButtonsText = []
		self.ParamForText = []
		if len(self.ProcessButtons) > 0:
			for i in self.ProcessButtons:
				i.destroy()
		self.ProcessButtons = []
		for i in xrange(len(alter)):
			self.ParamForText.append([inp, unicode(alter[i]), out])
			#self.ProcessData.append(manager.dict())
			#self.ProcessData[-1]["Error"] = 1
			self.ButtonsText.append(StringVar())
			self.ProcessButtons.append(Button(self.ButtonFrame, textvariable = self.ButtonsText[-1]))
			self.ProcessButtons[-1].bind("<Button-1>", self.CommandStopProc)
			self.startedProc.append(Process(target=Proc_52_52.main, args=("%s\t%s\t%s"%(inp, out, unicode(alter[i])),i, i)))
			self.ProcessButtons[-1].pack(side = BOTTOM)
		for i in xrange(len(self.ProcessButtons)):
			try:
				self.ButtonsText[i].set("Net: %s, %s, %s\nError: %s\nProgress: %s"%(inp, alter[i], out, 1, 0))
			except:
				print ("Except manager", self.ProcessData[i])
				self.ButtonsText[i].set("Net: %s, %s, %s\nError: %s\nProgress: %s"%(inp, alter[i], out, 1, 0))
		for i in  self.startedProc:
			i.start()
		
	def ParamFromText(self, s):
		s1 = s.split("_")
		s2 = []
		print (s1, "ParamFromText")
		s2.append(int(s1[0]))
		s2.append(int(s1[2]))
			#else: s2.append(s1[i])
		s3 = s1[1].strip("[").strip("]")
		if s3.find(",") == -1:
			s2.append([int(s3)])
		else:
			s4 = s3.split(",")
			s5 = []
			for i in s4:
				s5.append(int(i))
			s2.append(s5)
		return s2[:]

	def Alternate(self, m):
		r = []
		for i in xrange(len(m)):
			m[i]= m[i]+1
			r.append(m[:])
			m[i]= m[i]-1
		m.append(1)
		r.append(m)
		
		return r
		
	def CommandStopProc(self, event):
		for i in xrange(len(self.ProcessButtons)):
			print (self.ProcessButtons[i], event.widget)
			if self.ProcessButtons[i] == event.widget:
				self.startedProc[i].terminate()
				event.widget.destroy()
				break
			
if __name__ == "__main__":
	a = APP()