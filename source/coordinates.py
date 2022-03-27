import csv
import glob
import os
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spectral as sp
from osgeo import gdal, osr


def get_coordinates_df(image_path):
    def get_coordinates_from_image(gdal_transform, x_coor, y_coor):
        GT = gdal_transform
        # supposing x_coor and y_coor are your pixel coordinate this
        # is how to get the coordinate in space. Affine transform - see docs
        gps_x = GT[0] + x_coor*GT[1] + y_coor*GT[2]
        gps_y = GT[3] + x_coor*GT[4] + y_coor*GT[5]
        px_w = GT[1]
        px_h = GT[5]
        # shift to the center of the pixel
        gps_x += px_w / 2.0
        gps_y += px_h / 2.0
        return gps_x, gps_y

    gdal_image = gdal.Open(image_path)
    height = gdal_image.RasterYSize
    width = gdal_image.RasterXSize
    gdal_transform = gdal_image.GetGeoTransform()

    coor_list = []
    for img_v, img_u in product(range(height), range(width)):
        gps_x, gps_y = get_coordinates_from_image(gdal_transform, img_u, img_v)
        coor_list.append([img_u, img_v, gps_x, gps_y])

    coor_df = pd.DataFrame(np.array(coor_list), columns=['img_u', 'img_v', 'gps_x', 'gps_y'])
    return coor_df


if __name__ == '__main__':

    data_dir = os.path.abspath("data/images")
    images_paths_list = sorted(glob.glob(os.path.join(data_dir, "*.tif")))

    image_idx = 0
    image_path = images_paths_list[image_idx]
    image_name = image_path.split("\\")[-1].split(".")[0]

    coor_df = get_coordinates_df(image_path)

    save_dir = os.path.abspath("output/coordinates")
    os.makedirs(save_dir, exist_ok=True)
    coor_df.to_csv(os.path.join(save_dir, image_name + ".csv"), index=False)



