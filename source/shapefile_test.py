import glob
import os

import geopandas as gpd
import pandas as pd




if __name__ == '__main__':

    data_dir = os.path.abspath("data/images")
    images_paths_list = sorted(glob.glob(os.path.join(data_dir, "*.tif")))

    image_idx = 0
    image_path = images_paths_list[image_idx]
    image_name = image_path.split("\\")[-1].split(".")[0]

    masks_dir = os.path.abspath("output/masks")
    coor_dir = os.path.abspath("output/coordinates")

    mask_df = pd.read_csv(os.path.join(masks_dir, image_name + ".csv"))
    coor_df = pd.read_csv(os.path.join(coor_dir, image_name + ".csv"))
    merged_df = pd.concat([coor_df[["gps_x", "gps_y"]], mask_df["mask_value"]], axis=1)

    merged_df = merged_df[merged_df.mask_value == 1]

    save_dir = os.path.abspath("output/merged")
    os.makedirs(save_dir, exist_ok=True)
    merged_df.to_csv(os.path.join(save_dir, image_name + ".csv"), index=False)

	### read from file
    merged_df = pd.read_csv(os.path.join(save_dir, image_name + ".csv"))
    merged_df = merged_df[merged_df.mask_value == 1][["gps_x", "gps_y"]]

    data_gdf = gpd.GeoDataFrame(merged_df,
                    geometry = gpd.points_from_xy(merged_df['gps_x'], merged_df['gps_y']))

    print(type(data_gdf))
    save_dir = os.path.abspath("output/shape_files")
    os.makedirs(save_dir, exist_ok=True)
    # ESRI_WKT = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
    # data_gdf.to_file(filename='data.shp', driver='ESRI Shapefile', crs_wkt='ESRI_WKT')
    data_gdf.to_file(filename=os.path.join(save_dir, image_name + ".shp"), driver='ESRI Shapefile')
