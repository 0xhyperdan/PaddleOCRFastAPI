# -*- coding: utf-8 -*-

import os

import requests
from fastapi import APIRouter, HTTPException, UploadFile, status
import numpy as np
from paddleocr import PaddleOCR
from typing import Any

from models.OCRModel import *
from models.RestfulModel import *
from utils.ImageHelper import base64_to_ndarray, bytes_to_ndarray

OCR_LANGUAGE = os.environ.get("OCR_LANGUAGE", "ch")

router = APIRouter(prefix="/ocr", tags=["OCR"])

ocr = PaddleOCR(
    use_doc_orientation_classify=False,  # 通过 use_doc_orientation_classify 参数指定不使用文档方向分类模型
    use_doc_unwarping=False,  # 通过 use_doc_unwarping 参数指定不使用文本图像矫正模型
    use_textline_orientation=False,  # 通过 use_textline_orientation 参数指定不使用文本行方向分类模型
    lang=OCR_LANGUAGE,  # 通过 lang 参数指定使用的语言模型
)


def _to_serializable(value: Any) -> Any:
    """递归将 numpy 类型转换为可序列化的 Python 基本类型"""
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (list, tuple)):
        return [_to_serializable(item) for item in value]
    if isinstance(value, dict):
        return {key: _to_serializable(val) for key, val in value.items()}
    return value


@router.get("/predict-by-path", response_model=RestfulModel, summary="识别本地图片")
def predict_by_path(image_path: str):
    result = _to_serializable(ocr.ocr(image_path))
    restfulModel = RestfulModel(
        resultcode=200, message="Success", data=result, cls=OCRModel
    )
    return restfulModel


@router.post(
    "/predict-by-base64", response_model=RestfulModel, summary="识别 Base64 数据"
)
def predict_by_base64(base64model: Base64PostModel):
    img = base64_to_ndarray(base64model.base64_str)
    result = _to_serializable(ocr.ocr(img=img))
    restfulModel = RestfulModel(
        resultcode=200, message="Success", data=result, cls=OCRModel
    )
    return restfulModel


@router.post("/predict-by-file", response_model=RestfulModel, summary="识别上传文件")
async def predict_by_file(file: UploadFile):
    restfulModel: RestfulModel = RestfulModel()
    if file.filename.endswith((".jpg", ".png")):  # 只处理常见格式图片
        restfulModel.resultcode = 200
        restfulModel.message = file.filename
        file_data = file.file
        file_bytes = file_data.read()
        img = bytes_to_ndarray(file_bytes)
        result = _to_serializable(ocr.ocr(img=img))
        restfulModel.data = result
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请上传 .jpg 或 .png 格式图片",
        )
    return restfulModel


@router.get("/predict-by-url", response_model=RestfulModel, summary="识别图片 URL")
async def predict_by_url(imageUrl: str):
    restfulModel: RestfulModel = RestfulModel()
    response = requests.get(imageUrl)
    image_bytes = response.content
    if image_bytes.startswith(b"\xff\xd8\xff") or image_bytes.startswith(
        b"\x89PNG\r\n\x1a\n"
    ):  # 只处理常见格式图片 (jpg / png)
        restfulModel.resultcode = 200
        img = bytes_to_ndarray(image_bytes)
        result = _to_serializable(ocr.ocr(img=img))
        restfulModel.data = result
        restfulModel.message = "Success"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请上传 .jpg 或 .png 格式图片",
        )
    return restfulModel
