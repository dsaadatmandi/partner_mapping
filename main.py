from logging import raiseExceptions
from urllib.request import DataHandler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
import datetime
from matplotlib import colors
import googlemaps
import matplotlib.path as mpath
from pyproj import Transformer
plt.style.use('seaborn')
import asyncio
import utils.keyledger as kl
import utils.pin as pin_mod
import time

class PlotMagic:
    def __init__(self):
        self.germany_df = gpd.read_file('./data/input.gpkg', dtype={'plz': str})
        self.transformer = Transformer.from_crs('epsg:4326', 'epsg:3857')
        self.pin = pin_mod.LocationPin().pin
        self.keys = kl.KeyLedger()
        self.gmaps = googlemaps.Client(key=self.keys.googlemaps_key)
        self.hno = True
        print("If you want to update the data used here, see 'generate_gpkg.py'.")
        #self.execute()
    
    def initialise(self):
        self.postal_code_list = self.get_input()
        self.colormapping = {'Sehr hohes Potenzial' : 'green', 'Hohes Potenzial': 'orange', 'Mittleres Potenzial': 'deepskyblue'}
        self.ketten = ['Fielmann', 'GEERS', 'KIND', 'Amplifon', 'Apollo']
        self.ketten_laden = []
        self.fach_laden = []
    
    def get_input(self):
        return input("Enter Postal Codes that you want to plot, separated by commas. >>> ").replace(" ", "").split(",")

    def parse_input(self):
        self.plot_df = self.germany_df.query('plz == @self.postal_code_list').to_crs(epsg=3857)

    def generate_plot(self):
        self.fig, self.ax = plt.subplots()
        self.ax = self.plot_df.plot(ax=self.ax, legend=False, color=self.plot_df['potenzial'].map(self.colormapping), alpha=0.3, linewidth=0.5, edgecolor="black")
        plt.axis('off')

    def add_basemap(self):
        #could build selector here
        #ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik, interpolation='sinc')
        #ctx.add_basemap(ax, source=ctx.providers.Thunderforest.Neighbourhood(apikey=self.keys.thunderforest_key), interpolation='sinc')
        source_stadia = 'https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}.png?api_key=' + self.keys.stadia_key
        ctx.add_basemap(self.ax, source=source_stadia, interpolation='sinc')

    def plot_places(self, places, pin, color, akustiker_mode, alpha, marker_size):
        for n in places:
            if [i for i in self.postal_code_list if i in n.get('formatted_address')]:
                if akustiker_mode:
                    if [j for j in self.ketten if j in n.get('name')]:
                        x, y = self.transformer.transform(n.get('geometry').get('location').get('lat'), n.get('geometry').get('location').get('lng'))
                        plt.plot(x, y, color, marker=self.pin, markersize=marker_size)
                        self.ketten_laden.append(n.get('name'))
                    else:
                        x, y = self.transformer.transform(n.get('geometry').get('location').get('lat'), n.get('geometry').get('location').get('lng'))
                        plt.plot(x, y, 'bo', marker=self.pin, markersize=marker_size)
                        self.fach_laden.append(n.get('name'))
                else:
                    x, y = self.transformer.transform(n.get('geometry').get('location').get('lat'), n.get('geometry').get('location').get('lng'))
                    plt.plot(x, y, color, marker=self.pin, markersize=marker_size, alpha=alpha)
                    self.location_list.append(n.get('name'))

    def get_results(self, query_type: str, token):
        return self.gmaps.places(query="{} in der Nähe von {}".format(query_type, self.postal_code_list[0]), region='de', page_token=token)

    def plot_logic(self, query_type: str, pin, color: str, akustiker_mode=False, alpha=1, marker_size=25):
        self.location_list = []
        token = None
        while True:
            results = self.get_results(query_type, token)
            places = results.get('results')
            self.plot_places(places, pin, color, akustiker_mode, alpha, marker_size)
            token = results.get('next_page_token')
            if token == None:
                break
            else:
                print(f"Getting more results for {query_type}. Please wait...")
                time.sleep(2)
                pass

    def execute_plotting(self):
        if self.hno:
            self.plot_logic('HNO', self.pin, 'gray', alpha=0.8, marker_size=15)
            self.hno_list = self.location_list
        self.plot_logic('Hörgeräte', self.pin, 'ro', akustiker_mode=True)

    def set_correct_limits(self):
        self.x_lim_input, self.y_lim_input = self.ax.get_xlim(), self.ax.get_ylim()
        self.x_size = self.x_lim_input[1] - self.x_lim_input[0]
        self.y_size = self.y_lim_input[1] - self.y_lim_input[0]
        self.ratio = self.x_size/self.y_size
        self.correct_ratio = 14.28/10.86
        if self.ratio == self.correct_ratio:
            pass
        elif self.ratio < self.correct_ratio:
            self.x_new = self.y_size*self.correct_ratio
            self.ax.set(xlim=(self.x_lim_input[0]-0.5*(self.x_new-self.x_size), self.x_lim_input[1]+0.5*(self.x_new-self.x_size)))
        elif self.ratio > self.correct_ratio:
            self.y_new = self.x_size/self.correct_ratio
            self.ax.set(ylim=(self.y_lim_input[0]-0.5*(self.y_new-self.y_size), self.y_lim_input[1]+0.5*(self.y_new-self.y_size)))

    def remove_whitespace(self):
        plt.gca().set_axis_off()
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0,0)

    def output_data(self):
        plt.show()
        print('Es gibt {} Fachgeschäfte und {} Ketten in diesem Gebiet'.format(len(self.fach_laden), len(self.ketten_laden)))
        print('Fachgeschäfte:\n', self.fach_laden, '\nKetten:\n', self.ketten_laden)

    def execute(self):
        self.initialise()
        self.parse_input()
        self.generate_plot()
        self.set_correct_limits()
        self.add_basemap()
        self.execute_plotting()
        self.remove_whitespace()
        plt.savefig('./graphs/{}.png'.format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")), bbox_inches='tight', dpi=300, pad_inches=0)
        self.output_data()

######FIGURE OUT BEST WAY TO SAVE IN CONTAINER ->> STATELESS

#plt.savefig('./graphs/{}.png'.format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")), bbox_inches='tight', dpi=300)

#plt.show()

while True:
    print("Creating Object")
    plotter = PlotMagic()
    print("Executing code   ")
    plotter.execute()
    break  
