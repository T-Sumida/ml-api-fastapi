# -*- coding:utf-8 -*-

# モデル作成用スクリプト

import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50

if __name__ == "__main__":
    model = ResNet50(weights='imagenet')
    print(model.summary())
    model.save("./static/model/resnet_imagenet.h5")
    print("model output to \"static/model/resnet_imagenet.h5\"")
