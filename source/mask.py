import glob
import os
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image


def rock_formula(bands):
    b1 = bands[0]
    b2 = bands[1]
    b3 = bands[2]
    if (b1 < b2) and (b1 < b3) and (b3 >= b2) and (b3 - b2 <= 5) and (b2 >= 165):
        mask_value = 1
    else:
        mask_value = 0
    return mask_value


def get_segmentation_mask_df(image_path, formula):
    image = Image.open(image_path)
    image_arr = np.array(image)
    height, width = image_arr.shape[:2]

    mask_list = []
    for img_v, img_u in product(range(height), range(width)):
        bands = image_arr[img_v, img_u]
        mask_value = formula(bands)
        mask_list.append([img_u, img_v, mask_value])

    mask_df = pd.DataFrame(np.array(mask_list), columns=['img_u', 'img_v', 'mask_value'])
    return mask_df

if __name__ == '__main__':

    data_dir = os.path.abspath("data/images")
    images_paths_list = sorted(glob.glob(os.path.join(data_dir, "*.tif")))

    image_idx = 0
    image_path = images_paths_list[image_idx]
    image_name = image_path.split("\\")[-1].split(".")[0]

    # mask_df = get_segmentation_mask_df(image_path, rock_formula)

    save_dir = os.path.abspath("output/masks")
    # os.makedirs(save_dir, exist_ok=True)
    # mask_df.to_csv(os.path.join(save_dir, image_name + ".csv"), index=False)

	### read from file and plot mask
    mask_df = pd.read_csv(os.path.join(save_dir, image_name + ".csv"))
    mask_df = mask_df[mask_df.mask_value == 1]
    plt.figure()
    plt.scatter(mask_df["img_u"].to_numpy(), mask_df["img_v"].to_numpy())
    plt.show()
