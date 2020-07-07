import logging
import os

try:
    from ipyleaflet import Map, Marker, MarkerCluster, Polyline
    import webbrowser
except ImportError:
    logging.error("Import of ipyleaflet or webbrowser failed.")


class visualize:
    def __init__(self, dataframe):
        """
        This class visualizes the resulting sequence of cities on a open source map.

        :param dataframe: dataframe
        """
        self.dataframe = dataframe
        self.sequence = None
        print("Visualization selected.")

    def visualize_sequence_on_map(self, sequence):
        """
        Visualizes the resulting sequence of cities on a open source map.
        :param sequence: list [int]
        :return:
        """

        self.sequence = sequence

        # Get Marker positions and create map with markers:
        markers = self._create_markers(sequence)
        m = Map(center=markers[0].location, zoom=7, scroll_wheel_zoom=True)
        marker_cluster = MarkerCluster(markers=markers)
        m.add_layer(marker_cluster)

        # Create line between cities:
        line = Polyline(
            locations=[x.location for x in markers],
            color="red",
            fill=False
        )
        m.add_layer(line)

        m.layout.width = '100vw'
        m.layout.height = '100vh'
        # Save file and show in webbrowser:
        fname = "utils/tmp/map.html"
        realpath = os.path.realpath(fname)
        m.save(fname)
        # webbrowser.open_new_tab(fname)
        webbrowser.open_new_tab("file://" + realpath)

        print("...Opening interactive map in browser. If browser does not show the map correctly, try opening the "
              "saved HTML-file ({n}) manually.".format(n=realpath))



    def _create_markers(self, sequence):
        """
        Creates markers in the needed structure/object.
        :param sequence: list [int]

        :return: list [Marker]
        """
        markers = []
        for s in sequence:
            markers.append(Marker(
                location=(self.dataframe["Breitengrad"][s], self.dataframe["Längengrad"][s]),
                title=self.dataframe["msg Standort"][s],
                draggable=False
            ))
        return markers
