from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import time
import cv2
import numpy as np
import time
import os
from shutil import copyfile

import argparse
import sys
import time
import os
import operator
import tensorflow as tf
import numpy as np

class Classify():
    def __init__(self):
        self.name = "AccidentImageClassifier"

    def load_graph(self,model_file):
        graph = tf.Graph()
        graph_def = tf.GraphDef()

        with open(model_file, "rb") as f:
            graph_def.ParseFromString(f.read())
        with graph.as_default():
            tf.import_graph_def(graph_def)

        return graph

    def read_tensor_from_image_file(self,file_name, input_height=299, input_width=299,input_mean=0, input_std=255):
        input_name = "file_reader"
        output_name = "normalized"
        file_reader = tf.read_file(file_name, input_name)
        if file_name.endswith(".png"):
            image_reader = tf.image.decode_png(file_reader, channels = 3,
                                               name='png_reader')
        elif file_name.endswith(".gif"):
            image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                          name='gif_reader'))
        elif file_name.endswith(".bmp"):
            image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
        else:
            image_reader = tf.image.decode_jpeg(file_reader, channels = 3,name='jpeg_reader')
        float_caster = tf.cast(image_tfreader, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0)
        resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
        normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
        sess = tf.Session()
        result = sess.run(normalized)

        return result

    def load_labels(self,label_file):
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
        return label

    def classify_image(self,path):
        image_path = path
        input_height = 224
        input_width = 224
        input_mean = 128
        input_std = 128
        input_layer = "input"
        output_layer = "final_result"
        model_file = os.join(BASE_DIR,'PredictAccident/retrained_graph.pb')
        label_file = os.join(BASE_DIR,'PredictAccident/retrained_labels.txt')

        graph = self.load_graph(model_file)
        t = self.read_tensor_from_image_file(image_path,input_height=input_height,input_width=input_width,input_mean=input_mean,input_std=input_std)

        input_name = "import/" + input_layer
        output_name = "import/" + output_layer
        input_operation = graph.get_operation_by_name(input_name)
        output_operation = graph.get_operation_by_name(output_name)
        with tf.Session(graph=graph) as sess:
            start = time.time()
            results = sess.run(output_operation.outputs[0],{input_operation.outputs[0]: t})
            end=time.time()
        results = np.squeeze(results)
        top_k = results.argsort()[-5:][::-1]
        labels = self.load_labels(label_file)

        template = "{} (score={:0.5f})"
        classPred = {}
        for i in top_k:
            classPred[labels[i]] = results[i]
        ans = max(classPred, key=classPred.get)
        return ans, classPred[ans]


        def predict_accident(self,path):
            class_name, percentage = self.classify_image(path)
            if (class_name[0] is 'a' or class_name[0] is 'A'):
                return 1
            else:
                return 0




