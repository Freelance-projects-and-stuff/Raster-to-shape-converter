import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spectral as sp

from source.utils import get_coordinates_df, save_coordinates

data_dir = os.path.abspath("data/images")
images_paths_list = sorted(glob.glob(os.path.join(data_dir, "*.tif")))

image_idx = 0
image_path = images_paths_list[image_idx]
image_name = image_path.split("\\")[-1].split(".")[0]

coor_df = get_coordinates_df(image_path)

save_dir = os.path.abspath("output/coordinates")
os.makedirs(save_dir, exist_ok=True)
coor_df.to_csv(os.path.join(save_dir, image_name + ".csv"), index=False)



