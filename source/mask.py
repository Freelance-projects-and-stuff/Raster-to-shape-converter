import glob
import os
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spectral as sp
from PIL import Image

from source.formulas import ndvi, rock_formula


def get_segmentation_mask_df(image_path, formula, loader="PIL"):
    if loader == "PIL":
        image = Image.open(image_path)
        image_arr = np.array(image)
    elif loader == "spectral":
        image = sp.envi.open(image_path)
        image_arr = image[:,:,:]
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
    images_paths_list = sorted(glob.glob(os.path.join(data_dir, "*.hdr")))

    image_idx = 0
    image_path = images_paths_list[image_idx]
    image_name = image_path.split("\\")[-1].split(".")[0]

    mask_df = get_segmentation_mask_df(image_path, ndvi, loader="spectral")

    save_dir = os.path.abspath("output/masks")
    os.makedirs(save_dir, exist_ok=True)
    mask_df.to_csv(os.path.join(save_dir, image_name + ".csv"), index=False)
