import logging
import os
import numpy as np

try:
    from ipyleaflet import Map, Marker, MarkerCluster, Polyline
    import webbrowser
except ImportError:
    logging.error("Import of ipyleaflet or webbrowser failed.")

try:
    import plotly.graph_objects as go
except ImportError:
    logging.error("Import of plotly failed.")


class visualize_graph:
    def __init__(self, tspsolver, dataframe):
        self.dataframe = dataframe
        self.best_sequence, self.best_dist = tspsolver.get_result()
        self.all_dists, self.all_sequences = tspsolver.get_best_sequences()

        self.fig = None

        print("Graph Visualization selected.")

    def visualize_sequences_in_graph(self):
        locationmode = 'USA-states'

        # Colors:
        color_cities = 'rgb(255,255,255)'
        color_germany = 'rgb(156,39,66)'
        color_countries = 100
        color_lines = 'rgb(30,30,30)'


        # Build figure from all sequences from the best iteration step:
        frames, lon_vals, lat_vals = self._setup_frames(color_countries, color_lines)
        self._setup_figure(frames, lon_vals, lat_vals, color_germany)
        self._setup_cities(locationmode, color_cities)
        self._setup_layout(color_countries)

        # Show interactive graph:
        self.fig.show()

        # Save interactive graph as html:
        fname = "utils/tmp/graph.html"
        realpath = os.path.realpath(fname)
        self.fig.write_html(realpath)

        print("...Opening interactive graph in browser. If browser does not show the map correctly, try opening the "
              "saved HTML-file ({n}) manually.".format(n=realpath))


    def _setup_frames(self, color_countries, color_lines):
        # Create frames for visualization: ----------------------------------------
        frames = list()
        self.all_sequences.append(self.best_sequence)
        self.all_dists.append(self.best_dist)

        for i in range(len(self.all_sequences)):
            seq = self.all_sequences[i]
            # Calculate color for current frame:
            color = int(color_countries + i / len(self.all_sequences) * (255.0 - color_countries))

            # Store all coordinates of the cities for the current frame in correct order:
            lon_vals = []
            lat_vals = []
            for s in seq:
                lon_vals.append(self.dataframe["Längengrad"][s])
                lat_vals.append(self.dataframe["Breitengrad"][s])

            # Append current frame with all lines connection the cities:
            frames.append(
                go.Frame(
                    data=[go.Scattergeo(
                        lon=lon_vals,
                        lat=lat_vals,
                        line=dict(width=2,
                                  color=color_lines),
                        opacity=0.8
                    )],
                    layout=go.Layout(
                        geo=dict(
                            landcolor='rgb({p},{p},{p})'.format(p=color)
                        )
                    )
                )
            )

        return frames, lon_vals, lat_vals

    def _setup_figure(self, frames, lon_vals, lat_vals, color_germany):
        # Set up plotly Figure: -----------------------------------------------------
        self.fig = go.Figure(
            data=[
                go.Scattergeo(
                    locationmode='USA-states', mode="lines",
                    lon=np.append(lon_vals[0], lon_vals[0]),
                    lat=np.append(lat_vals[0], lat_vals[0]),
                    # line=dict(width=1, color='rgb(250,0,0)'), opacity=0.1,
                    hoverinfo='none', name="teamname"
                )
            ],
            layout=go.Layout(
                title="Start Title",
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(
                        label="Play",
                        method="animate",
                        args=[None, {"frame": {"duration": 20}}]
                    )])]
            ),
            frames=frames
        )


        # Coloring Germany red: ----------------------------------------------------------
        self.fig.add_trace(go.Choropleth(
            locations=["Germany"],  # Spatial coordinates
            z=[0.0],  # Data to be color-coded
            locationmode='country names',  # set of locations match entries in `locations`
            colorscale=[[0.0, color_germany], [0.5, color_germany], [1.0, color_germany]],  # old: "rgb(188,44,0)"
            showscale=False,
            autocolorscale=False
        ))

        return self.fig

    def _setup_cities(self, locationmode, color_cities):
        # Adding Cities:------------------------------------
        self.fig.add_trace(go.Scattergeo(
            locationmode=locationmode,
            lon=self.dataframe["Längengrad"].tolist(),
            lat=self.dataframe["Breitengrad"].tolist(),
            text=self.dataframe["msg Standort"],
            name="msg locations",
            textposition="top center",
            textfont={
                "family": "Balto, sans-serif",
                "size": 14,
                "color": "Black"
            },
            mode='markers+text',
            marker=dict(
                size=10,
                color=color_cities,

                line=dict(
                    width=1,
                    color='White'
                )
            ))
        )

    def _setup_layout(self, color_countries):
        # Updating Figure Layout: ---------------------------------------------------------
        self.fig.update_layout(
            title_text='[PRESS PLAY] .msg Coding Challenge: \n'
                       'Iterating through the Search Algorithm Output for finding the shortest '
                       'route around all msg locations in Germany.\n',
            showlegend=False,
            hovermode=False,
            geo=dict(
                lataxis=dict(range=[min(self.dataframe["Breitengrad"].tolist()) * 0.97,
                                    max(self.dataframe["Breitengrad"].tolist()) * 1.03]),
                lonaxis=dict(range=[min(self.dataframe["Längengrad"].tolist()) * 0.85,
                                    max(self.dataframe["Längengrad"].tolist()) * 1.03]),
                scope='europe',
                showland=True,
                landcolor='rgb({p},{p},{p})'.format(p=color_countries),
                countrycolor='White',
                countrywidth=1

            ),
        )


class visualize_map:
    def __init__(self, dataframe):
        """
        This class visualizes the resulting sequence of cities on a open source map.

        :param dataframe: dataframe
        """
        self.dataframe = dataframe
        self.sequence = None
        print("Streetmap Visualization selected.")

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

        print("...Opening interactive streetmap in browser. If browser does not show the map correctly, try opening "
              "the saved HTML-file ({n}) manually.".format(n=realpath))



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
