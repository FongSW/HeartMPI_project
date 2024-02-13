import numpy as np
import pandas as pd
import pydicom as dicom
import cv2, os
from glob import glob
from numpy import save 
from app.utility_function.qualitative.cropped_image.crop_region_vessel import crop_vessel
from dotenv.main import load_dotenv

# load .env variables
load_dotenv()


def save_cropped_polar(save_folder, hn, test_status, num, im_array):

    status = {"s": "stress", "r":"rest"}
    polar_type = {"1":"perfusion", "2":"severity", "0b":"blackout", "0d":"def-severity"}

    # app/attempt/{hn}/temp/cropped_images
    # /opt/hearmpi-front-web/data/4dm-mpi/{hn}/temp/cropped_images
    save_path = f"{save_folder}/cropped_images/{status[test_status[0]]}/{polar_type[num]}/{hn}_{polar_type[num]}.npy"
    save(save_path, im_array)
    print(f">>>>> save crop img: {save_path}")
    return save_path

def crop_polar(hn, test_status, path_img):
    # SS,RS -> perfusion, severity 2 รูปนี้จะตัดออกมาได้ 2 รูปย่อย
    # SB,RB -> Black out
    # SD,RD -> Def serverity
    save_folder = "/".join(path_img.split("/")[:-1])
    save_lst = list()
    try:
        im = dicom.read_file(path_img)
        im = im.pixel_array
    except Exception as e:
        print(e)
        raise Exception(e)
        
    if 'ss' in path_img or 'rs' in path_img:
        for lop in range(1,3):
            if lop == 1:
                shiftr = 0
            if lop == 2: 
                shiftr = 272
            # crop 
            left = 217 + shiftr
            top = 194 
            right = 429 + shiftr
            bottom = 406
            imcut = im[top:bottom, left:right]

            # clean text
            imcut[:15,:42] = 0
            imcut[:15,200:] = 0
            imcut[185:220,:32] = 0
            imcut[185:220,190:] = 0
            imcut = cv2.resize(imcut, (224, 224), interpolation = cv2.INTER_AREA)
            save_path = save_cropped_polar(save_folder, hn, test_status, str(lop), imcut)
            save_lst.append(save_path)
    
    else:
        # crop 
        left = 489
        top = 194 
        right = 701
        bottom = 406
        im = im[top:bottom, left:right]

        # clean text
        im[:15,:42] = 0
        im[:15,200:] = 0
        im[185:220,:32] = 0
        im[185:220,190:] = 0
        im = cv2.resize(im, (224, 224), interpolation = cv2.INTER_AREA)
        save_path = save_cropped_polar(save_folder, hn, test_status, f"0{test_status[1]}", im)
        save_lst.append(save_path)
    
    return save_lst


def prepare_img(hn, file_path):

    # file path : /opt/heartmpi-front-web/data/4dm-mpi/{hn_number}/temp/
    # real save path : /opt/hearmpi-front-web/data/4dm-mpi/048278-46/temp/cropped_images

    # change format path
    file_path = file_path.replace("\\", "/")
    
    # create save folders
    print("-"*25, "Create save folders", "-"*25)
    cropped_path = f"{file_path}/cropped_images"
    lab_type = ["stress", "rest"]
    polar_type = ["perfusion", "severity", "blackout", "def-severity"]
    if not os.path.exists(cropped_path):
        for i in lab_type:
            for j in polar_type:
                save_path = f"{cropped_path}/{i}/{j}"
                os.makedirs(save_path)
                print(f">>>>> The new directory: {save_path} was created!")
    else:
        print(f">>>>> The directory {cropped_path} is exit.")

    # crop polar map
    print("-"*25, "Cropped polar map", "-"*25)
    all_polar_path = list()
    for f in glob(file_path + "/*.dcm"):
        test_type = (f.split("/")[-1].split(".")[0])
        if ("sis" != test_type) and ("ris" != test_type):
            save_path = crop_polar(hn, test_type, f)
            for i in save_path:
                all_polar_path.append(i)

    # crop vessels
    print("-"*25, "Cropped vessels", "-"*25)
    cropped_mask_path = os.environ['MASK_PATH']
    mask_path = [
        f'{cropped_mask_path}/LAD_224_Mask.jpg',
        f'{cropped_mask_path}/LCX_224_Mask.jpg',
        f'{cropped_mask_path}/RCA_224_Mask.jpg'
    ]
    vessel = ['lad', 'lcx', 'rca']


    # crop_vessel(polar_path, mask_path, cropped_path, hn, vessel)
    all_vessel_path = dict()
    for polar_path in all_polar_path:
        save_vessel_path =  "/".join([item for item in polar_path.split('/')[:-1]])
        for i in range(len(mask_path)):
            crop_vessel(polar_path, mask_path[i], save_vessel_path, hn, vessel[i])
            all_vessel_path["_".join(polar_path.split('/')[-3:-1:1])] = save_vessel_path

    return all_vessel_path