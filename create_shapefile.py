
import glob
import os
import geopandas as gpd
import pandas as pd

from source.coordinates import get_coordinates_df
from source.mask import get_segmentation_mask_df
from source.formulas import rock_formula


def get_merged_gdf(coor_df, mask_df):
    merged_df = pd.concat([coor_df[["gps_x", "gps_y"]], mask_df["mask_value"]], axis=1)
    merged_df = merged_df[merged_df.mask_value == 1][["gps_x", "gps_y"]]
    data_gdf = gpd.GeoDataFrame(merged_df,
                    geometry = gpd.points_from_xy(merged_df['gps_x'], merged_df['gps_y']))
    return data_gdf


data_dir = "data/images"
save_dir = "output/shape_files"

data_dir = os.path.abspath(data_dir)
save_dir = os.path.abspath(save_dir)
images_paths_list = sorted(glob.glob(os.path.join(data_dir, "*.tif")))
os.makedirs(save_dir, exist_ok=True)

# image_idx = 0
# image_path = images_paths_list[image_idx]

for image_path in images_paths_list:
    image_name = image_path.split("\\")[-1].split(".")[0]

    print(f"Processed image: {image_name}")
    print("Extracting coordinates...")
    coor_df = get_coordinates_df(image_path)
    print("Done.")
    print("Extracting masks...")
    mask_df = get_segmentation_mask_df(image_path, rock_formula)
    print("Done.")
    print("Saving shape file...")
    data_gdf = get_merged_gdf(coor_df, mask_df)
    data_gdf.to_file(filename=os.path.join(save_dir, image_name + ".shp"), driver='ESRI Shapefile')
    print("Done.")
