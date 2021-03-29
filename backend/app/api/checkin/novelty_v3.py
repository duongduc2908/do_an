# -*- coding: utf-8 -*-
import bottleneck as bn
from sklearn import model_selection
from sklearn.svm import SVC
import numpy as np
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.utils import shuffle

class NoveltyDetectionSingle:

    def __init__(self, known_class, novelty_class):
        self.theta = []
        self.known_class = known_class
        self.novelty_class = novelty_class
        set_known_class = set(known_class)
        self.set_known_class = set_known_class
        known_class_to_sub_class = dict()
        sub_class_to_known_class = dict()
        for i in range(len(known_class)):
            known_class_to_sub_class[known_class[i]] = i
            sub_class_to_known_class[i] = known_class[i]

        self.known_class_to_sub_class = known_class_to_sub_class
        self.sub_class_to_known_class = sub_class_to_known_class
        self.n_class=len(set_known_class)+len(set(novelty_class))
        self.scale=0.02
        self.norm=0.001
    def fit(self, X, y):
        X_known = []
        X_novelty = []
        y_known = []
        y_novelty = []
        for i in range(len(y)):
            if y[i] in self.set_known_class:
                X_known.append(X[i])
                y_known.append(y[i])
            else:
                X_novelty.append(X[i])
                y_novelty.append(y[i])

        test_size = len(y_novelty)
        X_svm, X_h, y_svm, y_h = model_selection.train_test_split(X_known, y_known, test_size=0.25,random_state=107)

        y_svm_train = [self.known_class_to_sub_class[c] for c in y_svm]
        
        sgd=LogisticRegression(random_state=23,solver='lbfgs',class_weight='balanced',multi_class='multinomial',max_iter=80)
        #sgd = SGDClassifier(random_state=23,max_iter=1000,tol=0.0001)
        sgd.fit(X_svm, y_svm_train)
        svc = CalibratedClassifierCV(sgd,cv='prefit')
        svc.fit(X_svm, y_svm_train)
        self.svc = svc
        # tạo tập training cho layer tiếp theo
        X_next = []
        y_next = []
        for x,y in zip(X_h,y_h):
            y_pred_proba = svc.predict_proba([x])[0]
            y_pred_proba_sorted = sorted(y_pred_proba)
            theta_s = self.scale*y_pred_proba_sorted[-1] / (y_pred_proba_sorted[-2]+self.norm)
            #print(theta_s)
            theta_v=  y_pred_proba_sorted[-1]
            #print('known:',theta_v,theta_s)
            X_next.append([theta_v,theta_s])
            y_next.append(0)
        for x,y in zip(X_novelty,y_novelty):
            y_pred_proba = svc.predict_proba([x])[0]
            y_pred_proba_sorted = sorted(y_pred_proba)
            theta_s = self.scale*y_pred_proba_sorted[-1] / (y_pred_proba_sorted[-2]+self.norm)
            theta_v=  y_pred_proba_sorted[-1]
            #print('unknown:',theta_v,theta_s)	
            X_next.append([theta_v,theta_s])
            y_next.append(1)

        #novelty_model= SVC(kernel='linear', C=0.025,probability=True,class_weight='balanced')
        novelty_model=LogisticRegression(random_state=23,solver='lbfgs',class_weight='balanced',multi_class='multinomial',max_iter=80)
        novelty_model.fit(X_next, y_next)

        self.novelty_model = novelty_model

    def predict(self, X):
        ret = []
        for seq in X:
            y_pred_proba = self.svc.predict_proba(seq)
            #y_pred_proba = bn.median(y_pred_proba, axis=0)
            y_pred_proba = np.mean(y_pred_proba, axis=0)
            y_pred_proba_sorted = sorted(y_pred_proba)
            theta_s =self.scale*y_pred_proba_sorted[-1] / (y_pred_proba_sorted[-2]+self.norm)
            theta_v=  y_pred_proba_sorted[-1]	
	    #print(theta_v,theta_s)
            ret.append(self.novelty_model.predict([[theta_v,theta_s]])[0])
        return ret


class PredictModel:

    def __init__(self):
        self.ensemble = []
        self.n_class=0
        self.n_model=0
    def fit(self, X, y):
        class_ids = range(len(set(y)))
        self.n_class=len(set(y))
        X = np.array(X)
        y = np.array(y)
        self.n_model=min(self.n_class,10)
        splitter = model_selection.KFold(n_splits=self.n_model, random_state=107,shuffle=True)
        for know_class, novelty_class in splitter.split(class_ids):
            model = NoveltyDetectionSingle(know_class, novelty_class)
            print(len(self.ensemble) + 1)
            model.fit(X, y)
            self.ensemble.append(model)
        log=LogisticRegression(random_state=23,solver='lbfgs',class_weight='balanced',multi_class='multinomial',max_iter=100)
        log.fit(X, y)
        self.svc=log
    def predict(self, X):
        ret = []
        for seq in X:
            y_pred_proba = self.svc.predict_proba(seq)
            label=self.svc.predict(seq)
            #y_pred_proba = bn.median(y_pred_proba, axis=0)
            y_pred_proba = np.mean(y_pred_proba, axis=0)
            y_pred = np.argmax(y_pred_proba)
            proba = np.max(y_pred_proba)
            count = 0
            for model in self.ensemble:
                if y_pred in model.set_known_class:
                    count += model.predict([seq])[0]
            ret.append(count)
        return ret,label
