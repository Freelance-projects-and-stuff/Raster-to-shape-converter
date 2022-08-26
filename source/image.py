import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def save_image(mask_df, save_path, image_title=None):
    v_max, u_max = int(mask_df.img_v.max()), int(mask_df.img_u.max())
    image_out = np.zeros((v_max+1, u_max+1))
    image_out[mask_df.img_v.to_numpy().astype("int"),
              mask_df.img_u.to_numpy().astype("int")] = mask_df.mask_value.to_numpy()
    plt.title(image_title)
    plt.imshow(image_out)
    plt.colorbar()
    plt.savefig(save_path)
    plt.close()
    return image_out


if __name__ == '__main__':

    data_dir = os.path.abspath("data/images")
    images_paths_list = sorted(glob.glob(os.path.join(data_dir, "*.hdr")))

    image_idx = 0
    image_path = images_paths_list[image_idx]
    image_name = image_path.split("\\")[-1].split(".")[0]

    masks_dir = os.path.abspath("output/masks")
    save_dir = os.path.abspath("output/images")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, image_name + ".png")

    mask_df = pd.read_csv(os.path.join(masks_dir, image_name + ".csv"))
    image_out = save_image(mask_df, save_path)

