
import glob
import os

import geopandas as gpd
import numpy as np
import pandas as pd
import spectral as sp

from source.coordinates import get_coordinates_df
from source.formulas import gndvi, mcari, ndvi, pssr, rock_formula, wbi
from source.image import save_image
from source.mask import get_segmentation_mask_df


def get_merged_gdf(coor_df, mask_df):
    merged_df = pd.concat([coor_df[["gps_x", "gps_y"]], mask_df["mask_value"]], axis=1)
    # merged_df = merged_df[merged_df.mask_value == 1][["gps_x", "gps_y"]]
    data_gdf = gpd.GeoDataFrame(merged_df,
                    geometry = gpd.points_from_xy(merged_df['gps_x'], merged_df['gps_y']))
    return data_gdf

def change_path_suffix(path, suffix):
    return path.split(".")[0] + "." + suffix



equation = ndvi
data_dir = "data/images"
save_shp_dir = "output/shape_files"
save_img_dir = "output/images"
save_ras_dir = "output/rasters"

data_dir = os.path.abspath(data_dir)
save_shp_dir = os.path.abspath(save_shp_dir)
save_img_dir = os.path.abspath(save_img_dir)
save_ras_dir = os.path.abspath(save_ras_dir)

os.makedirs(save_shp_dir, exist_ok=True)
os.makedirs(save_img_dir, exist_ok=True)
os.makedirs(save_ras_dir, exist_ok=True)

images_paths_list = sorted(glob.glob(os.path.join(data_dir, "*.hdr")))

# image_idx = 2
# image_path = images_paths_list[image_idx]

for image_path in images_paths_list:
    image_name = image_path.split("\\")[-1].split(".")[0]

    print(f"__ Processed image: {image_name} __")
    print("Extracting coordinates...")
    image_coor_path = change_path_suffix(image_path, suffix="dat")
    coor_df = get_coordinates_df(image_coor_path)
    print("Done.")
    print("Extracting masks...")
    image_mask_path = change_path_suffix(image_path, suffix="hdr")
    mask_df, metadata = get_segmentation_mask_df(image_mask_path, equation,
                                        loader="spectral")
    print("Done.")
    print("Saving shape file...")
    data_gdf = get_merged_gdf(coor_df, mask_df)
    data_gdf.to_file(filename=os.path.join(save_shp_dir, image_name + ".shp"),
                        driver='ESRI Shapefile')
    print("Done.")
    print("Saving png file...")
    raster = save_image(mask_df,
                save_path=os.path.join(save_img_dir, image_name + ".png"),
                image_title=equation.__name__)
    print("Done.")
    if metadata:
        print("Saving raster file...")
        metadata["band names"] = 'Value'
        sp.envi.save_image(os.path.join(save_ras_dir, image_name + ".hdr"), raster,
                        metadata=metadata, dtype=np.float32, force=True)
        print("Done.")
