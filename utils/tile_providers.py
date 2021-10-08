# Helper for provider object for contextily, built-in is very limited/does not work as intended

import contextily as ctx

class TileProviders():
    def stadia(self, map_type, key):
        return 'https://tiles.stadiamaps.com/tiles/' + map_type + '/{z}/{x}/{y}.png?api_key=' + key


        #ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik, interpolation='sinc')
#ctx.add_basemap(ax, source=ctx.providers.Thunderforest.Neighbourhood(apikey="4811d9ca2dcc4ac5a597a70cb6e263cb"), interpolation='sinc')
ctx.add_basemap(ax, source='https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}.png?api_key=6791cad9-2687-433b-a86e-72ef2166907d', interpolation='sinc')
