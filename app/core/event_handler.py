# -*- coding:utf-8 -*-

from typing import Callable
from logging import getLogger

from fastapi import FastAPI

from app.core.config import MODEL_PATH, IMG_SIZE
from app.services.models import ImageClassificationModel


logger = getLogger(__name__)


def _startup_model(app: FastAPI) -> None:
    model_instalce = ImageClassificationModel(MODEL_PATH, IMG_SIZE)
    app.state.model = model_instalce


def _shutdown_model(app: FastAPI) -> None:
    app.state.model = None


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Running app start handler.")
        _startup_model(app)
    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")
        _shutdown_model(app)
    return shutdown
