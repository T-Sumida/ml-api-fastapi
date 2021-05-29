# -*- coding:utf-8 -*-

from pydantic import BaseModel


class PredictionResult(BaseModel):
    name: str
