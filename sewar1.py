import cv2
import numpy as np
from sewar import full_ref
from skimage import measure, metrics

ref_img = cv2.imread("original_lenna_grey.png", 1)
img = cv2.imread("original_lenna_grey_blur.png", 1)

rmse_skimg = metrics.normalized_root_mse(ref_img, img)
print(rmse_skimg)

from skimage.metrics import structural_similarity as ssim

ssim_skimg = ssim(ref_img, img, data_range=img.max()-img.min(), channel_axis=2)
print(ssim_skimg)