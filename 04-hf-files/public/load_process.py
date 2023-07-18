import ee
import geemap
import geopandas as gpd
import os
import sys


# Get the path to the "public" directory
public_path = os.path.dirname(__file__)

# Add the "public" directory to the Python path
sys.path.append(public_path)

from functions import ImageFunctions

class ImageProcess:
    def __init__(self, map_instance) -> None:
        self.map_instance = map_instance
        self.image_functions = ImageFunctions()



    def load_and_process_true(self, map_instance, shapefile_path):
            # Load the study area
        print('Loading study boundary')
        study_boundary = gpd.read_file(shapefile_path)
        ee_boundary = geemap.geopandas_to_ee(study_boundary)
        aoi = ee_boundary.geometry()

        vis_params= {
            'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
            'min': 0.0,
            'max': 0.3,
            'gamma': 2.5
            }
        dates = ['2021-11-11', '2021-10-26','2021-10-10', '2021-08-07','2021-07-22', '2021-07-06' ]

        processed_collection = ee.ImageCollection([])

        # Loop through the dates and get the imagery
        for date in dates:

            start_date = ee.Date(date)
            end_date = start_date.advance(1, 'day')

            # Filter the image collection by date and area
            image = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2") \
                .filterDate(start_date, end_date) \
                .filterBounds(ee_boundary) \
                .first()  # get the first image that matches the filters

            if image:  # check if image exists

                optical_bands = image.select('SR_B.*').multiply(0.0000275).add(-0.2)
                clipped_image = optical_bands.clip(aoi)  # Clip the image to the study boundary
                map_instance.addLayer(clipped_image, vis_params, date, shown = True)  # add the image to the map
                processed_collection = processed_collection.merge(clipped_image)  # add the image to the processed collection
            else:
                print(f"No image found for date {date}")



    def load_and_process_chla(self, map_instance, shapefile_path):
        # Load the study area

        study_boundary = gpd.read_file(shapefile_path)
        ee_boundary = geemap.geopandas_to_ee(study_boundary)
        aoi = ee_boundary.geometry()
        TURBO_PALETTE = [
        "30123b", "321543", "33184a", "341b51", "351e58", "36215f", "372466", "38276d", 
        "392a73", "3a2d79", "3b2f80", "3c3286", "3d358b", "3e3891", "3f3b97", "3f3e9c", 
        "4040a2", "4143a7", "4146ac", "4249b1", "424bb5", "434eba", "4451bf", "4454c3", 
        "4456c7", "4559cb", "455ccf", "455ed3", "4661d6", "4664da", "4666dd", "4669e0", 
        "466be3", "476ee6", "4771e9", "4773eb", "4776ee", "4778f0", "477bf2", "467df4", 
        "4680f6", "4682f8", "4685fa", "4687fb", "458afc", "458cfd", "448ffe", "4391fe", 
        "4294ff", "4196ff", "4099ff", "3e9bfe", "3d9efe", "3ba0fd", "3aa3fc", "38a5fb", 
        "37a8fa", "35abf8", "33adf7", "31aff5", "2fb2f4", "2eb4f2", "2cb7f0", "2ab9ee", 
        "28bceb", "27bee9", "25c0e7", "23c3e4", "22c5e2", "20c7df", "1fc9dd", "1ecbda", 
        "1ccdd8", "1bd0d5", "1ad2d2", "1ad4d0", "19d5cd", "18d7ca", "18d9c8", "18dbc5", 
        "18ddc2", "18dec0", "18e0bd", "19e2bb", "19e3b9", "1ae4b6", "1ce6b4", "1de7b2", 
        "1fe9af", "20eaac", "22ebaa", "25eca7", "27eea4", "2aefa1", "2cf09e", "2ff19b", 
        "32f298", "35f394", "38f491", "3cf58e", "3ff68a", "43f787", "46f884", "4af880", 
        "4ef97d", "52fa7a", "55fa76", "59fb73", "5dfc6f", "61fc6c", "65fd69", "69fd66", 
        "6dfe62", "71fe5f", "75fe5c", "79fe59", "7dff56", "80ff53", "84ff51", "88ff4e", 
        "8bff4b", "8fff49", "92ff47", "96fe44", "99fe42", "9cfe40", "9ffd3f", "a1fd3d", "a4fc3c", "a7fc3a", "a9fb39", "acfb38", 
        "affa37", "b1f936", "b4f836", "b7f735", "b9f635", "bcf534", "bef434", "c1f334", 
        "c3f134", "c6f034", "c8ef34", "cbed34", "cdec34", "d0ea34", "d2e935", "d4e735", 
        "d7e535", "d9e436", "dbe236", "dde037", "dfdf37", "e1dd37", "e3db38", "e5d938", 
        "e7d739", "e9d539", "ebd339", "ecd13a", "eecf3a", "efcd3a", "f1cb3a", "f2c93a", 
        "f4c73a", "f5c53a", "f6c33a", "f7c13a", "f8be39", "f9bc39", "faba39", "fbb838", 
        "fbb637", "fcb336", "fcb136", "fdae35", "fdac34", "fea933", "fea732", "fea431", 
        "fea130", "fe9e2f", "fe9b2d", "fe992c", "fe962b", "fe932a", "fe9029", "fd8d27", 
        "fd8a26", "fc8725", "fc8423", "fb8122", "fb7e21", "fa7b1f", "f9781e", "f9751d", 
        "f8721c", "f76f1a", "f66c19", "f56918", "f46617", "f36315", "f26014", "f15d13", 
        "f05b12", "ef5811", "ed5510", "ec530f", "eb500e", "ea4e0d", "e84b0c", "e7490c", 
        "e5470b", "e4450a", "e2430a", "e14109", "df3f08", "dd3d08", "dc3b07", "da3907", 
        "d83706", "d63506", "d43305", "d23105", "d02f05", "ce2d04", "cc2b04", "ca2a04", 
        "c82803", "c52603", "c32503", "c12302", "be2102", "bc2002", "b91e02", "b71d02", 
        "b41b01", "b21a01", "af1801", "ac1701", "a91601", "a71401", "a41301", "a11201", 
        "9e1001", "9b0f01", "980e01", "950d01", "920b01", "8e0a01", "8b0902", "880802", 
        "850702", "810602", "7e0502", "7a0403" ]

        chloro_params= {
        'bands': ['ln_chl_a'],
        'min': 0,
        'max': 3,
        'palette': TURBO_PALETTE
        }
        dates = ['2021-11-11', '2021-10-26','2021-10-10', '2021-08-07','2021-07-22', '2021-07-06' ]

        processed_collection = ee.ImageCollection([])

        # Loop through the dates and get the imagery
        for date in dates:

            start_date = ee.Date(date)
            end_date = start_date.advance(1, 'day')

            # Filter the image collection by date and area
            image = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2") \
                .filterDate(start_date, end_date) \
                .filterBounds(ee_boundary) \
                .first()  # get the first image that matches the filters

            if image:  # check if image exists

                clipped_image = image.clip(aoi)  # Clip the image to the study boundary
                processed_image = map_instance.image_functions.trinh_et_al_chl_a(clipped_image)  # process the image
                map_instance.addLayer(processed_image, chloro_params, date, shown = True)  # add the image to the map
                processed_collection = processed_collection.merge(processed_image)  # add the image to the processed collection
            else:
                print(f"No image found for date {date}")

        # Set the map to focus on the study area

        map_instance.add_colorbar_branca(vis_params= chloro_params, colors = TURBO_PALETTE,vmin =  0, vmax = 3, label = 'mg/m³')



    def load_and_process_spm(self, map_instance, shapefile_path):
            # Load the study area
        
        study_boundary = gpd.read_file(shapefile_path)
        ee_boundary = geemap.geopandas_to_ee(study_boundary)
        aoi = ee_boundary.geometry()
        VIRIDIS_PALETTE = [
        '440154', '440256', '450457', '450559', '46075a', '46085c', '460a5d', '460b5e', '470d60', 
        '470e61', '471063', '471164', '471365', '481467', '481668', '481769', '48186a', '481a6c', 
        '481b6d', '481c6e', '481d6f', '481f70', '482071', '482173', '482374', '482475', '482576', 
        '482677', '482878', '482979', '472a7a', '472c7a', '472d7b', '472e7c', '472f7d', '46307e', 
        '46327e', '46337f', '463480', '453581', '453781', '453882', '443983', '443a83', '443b84', 
        '433d84', '433e85', '423f85', '424086', '424186', '414287', '414487', '404588', '404688', 
        '3f4788', '3f4889', '3e4989', '3e4a89', '3e4c8a', '3d4d8a', '3d4e8a', '3c4f8a', '3c508b', 
        '3b518b', '3b528b', '3a538b', '3a548c', '39558c', '39568c', '38588c', '38598c', '375a8c', 
        '375b8d', '365c8d', '365d8d', '355e8d', '355f8d', '34608d', '34618d', '33628d', '33638d', 
        '32648e', '32658e', '31668e', '31678e', '30688e', '30698e', '2f6a8e', '2f6b8e', '2e6c8e', 
        '2e6d8e', '2d6e8e', '2d6f8e', '2c708e', '2c718e', '2b728e', '2b738e', '2a748e', '2a758e', 
        '29768e', '29778e', '28788e', '28798e', '277a8e', '277b8e', '267c8e', '267d8e', '257e8e', 
        '257f8e', '24808e', '24818e', '23828e', '23828e', '22838e', '22848e', '21858e', '21868e', 
        '20878e', '20888e', '1f898e', '1f8a8d', '1e8b8d', '1e8c8d', '1d8d8d', '1d8e8d', '1c8f8d', 
        '1c8f8d', '1b908c', '1b918c', '1a928c', '1a938b', '19948b', '19958b', '18968a', '18978a', 
        '17988a', '179989', '169a89', '169b88', '159c88', '159d87', '149e87', '149f86', '13a086', 
        '13a185', '12a285', '12a384', '11a483', '11a583', '10a682', '10a781', '0fa881', '0fa980', 
        '0eaa7f', '0eab7e', '0dac7e', '0dad7d', '0cae7c', '0caf7b', '0bb07a', '0bb179', '0ab278', 
        '0ab377', '09b476', '09b575', '08b674', '08b773', '07b872', '07b971', '06ba70', '06bb6f', 
        '05bc6e', '05bd6d', '04be6c', '04bf6b', '03c06a', '03c169', '02c268', '02c367', '01c466', 
        '01c565', '00c664']
        
        spm_params= {
        'bands': ['spm'],
        'min': 0,
        'max': 50,
        'palette': VIRIDIS_PALETTE
        }
        dates = ['2021-11-11', '2021-10-26','2021-10-10', '2021-08-07','2021-07-22', '2021-07-06' ]

        processed_collection = ee.ImageCollection([])

        # Loop through the dates and get the imagery
        for date in dates:
            
            start_date = ee.Date(date)
            end_date = start_date.advance(1, 'day')

            # Filter the image collection by date and area
            image = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2") \
                .filterDate(start_date, end_date) \
                .filterBounds(ee_boundary) \
                .first()  # get the first image that matches the filters

            if image:  # check if image exists

                clipped_image = image.clip(aoi)  # Clip the image to the study boundary
                processed_image = map_instance.image_functions.novoa_et_al_spm(clipped_image)  # process the image
                map_instance.addLayer(processed_image, spm_params, date, shown = True)  # add the image to the map
                processed_collection = processed_collection.merge(processed_image)  # add the image to the processed collection
            else:
                print(f"No image found for date {date}")

        # Set the map to focus on the study area
        map_instance.add_colorbar_branca(vis_params= spm_params, colors = VIRIDIS_PALETTE,vmin =  0, vmax = 50, label = 'g/m³')


    def load_and_process_sst(self, map_instance, shapefile_path):
        # Load the study area

        study_boundary = gpd.read_file(shapefile_path)
        ee_boundary = geemap.geopandas_to_ee(study_boundary)
        aoi = ee_boundary.geometry()
        TURBO_PALETTE = [
        "30123b", "321543", "33184a", "341b51", "351e58", "36215f", "372466", "38276d", 
        "392a73", "3a2d79", "3b2f80", "3c3286", "3d358b", "3e3891", "3f3b97", "3f3e9c", 
        "4040a2", "4143a7", "4146ac", "4249b1", "424bb5", "434eba", "4451bf", "4454c3", 
        "4456c7", "4559cb", "455ccf", "455ed3", "4661d6", "4664da", "4666dd", "4669e0", 
        "466be3", "476ee6", "4771e9", "4773eb", "4776ee", "4778f0", "477bf2", "467df4", 
        "4680f6", "4682f8", "4685fa", "4687fb", "458afc", "458cfd", "448ffe", "4391fe", 
        "4294ff", "4196ff", "4099ff", "3e9bfe", "3d9efe", "3ba0fd", "3aa3fc", "38a5fb", 
        "37a8fa", "35abf8", "33adf7", "31aff5", "2fb2f4", "2eb4f2", "2cb7f0", "2ab9ee", 
        "28bceb", "27bee9", "25c0e7", "23c3e4", "22c5e2", "20c7df", "1fc9dd", "1ecbda", 
        "1ccdd8", "1bd0d5", "1ad2d2", "1ad4d0", "19d5cd", "18d7ca", "18d9c8", "18dbc5", 
        "18ddc2", "18dec0", "18e0bd", "19e2bb", "19e3b9", "1ae4b6", "1ce6b4", "1de7b2", 
        "1fe9af", "20eaac", "22ebaa", "25eca7", "27eea4", "2aefa1", "2cf09e", "2ff19b", 
        "32f298", "35f394", "38f491", "3cf58e", "3ff68a", "43f787", "46f884", "4af880", 
        "4ef97d", "52fa7a", "55fa76", "59fb73", "5dfc6f", "61fc6c", "65fd69", "69fd66", 
        "6dfe62", "71fe5f", "75fe5c", "79fe59", "7dff56", "80ff53", "84ff51", "88ff4e", 
        "8bff4b", "8fff49", "92ff47", "96fe44", "99fe42", "9cfe40", "9ffd3f", "a1fd3d", "a4fc3c", "a7fc3a", "a9fb39", "acfb38", 
        "affa37", "b1f936", "b4f836", "b7f735", "b9f635", "bcf534", "bef434", "c1f334", 
        "c3f134", "c6f034", "c8ef34", "cbed34", "cdec34", "d0ea34", "d2e935", "d4e735", 
        "d7e535", "d9e436", "dbe236", "dde037", "dfdf37", "e1dd37", "e3db38", "e5d938", 
        "e7d739", "e9d539", "ebd339", "ecd13a", "eecf3a", "efcd3a", "f1cb3a", "f2c93a", 
        "f4c73a", "f5c53a", "f6c33a", "f7c13a", "f8be39", "f9bc39", "faba39", "fbb838", 
        "fbb637", "fcb336", "fcb136", "fdae35", "fdac34", "fea933", "fea732", "fea431", 
        "fea130", "fe9e2f", "fe9b2d", "fe992c", "fe962b", "fe932a", "fe9029", "fd8d27", 
        "fd8a26", "fc8725", "fc8423", "fb8122", "fb7e21", "fa7b1f", "f9781e", "f9751d", 
        "f8721c", "f76f1a", "f66c19", "f56918", "f46617", "f36315", "f26014", "f15d13", 
        "f05b12", "ef5811", "ed5510", "ec530f", "eb500e", "ea4e0d", "e84b0c", "e7490c", 
        "e5470b", "e4450a", "e2430a", "e14109", "df3f08", "dd3d08", "dc3b07", "da3907", 
        "d83706", "d63506", "d43305", "d23105", "d02f05", "ce2d04", "cc2b04", "ca2a04", 
        "c82803", "c52603", "c32503", "c12302", "be2102", "bc2002", "b91e02", "b71d02", 
        "b41b01", "b21a01", "af1801", "ac1701", "a91601", "a71401", "a41301", "a11201", 
        "9e1001", "9b0f01", "980e01", "950d01", "920b01", "8e0a01", "8b0902", "880802", 
        "850702", "810602", "7e0502", "7a0403" ]

        sst_params= {
        'bands': ['SST_B10_Celsius'],
        'min': 13.5,
        'max': 20,
        'palette': TURBO_PALETTE
        }
        dates = ['2021-11-11', '2021-10-26','2021-10-10', '2021-08-07','2021-07-22', '2021-07-06' ]

        processed_collection = ee.ImageCollection([])

        # Loop through the dates and get the imagery
        for date in dates:

            start_date = ee.Date(date)
            end_date = start_date.advance(1, 'day')

            # Filter the image collection by date and area
            image = ee.ImageCollection("LANDSAT/LC08/C02/T1_RT") \
                .filterDate(start_date, end_date) \
                .filterBounds(ee_boundary) \
                .first()  # get the first image that matches the filters

            if image:  # check if image exists
                clipped_image = image.clip(aoi)  # Clip the image to the study boundary
                processed_image = map_instance.image_functions.calculate_sst(clipped_image)  # process the image
                map_instance.addLayer(processed_image, sst_params, date, shown = True)  # add the image to the map
                processed_collection = processed_collection.merge(processed_image)  # add the image to the processed collection
            else:
                print(f"No image found for date {date}")

        # Set the map to focus on the study area

        map_instance.add_colorbar_branca(vis_params= sst_params, colors = TURBO_PALETTE,vmin =  13.5, vmax = 20, label = 'C')


    def load_and_process_salinity(self, map_instance, shapefile_path):
                # Load the study area
            
            study_boundary = gpd.read_file(shapefile_path)
            ee_boundary = geemap.geopandas_to_ee(study_boundary)
            aoi = ee_boundary.geometry()
            VIRIDIS_PALETTE = [
            '440154', '440256', '450457', '450559', '46075a', '46085c', '460a5d', '460b5e', '470d60', 
            '470e61', '471063', '471164', '471365', '481467', '481668', '481769', '48186a', '481a6c', 
            '481b6d', '481c6e', '481d6f', '481f70', '482071', '482173', '482374', '482475', '482576', 
            '482677', '482878', '482979', '472a7a', '472c7a', '472d7b', '472e7c', '472f7d', '46307e', 
            '46327e', '46337f', '463480', '453581', '453781', '453882', '443983', '443a83', '443b84', 
            '433d84', '433e85', '423f85', '424086', '424186', '414287', '414487', '404588', '404688', 
            '3f4788', '3f4889', '3e4989', '3e4a89', '3e4c8a', '3d4d8a', '3d4e8a', '3c4f8a', '3c508b', 
            '3b518b', '3b528b', '3a538b', '3a548c', '39558c', '39568c', '38588c', '38598c', '375a8c', 
            '375b8d', '365c8d', '365d8d', '355e8d', '355f8d', '34608d', '34618d', '33628d', '33638d', 
            '32648e', '32658e', '31668e', '31678e', '30688e', '30698e', '2f6a8e', '2f6b8e', '2e6c8e', 
            '2e6d8e', '2d6e8e', '2d6f8e', '2c708e', '2c718e', '2b728e', '2b738e', '2a748e', '2a758e', 
            '29768e', '29778e', '28788e', '28798e', '277a8e', '277b8e', '267c8e', '267d8e', '257e8e', 
            '257f8e', '24808e', '24818e', '23828e', '23828e', '22838e', '22848e', '21858e', '21868e', 
            '20878e', '20888e', '1f898e', '1f8a8d', '1e8b8d', '1e8c8d', '1d8d8d', '1d8e8d', '1c8f8d', 
            '1c8f8d', '1b908c', '1b918c', '1a928c', '1a938b', '19948b', '19958b', '18968a', '18978a', 
            '17988a', '179989', '169a89', '169b88', '159c88', '159d87', '149e87', '149f86', '13a086', 
            '13a185', '12a285', '12a384', '11a483', '11a583', '10a682', '10a781', '0fa881', '0fa980', 
            '0eaa7f', '0eab7e', '0dac7e', '0dad7d', '0cae7c', '0caf7b', '0bb07a', '0bb179', '0ab278', 
            '0ab377', '09b476', '09b575', '08b674', '08b773', '07b872', '07b971', '06ba70', '06bb6f', 
            '05bc6e', '05bd6d', '04be6c', '04bf6b', '03c06a', '03c169', '02c268', '02c367', '01c466', 
            '01c565', '00c664']
            
            salinity_params= {
            'bands': ['salinity'],
            'min': 0,
            'max': 1000,
            'palette': VIRIDIS_PALETTE
            }
            dates = ['2021-11-11', '2021-10-26','2021-10-10', '2021-08-07','2021-07-22', '2021-07-06' ]

            processed_collection = ee.ImageCollection([])

            # Loop through the dates and get the imagery
            for date in dates:
                
                start_date = ee.Date(date)
                end_date = start_date.advance(1, 'day')

                # Filter the image collection by date and area
                image = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2") \
                    .filterDate(start_date, end_date) \
                    .filterBounds(ee_boundary) \
                    .first()  # get the first image that matches the filters

                if image:  # check if image exists

                    clipped_image = image.clip(aoi)  # Clip the image to the study boundary
                    processed_image = map_instance.image_functions.ansari_akhoondzadeh_salinity(clipped_image)  # process the image
                    map_instance.addLayer(processed_image, salinity_params, date, shown = True)  # add the image to the map
                    processed_collection = processed_collection.merge(processed_image)  # add the image to the processed collection
                else:
                    print(f"No image found for date {date}")

            # Set the map to focus on the study area
            map_instance.add_colorbar_branca(vis_params= salinity_params, colors = VIRIDIS_PALETTE,vmin =  0, vmax = 1000, label = 'EC')
