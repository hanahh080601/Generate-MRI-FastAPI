from fastapi import APIRouter, Form, File, UploadFile
from generator import generator
from fastapi.responses import FileResponse
from PIL import Image
import io
import numpy as np
import cv2

image = APIRouter()

@image.get('/')
async def list_random_images():
    pass

# @image.post('/generate_all')
# async def generate_image(source_contrast: str = 't1', target_contrast: str = 't2'):
#     try:
#         source_path, generated_path, ground_truth_path, ssim, psnr, nmae = generator.generate(source_contrast, target_contrast)
#         return {
#             "source_path": source_path, 
#             "generated_path": generated_path, 
#             "ground_truth_path": ground_truth_path, 
#             "ssim": ssim, 
#             "psnr": psnr, 
#             "nmae": nmae
#         }
#     except Exception as e:
#         print(e)
#         return None

@image.post('/generate_with_target_contrast')
async def generate_image(source_contrast: str = 't1', target_contrast: str = 't2'):
    try:
        source_path, generated_path, ground_truth_path, ssim, psnr, nmae = generator.generate(source_contrast, target_contrast)
        return {
            "source_path": source_path, 
            "generated_path": generated_path, 
            "ground_truth_path": ground_truth_path, 
            "ssim": ssim, 
            "psnr": psnr, 
            "nmae": nmae
        }
    
    except Exception as e:
        print(e)
        return None
    

@image.post('/generate_from_uploaded_file')  
async def generate_from_uploaded_image(file: UploadFile = File(...), src_contrast: str = 't1', trg_contrast: str = 't2'):
    try:
        print(file.filename)
        contents = await file.read()
        # print(contents)
        img = Image.open(io.BytesIO(contents))
        # pred = prediction.predict(img)
    except Exception as e:
        print(e)
    finally:
        await file.close()
    return None
    