from feature_extraction.face_model import get_input

from face_detection import keypoints
import tensorflow.compat.v1 as tf 
import sklearn.preprocessing
import numpy as np
import os 


class FaceVector:
    def __init__(self, model_type=34):
        #current_path = os.path.abspath(os.path.dirname(__file__))
        #frozen_graph_path = os.path.join(current_path, 'models/fv_model_{}.pb'.format(model_type))
        frozen_graph_path='models/fv_model_34.pb'
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.sess = tf.Session()
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(frozen_graph_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
                self.tinput = self.graph.get_tensor_by_name("data:0")
                self.toutput = self.graph.get_tensor_by_name("fc1/add_1:0")

        # with tf.Graph().as_default() as self.graph:
        #     with tf.Session().as_default() as self.sess:
        #         model_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'models/tf_resnet{}'.format(model_type))
        #         tf.saved_model.load(self.sess, ['serve'], model_path)
        #         self.tinput = self.graph.get_tensor_by_name("data:0")
        #         self.toutput = self.graph.get_tensor_by_name("fc1/add_1:0")


    def get_vector(self, rgb_img, bb=None, point=None):
        if bb is None:
            h, w = rgb_img.shape[:2]
            bb = [0, 0, w, h]
        if point is None:
            l,t,r,b = bb 
            face = rgb_img[t:b,l:r]
            point = keypoints.get_keypoints(face)
            point = np.array([[l+x, t+y] for x, y in point])
        img = get_input(rgb_img, bb, point)
        img = np.transpose(img, (1,2,0))
        with self.graph.as_default():
            with self.sess.as_default():
                output = self.sess.run(self.toutput, {self.tinput: [img]})
        output = sklearn.preprocessing.normalize(output).flatten()
        return output
