from fastapi import APIRouter, Form, File, UploadFile
from generator import stargan_generator, resunet_generator
from fastapi.responses import FileResponse
from PIL import Image
import io
import numpy as np
import cv2
from urllib.parse import unquote
import os

image = APIRouter()
api_url_get = 'http://127.0.0.1:8000/images?name='


@image.get('/images')
async def get_image_by_path(name: str):
    try:
        path = os.path.join(os.path.dirname(__file__), '../', name)
        return FileResponse(unquote(path), media_type="image/png")
    except Exception as e:
        print(e)
        return None
    
@image.post('/generate/input_target_contrast')
async def generate_image_faster(dataset: str='IXI', source_contrast: str = 't1', target_contrast: str = 't2'):
    try:
        source_path, generated_path, ground_truth_path, ssim, psnr, nmae = stargan_generator.generate_faster(dataset, source_contrast, target_contrast)
        return {
            "source_path": api_url_get + source_path, 
            "generated_path": api_url_get + generated_path, 
            "ground_truth_path": api_url_get + ground_truth_path, 
            "ssim": ssim, 
            "psnr": psnr, 
            "nmae": nmae,
            "source_contrast": source_contrast,
            "target_contrast": target_contrast
        }
    
    except Exception as e:
        print(e)
        return None
    

@image.post('/generate/uploaded_file')  
async def generate_from_uploaded_image(file: UploadFile = File(...), dataset: str = 'IXI', src_contrast: str = 't1', trg_contrast: str = 't2'):
    try:
        print(file.filename)
        print(dataset, src_contrast, trg_contrast)
        source_path, generated_path, ground_truth_path, ssim, psnr, nmae = stargan_generator.generate_from_uploaded_image(dataset, file.filename, src_contrast, trg_contrast)
        return {
            "source_path": api_url_get + source_path, 
            "generated_path": api_url_get + generated_path, 
            "ground_truth_path": api_url_get + ground_truth_path,
            "ssim": ssim, 
            "psnr": psnr, 
            "nmae": nmae,
            "source_contrast": src_contrast,
            "target_contrast": trg_contrast
        }
    except Exception as e:
        print(e)
    finally:
        await file.close()
    return None


    