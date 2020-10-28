import tkinter as tk
from random import random
from math import sin,cos,radians


class ball:
	def __init__(self,x=240,y=620,r=6,col = "black"): # Top Tanımlama
		self.x = x
		self.y = y
		self.r = r
		self.col = col
		self.olu = False
		self.fit = []
		self.yon = [random()*360 for i in range(400)] # 360 derecelik rastgele yönlerden oluşan 400 adet liste
		pass
	def fitnessCalc(self):# Uygunluk Fonksiyonu
		self.fit.append(((self.x-240)**2+(self.y-20)**2)**0.5) # Hedefe uzaklık
	def draw(self,canva):
		canva.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r, fill= self.col) # Kendini çizdiriyor
	def move(self,alp):
		if self.olu:# Öldü mü?
			self.fit.append(1000)# Diğerlerinden önce ölürse gelecek nesillere gen aktarım şansını o kadar kaybediyor
		else:# Yaşıyor ise
			self.fitnessCalc()
			self.x += 30*sin(radians(alp))
			self.y -= 30*cos(radians(alp))
		if self.x>480 or self.x<0 or self.y>640 or self.y<0: # SINIRLAR
			self.olu = True
			self.x -= 30*sin(radians(alp))
			self.y += 30*cos(radians(alp))
		
		if self.x>0 and self.y>300 and self.x<300 and self.y<340:# Engel 1
			self.olu = True
			self.x -= 30*sin(radians(alp))
			self.y += 30*cos(radians(alp))
		if self.x>200 and self.y>200-60 and self.x<640 and self.y<240-60:# Engel 2
			self.olu = True
			self.x -= 30*sin(radians(alp))
			self.y += 30*cos(radians(alp))
		
	def reborn(self):# Gelecek nesil doğuyor
		self.x = 240
		self.y = 620
		self.olu = False
		newyon = []
		for i in self.yon:
			newyon.append(i+(0.5-random())*15) # 8 oranında yeni doğanın genlerinde mutasyon oluşturuyor
		self.yon = newyon


main = tk.Tk()# Sayfayı oluşturma
main.geometry("480x640")

C = tk.Canvas(main, bg="gray",height=640,width=480)

mean = lambda ls: sum(ls)/len(ls)# Listenin ortalamasını alma fonksiyonu oluşturdum

balls = [ball() for i in range(200)]# 200 adet top oluşturuyor
#top = ball()

def bittimi(balls):# Tüm topların ölüp ölmediğini kontrol ediyor
	for i in balls:
		if i.olu == False:
			return False
	return True
	
maxfit = 570
def selectParent(balls):# Popülasyonda başarılı olanları seçiyor
	allballmeanfits = []
	selected = []
	for i in balls:
		allballmeanfits.append(mean(i.fit))
	allballmeanfits,allballminfits = mean(allballmeanfits), min(allballmeanfits)
	
	print("All Balls Mean Error :",allballmeanfits)
	for i in balls:
		if mean(i.fit) < allballminfits+100 and mean(i.fit) < maxfit:
			selected.append(i)
	return selected

i = 0
z = 10
best = balls[0]

loopspeed = 100

def loop():# Sonsuz döngülü fonksiyon
	global i,z, balls, best
	i+=1
	for ali in balls:
		ali.move(ali.yon[i])
	
	if bittimi(balls):
		i=0
		balls = selectParent(balls)
		best = balls[0]
		for ali in balls:
			if(min(best.fit)>min(ali.fit)):
				best = ali
			ali.reborn()
		newballs = [ball(col="red") for i in range(200-len(balls))]
		
		for ali in newballs:
			ali.yon = best.yon
			ali.reborn()
			balls.append(ali)
	#top.move(top.yon[i])
	
	if i > z or i>345:
		i=0
		z+=5
		print(z)
		for u in balls:
			u.olu = True
	main.after(loopspeed,loop)

	
def draw():# Kendini tekrar eden çizen fonksiyon
	C.delete("all")
	arc = C.create_oval(240-10,20-10,240+10,20+10,fill="red") # GOAL
	engel = C.create_rectangle(0,300,300,340,fill="red")
	engel = C.create_rectangle(640,300-160,200,340-160,fill="red")
	for ali in balls:
		ali.draw(C)
	#best.draw(C)
	#top.draw(C)
	main.after(15,draw)
def slow(e):
	global loopspeed
	if loopspeed>1:
		loopspeed-=1
	print("LOOP SPEED : ",loopspeed)
def fast(e):
	global loopspeed
	loopspeed+=1
	print("LOOP SPEED : ",loopspeed)
main.after(loopspeed,loop)
main.after(1,draw)
main.bind("<Up>",slow)
main.bind("<Down>",fast)
C.pack()
main.mainloop()