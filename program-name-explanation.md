- 2020/8/9 REVISIONS:
    - sentinel2.py
        - Sentinel2_get_sorted_data
        - Sentinel2_get_all_data

    - sentinel-test52-tokyo.ipynb
        - Create timelapse 
        - Sort data based on cloudcoverpercentage
        - Get 1 scene each month
        - Sentinel2_get_sorted_data() -> Sentinel2_get_all_data()

    - sentinel-test53-sapporo.ipynb
        - Create timelapse. Resolution 60, 2019/8 - 2020/7
        - Sort data based on cloudcoverpercentage
        - Get 1 scene each month
        - Sentinel2_get_sorted_data() -> Sentinel2_get_all_data()

    - sentinel-test60-tokyo.ipynb
        - Create timelapse. Resolution 10, 2020/6 (6periods)
        - Get all data between start_date and end_date
        - Sentinel2_get_all_data(products_gdf_sorted, index, fontfile, object_name, start_date, resolution)

    - sentinel-test61-sapporo.ipynb
        - Create timelapse. Resolution 60, 2020/1 - 2020/7, cloudcover 0-70
        - Get all data between start_date and end_date
        - Sentinel2_get_all_data(products_gdf_sorted, index, fontfile, object_name, start_date, resolution)
