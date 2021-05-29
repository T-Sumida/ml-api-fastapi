# -*- coding:utf-8 -*-
from logging import getLogger
from typing import BinaryIO

import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import decode_predictions

from app.models.prediction import PredictionResult


logger = getLogger(__name__)


class ImageClassificationModel(object):
    def __init__(self, model_path: str, size: int) -> None:
        """init
        Args:
            tracking_url (str): mlflow uri
            model_name (str): model name of mlflow
            size (int): target image size
        """
        self.size = size
        self._load_model(model_path)

    def _load_model(self, model_path: str) -> None:
        """load model"""
        logger.info(f"load model in {model_path}")
        self.model = tf.keras.models.load_model(model_path)
        logger.info("initialized model")

    def _pre_process(self, bin_data: BinaryIO) -> np.array:
        """preprocess
        Args:
            bin_data (BinaryIO): binary image data
        Returns:
            np.array: image data
        """
        file_bytes = np.asarray(bytearray(bin_data.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.size, self.size))
        return img

    def _post_process(self, prediction: np.array) -> PredictionResult:
        """post process
        Args:
            prediction (np.array): result of predict
        Returns:
           PredictionResult: prediction
        """
        result_label = decode_predictions(prediction, top=1)[0][0][1]
        dcp = PredictionResult(name=result_label)
        return dcp

    def _predict(self, img: np.array) -> np.array:
        """predict
        Args:
            img (np.array): image data
        Returns:
            np.array: prediction
        """
        prediction_result = self.model.predict(np.expand_dims(img, axis=0))
        return prediction_result

    def predict(self, bin_data: BinaryIO) -> PredictionResult:
        """predict method
        Args:
            bin_data (BinaryIO): binary image data
        Returns:
            PredictionResult: prediction
        """
        img = self._pre_process(bin_data)
        result = self._predict(img)
        post_processed_result = self._post_process(result)
        return post_processed_result
