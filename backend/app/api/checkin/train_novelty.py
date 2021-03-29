# coding: utf-8
import numpy as np
from sklearn import preprocessing
import pickle
from novelty_v3 import PredictModel
from time import time


filename='data/X_train.pkl'
X = pickle.load(open(filename, 'rb'))

filename='data/label_train.pkl'
name = pickle.load(open(filename, 'rb'))

print(name)

x_train=np.asarray(X)

label_encoder = preprocessing.LabelEncoder()
label_encoder=label_encoder.fit(name)
y_train = label_encoder.transform(name)

filename = 'models/name_model.pkl'
with open(filename, 'wb') as fo:  
    pickle.dump(label_encoder, fo)

novelty_detector = PredictModel()

t0=time()
novelty_detector.fit(x_train, y_train)

print(time()-t0)
filename = 'models/face_model.pkl'
with open(filename, 'wb') as fo:  
    pickle.dump(novelty_detector, fo)

