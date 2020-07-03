import pandas as pd
import logging
from math import cos, sin, asin, radians, sqrt


class loadcsv:
    """
    This class loads and interprets the csv-file with the format, which is stated in the task.
    Further, this class calculates the distances between the locations from the geocoordinates.
    """
    def __init__(self, path):
        """
        Setup the csv-interpreter.
        :param path: str
            Path to the csv-file
        """
        self.path = path
        self.loadeddata = pd.read_csv(self.path)
        logging.debug("\n" + str(self.loadeddata))
        self.distance_frame = None

    def _load_data(self):
        """
        Loads the csv-file into a pandas dataframe.
        :return:
        """
        self.loadeddata = pd.read_csv(self.path)
        logging.debug("\n" + str(self.loadeddata))

    def _calculate_distances(self):
        """
        Iterates through the dataframe entries (locations) and calculates the distance to each other location.
        Result is the distance matrix saved as self.distance_frame.
        :return:
        """
        dist_list_glob = []
        for i1, loc1 in self.loadeddata.iterrows():
            dist_list_loc = []
            for i2, loc2 in self.loadeddata.iterrows():
                dist_list_loc.append(self._get_distance(loc1, loc2))
            dist_list_glob.append(dist_list_loc)

        self.distance_frame = pd.DataFrame(dist_list_glob)

    def _get_distance(self, loc1, loc2):
        """
        This function calculates the distance between the two given locations in km. Here, the distance is calculated
        as the circle distance via the geo coordinates of the locations.
        :param loc1: dict
            first location entry from dataframe
        :param loc2: dict
            second location entry from dataframe
        :return:
        dist: float
            Distance between the two given locations in km
        """
        lon1, lat1, lon2, lat2 = map(radians, [loc1["Längengrad"], loc1["Breitengrad"], loc2["Längengrad"], loc2["Breitengrad"]])

        diff_lon = lon2 - lon1
        diff_lat = lat2 - lat1

        dist = 6371 * 2 * asin(sqrt(sin(diff_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(diff_lon / 2) ** 2))
        return dist

    def get_data(self):
        """
        This function executes the other internal functions and returns the internal dataframe objects which
        contain the location-infos and distances.
        :return:
        loadeddata: dataframe,
            Dataframe containing the general info for each location
        distance_frame: dataframe,
            Dataframe containing the distance matrix for all locations
        """
        self._load_data()
        self._calculate_distances()
        return self.loadeddata, self.distance_frame
