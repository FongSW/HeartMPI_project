import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread
from numpy import load, save

def crop_vessel(polar_path, mask_path, cropped_path, hn, vessel):

    # read polar map
    # polar_im = imread(polar_path)
    polar_im = load(polar_path)
    polar_im_x, polar_im_y, _ = polar_im.shape

    # read mask
    mask_im = imread(mask_path, cv2.IMREAD_GRAYSCALE)
    _, mask = cv2.threshold(mask_im, thresh=180, maxval=255, type=cv2.THRESH_BINARY)
    mask_x, mask_y, _ = mask.shape

    # stack mask on polar map
    x_vessel = min(polar_im_x, mask_x)
    x_half_vessel = mask.shape[0] // 2
    heart_mask = mask[x_half_vessel - (x_vessel//2) : (x_half_vessel + (x_vessel//2)) + 1,]

    polar_im_half = polar_im.shape[0] // 2
    polar_to_mask = polar_im[:, polar_im_half-x_half_vessel:polar_im_half+x_half_vessel]

    print("polar_to_mask", polar_to_mask.shape)
    print("heart_mask", heart_mask.shape)

    masked = cv2.bitwise_and(polar_to_mask, heart_mask, mask = None)
    tmp = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
    b, g, r = cv2.split(masked)
    rgba = [b,g,r, alpha]
    masked_tr = cv2.merge(rgba,4)

    # plt.imshow(masked_tr)
    # plt.show()

    # save img
    save_path = f"{cropped_path}/{hn}_{vessel}.npy"
    # cv2.imwrite(save_path, cv2.cvtColor(masked_tr, cv2.COLOR_BGR2RGB))
    save(save_path, masked_tr)
    print(f">>>>> save crop img {save_path}")