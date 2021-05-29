# -*- coding:utf-8 -*-

# モデル作成用スクリプト

from tensorflow.keras.applications.resnet50 import ResNet50

if __name__ == "__main__":
    model = ResNet50(weights='imagenet')
    print(model.summary())
    model.save("./models/")
    print("model output to \"./models\"")
