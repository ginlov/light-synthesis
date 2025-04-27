import os
import json
import PIL.Image
import numpy as np

import PIL;

def get_crop_param(basedir: str, camera_id: str, timestep: str):
    # Define the path to the crop parameters file
    annot_file = os.path.join(basedir, 'annots', camera_id, f'{timestep}_img.json')

    # Check if the file exists
    if not os.path.exists(annot_file):
        raise FileNotFoundError(f"Crop parameter file not found: {annot_file}")

    # Load the crop parameters from the JSON file
    with open(annot_file, 'r') as f:
        annot = json.load(f)

    eps = 30 # eps to fully cover the object
    crop_param = annot['annots'][0]['bbox'][:-1]
    crop_param[0] = max(0, crop_param[0] - eps)
    crop_param[1] = max(0, crop_param[1] - eps)
    crop_param[2] = min(annot['width'], crop_param[2] + eps)
    crop_param[3] = min(annot['height'], crop_param[3] + eps)
    crop_param = np.array(crop_param) / 2
    crop_param = crop_param.astype(int)

    # Adjust width and height to be divisible by 64
    crop_param[2] = crop_param[0] + ((crop_param[2] - crop_param[0]) // 64) * 64
    crop_param[3] = crop_param[1] + ((crop_param[3] - crop_param[1]) // 64) * 64
    
    return crop_param.astype(int) # As note in the paper, the image is downsampled by 2

def crop_img(basedir: str, camera_id: str, timestep: str) -> PIL.Image:
    # Get the crop parameters
    crop_param = get_crop_param(basedir, camera_id, timestep)

    # Define the path to the image file
    img_file = os.path.join(basedir, 'images_lr', camera_id, f'{timestep}_img.jpg')
    mask_file = os.path.join(basedir, 'fmask_lr', camera_id, f'{timestep}_img_fmask.png')

    # Read image and mask
    img = PIL.Image.open(img_file)
    mask = PIL.Image.open(mask_file)

    width, height = img.size

    # Crop
    img = np.array(img.crop(crop_param))
    mask = np.array(mask.crop(crop_param))

    # Mask image
    mask = mask / 255
    masked_img = img * mask.reshape(*mask.shape, 1).astype(np.uint8)

    return PIL.Image.fromarray(masked_img), crop_param, width, height

def fill_to_orginal_image(cropped_img: PIL.Image, crop_param: np.ndarray, width: int, height: int):
    # Create a new image with the original size
    new_img = PIL.Image.new('RGB', (width, height), (0, 0, 0))

    # Convert crop_param to integers for pasting
    left = int(crop_param[0])
    top = int(crop_param[1])  # 'bottom' in crop_param corresponds to 'top' in image coordinates

    # Paste the cropped image into the new image at the original position
    new_img.paste(cropped_img, (left, top))

    return new_img
