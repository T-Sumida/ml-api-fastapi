# -*- coding: utf-8 -*-
import io
from typing import Dict, List, BinaryIO, Tuple
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import decode_predictions
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

# 画像認識モデルの用意
global model, graph
graph = tf.get_default_graph()
model = tf.keras.models.load_model("./static/model/resnet_imagenet.h5")

# FastAPIの用意
app = FastAPI()

# static/js/post.jsをindex.htmlから呼び出すために必要
app.mount("/static", StaticFiles(directory="static"), name="static")

# templates配下に格納したindex.htmlをrenderするために必要
templates = Jinja2Templates(directory="templates")


def read_image(bin_data: BinaryIO, size: Tuple = (224, 224)) -> np.array:
    """画像を読み込む

    Arguments:
        bin_data {bytes} -- 画像のバイナリデータ

    Keyword Arguments:
        size {tuple} -- リサイズしたい画像サイズ (default: {(224, 224)})

    Returns:
        numpy.array -- 画像
    """
    file_bytes = np.asarray(bytearray(bin_data.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, size)
    return img


@app.post("/api/image_recognition")
async def image_recognition(files: List[UploadFile] = File(...)) -> Dict:
    """画像認識API

    Keyword Arguments:
        files {List[UploadFile]} -- アップロードされたファイル情報 (default: {File(...)})

    Returns:
        dict -- 推論結果
    """
    bin_data = io.BytesIO(files[0].file.read())
    img = read_image(bin_data)
    with graph.as_default():
        pred = model.predict(np.expand_dims(img, axis=0))
        result_label = decode_predictions(pred, top=1)[0][0][1]
        return {"response": result_label}


@app.get("/")
async def index(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse("index.html", {"request": request})
