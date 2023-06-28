# Place all your constants here
import os

# Note: constants should be UPPER_CASE
constants_path = os.path.realpath(__file__)
SRC_PATH = os.path.dirname(constants_path)
PROJECT_PATH = os.path.dirname(SRC_PATH)


# The larger study area to use for earth engine this study uses the coastline of the Santa Monica bay

STUDY_BOUNDARY_PATH = os.path.join(SRC_PATH,'study_boundary.gpkg')
