import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread
from numpy import load, save

def crop_vessel(img_path, mask_path, save_vessel_path, hn, vessel): #cut to per vessel

    mask_im     = imread(mask_path, cv2.IMREAD_GRAYSCALE)
    _, mask_val = cv2.threshold(mask_im, thresh=180, maxval=255, type=cv2.THRESH_BINARY)

    # img = imread(img_path) #or array of each pic $img = img_path
    img = cv2.resize(load(img_path), (212, 212))
    main_im_x, main_im_y, _ = img.shape


    def mask(mask, main_im_x, main_im_y,):
        mask_x, mask_y, _ = mask.shape

        x_vessel = min(main_im_x, mask_x)
        x_half_vessel = mask.shape[0]//2

        heart_mask = mask[x_half_vessel-x_vessel//2 : x_half_vessel+x_vessel//2+1, :main_im_y]
        # plt.imshow(heart_mask, cmap='Greys_r')
        # plt.show()

        img_width_half = img.shape[1]//2
        img_to_mask = img[: ,img_width_half-x_half_vessel:img_width_half+x_half_vessel]

        # print("temple_to_mask", img_to_mask.shape)
        # print("heart_mask", heart_mask.shape)
        # masked = cv2.bitwise_and(temple_to_mask,heart_mask, mask = None)
        masked = cv2.bitwise_and(img_to_mask, heart_mask, mask = None)
        imcut = cv2.resize(masked, (224, 224), interpolation = cv2.INTER_AREA)

        return imcut
    
    imcut = mask(mask_im, main_im_x, main_im_y)
    
    if vessel == 'lad':
        imcut = imcut[:135,:169]

    elif vessel == 'lcx':
        imcut = imcut[55:195,138:]

    elif vessel == 'rca':
        imcut = imcut[121:,5:148]

    # save imcut
    save_path = f"{save_vessel_path}/{hn}_{vessel}.npy"
    save(save_path, imcut)
    print(f">>>>> save crop img: {save_path}, \tshape: {imcut.shape}")