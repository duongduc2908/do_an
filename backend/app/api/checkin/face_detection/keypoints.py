from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from face_detection.face_detection import onet
import numpy as np
import cv2


def get_keypoints(img):
    h, w = img.shape[:2]
    total_boxes = np.array([[0, 0, w, h, 1]])
    img = cv2.resize(img, (48,48))
    tempimg = np.expand_dims(img, axis=3)
    tempimg = (tempimg-127.5)*0.0078125
    tempimg1 = np.transpose(tempimg, (3,1,0,2))
    out = onet(tempimg1)
    out0 = np.transpose(out[0])
    out1 = np.transpose(out[1])
    out2 = np.transpose(out[2])
    score = out2[1,:]
    points = out1
    ipass = np.where(score>0)
    points = points[:,ipass[0]]
    total_boxes = np.hstack([total_boxes[ipass[0],0:4].copy(), np.expand_dims(score[ipass].copy(),1)])
    mv = out0[:,ipass[0]]

    w = total_boxes[:,2]-total_boxes[:,0]+1
    h = total_boxes[:,3]-total_boxes[:,1]+1
    points[0:5,:] = np.tile(w,(5, 1))*points[0:5,:] + np.tile(total_boxes[:,0],(5, 1))-1
    points[5:10,:] = np.tile(h,(5, 1))*points[5:10,:] + np.tile(total_boxes[:,1],(5, 1))-1
    points = np.array([points[:,i].reshape((2,5)).T for i in range(points.shape[1])])
    return np.array(points[0])


if __name__ == '__main__':
    from face_detection.face_detection import detect_face
    import sys 
    import imageio 
    import cv2 
    import time

    image = imageio.imread(sys.argv[1])
    bbs, points = detect_face(image)
    l,t,r,b = bbs[0]
    face = image[t:b,l:r]
    for i in range(5):
        prev = time.time()
        kpoints = get_keypoints(face)
        print(time.time() - prev)
    for x, y in kpoints:
        cv2.circle(face, (x,y), 3, (0,255,0), -1)
    cv2.imshow('test', face[:,:,::-1])
    cv2.waitKey(0)
