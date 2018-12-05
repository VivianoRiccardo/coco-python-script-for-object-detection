from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
from PIL import Image
from threading import Thread
import time

class IlMioThread (Thread):
	def __init__(self, lista,d,coco,num):
		Thread.__init__(self)
		self.lista = lista
		self.d = d
		self.coco = coco
		self.num = num
		
	def run(self):
		h = -1
		w = -1
		k11 = 0
		k12 = 0
		k21 = 0
		k22 = 0
		number_list = []
		count1 = 0
		r_c = 0

		for i in self.lista:
			number_list = []
			t = self.coco.imgs[i]
			h, w = t['height'], t['width']
			k11 = 0
			k12 = 0
			k21 = 0
			k22 = 0

			h = 640-h
			w = 640-w

			if h > 0 and h%2==0:
				k11 = h/2
				k12 = h/2
			elif h > 0 and h%2!=0:
				k11 = ((int)(h/2))
				k12 = ((int)(h/2))+1
				
			if w > 0 and w%2==0:
				k21 = w/2
				k22 = w/2
			elif w > 0 and w&2!=0:
				k21 = ((int)(w/2))
				k22 = ((int)(w/2))+1
			
			for j in range(0,len(d[i])):
				if(j%2==0):
					self.d[i][j][0] += k21
					self.d[i][j][1] += k11
			
			h, w = t['height'], t['width']
					
			imgIds = self.coco.getImgIds(imgIds=[i]);
			img = self.coco.loadImgs(imgIds[np.random.randint(0,len(imgIds))])[0]
			I = io.imread(img['coco_url'])
			io.imsave(str(self.num)+".jpg", I)
			im = Image.open(str(self.num)+".jpg", "r")
			pix_val = list(im.getdata())
			count1 = 0
			if(type(pix_val[0]) != int):
				#print(i)
				f = open("./data/"+str(i)+".txt","w")
				r_c += 1
				for j in range(0,640):
					for k in range(0,640):
						if(j < k11 or j >= k11+h or k < k21 or k >= k21+w):
							number_list.append(0)
						else:
							 #print(pix_val[count1])
							number_list.append(pix_val[count1][0])
							count1+=1

				count1 = 0
				for j in range(0,640):
					for k in range(0,640):
						if(j < k11 or j >= k11+h or k < k21 or k >= k21+w):
							number_list.append(0)
						else:
							number_list.append(pix_val[count1][1])
							count1+=1
				count1 = 0
				for j in range(0,640):
					for k in range(0,640):
						if(j < k11 or j >= k11+h or k < k21 or k >= k21+w):
							number_list.append(0)
						else:
							number_list.append(pix_val[count1][2])
							count1+=1
				

				for j in range(0,len(number_list)):
					f.write((str(number_list[j]))+',')
				
				for j in range(0,len(d[i])):
					if(j%2==0):
						for k in range(0,len(self.d[i][j])):
							f.write(str(self.d[i][j][k])+',')
					else:
						f.write((str(self.d[i][j])+','))
				f.close()

pylab.rcParams['figure.figsize'] = (8.0, 10.0)
dataDir='..'
dataType='train2017'
annFile='{}/annotations/instances_{}.json'.format(dataDir,dataType)
coco=COCO(annFile)

d = {}
for i in coco.anns:

	#print(coco.loadAnns([i]))
	#exit(0)
	if coco.loadAnns([i])[0]['image_id'] not in d:
		d[coco.loadAnns([i])[0]['image_id']] = [coco.loadAnns([i])[0]['bbox'],coco.loadAnns([i])[0]['category_id']]
	else:
		d[coco.loadAnns([i])[0]['image_id']].append(coco.loadAnns([i])[0]['bbox'])
		d[coco.loadAnns([i])[0]['image_id']].append(coco.loadAnns([i])[0]['category_id'])

lista = d.keys()

l1 = []
l2 = []
l3 = []
l4 = []
for i in range(0,len(lista)/4):
	l1.append(lista[i])

for i in range(len(lista)/4,len(lista)/2):
	l2.append(lista[i])

for i in range(len(lista)/2,len(lista)*3/4):
	l3.append(lista[i])

for i in range(len(lista)*3/4,len(lista)):
	l4.append(lista[i])
	
thread1 = IlMioThread(l1,d,coco,1)
thread2 = IlMioThread(l2,d,coco,2)
thread3 = IlMioThread(l3,d,coco,3)
thread4 = IlMioThread(l4,d,coco,4)
thread1.start()
thread2.start()
thread3.start()
thread4.start()
# Join
thread1.join()
thread2.join()
thread3.join()
thread4.join()

