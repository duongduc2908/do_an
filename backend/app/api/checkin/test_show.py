import os
import imageio
import cv2
import time
from feature_extraction.extractor import FaceVector
from face_detection.face_detection import detect_face

face_vector = FaceVector()

import pickle

svm_file='models/face_model.pkl'
svm = pickle.load(open(svm_file, 'rb'))
name_file='models/name_model.pkl'
name_model = pickle.load(open(name_file, 'rb'))
path='test_images'
font = cv2.FONT_HERSHEY_SIMPLEX
dirs = os.listdir(path)
for files in dirs:
	file_name=path+"/"+files

	name=file_name.split('/')
	l=name[-1]
	image = imageio.imread(file_name)
	prev = time.time()
	print(image.shape)
	bbs, points = detect_face(image)
	print("Detect time: ", time.time() - prev)
	for bb, point in zip(bbs, points):
		(l,t,r,b)=bb
		prev = time.time()
		emb=face_vector.get_vector(image, bb,point)		
		y_pred,label = svm.predict([[emb]])
		name=name_model.inverse_transform(label)
		if y_pred[0]>1:
			name=['']	
		if len(name[0])>0:		
			cv2.rectangle(image,(l, t), (r, b), (255, 0, 0), 2)
		else:
			cv2.rectangle(image,(l, t), (r, b), (255, 255, 0), 2)
		if t>30:		
			cv2.putText(image,name[0],(l-6*(len(name[0])-4),t-10), font, 0.8,(0,255,0),2) 
		else:		
			cv2.putText(image,name[0],(l-6*(len(name[0])-4),b+20), font, 0.8,(0,255,0),2) 
	cv2.imwrite("img_test/"+files, image[..., ::-1])
	# cv2.waitKey(0)
