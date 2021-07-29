import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

from urllib.request import FancyURLopener
#import fiona
#from fiona import schema, _shim
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
import datetime
from matplotlib import colors
import googlemaps
import matplotlib.path as mpath
from svgpath2mpl import parse_path
import matplotlib as mpl
from pyproj import Transformer
plt.style.use('seaborn')
import time
#import rasterio
#import rasterio._shim
#import rasterio.control
#import rasterio.rpc
#import rasterio.crs
#import rasterio.sample
import PySimpleGUI as sg
import pyperclip



def set_correct_limits(x_size, y_size):
    ratio = x_size/y_size
    correct_ratio = 14.28/10.86
    if ratio == correct_ratio:
        pass
    elif ratio < correct_ratio:
        x_new = y_size*correct_ratio
        ax.set(xlim=(x_lim_input[0]-0.5*(x_new-x_size), x_lim_input[1]+0.5*(x_new-x_size)))
    elif ratio > correct_ratio:
        y_new = x_size/correct_ratio
        ax.set(ylim=(y_lim_input[0]-0.5*(y_new-y_size), y_lim_input[1]+0.5*(y_new-y_size)))

def get_results(query_type: str, token):
    return gmaps.places(query="{} in der Nähe von {}".format(query_type, plz_list[0]), region='de', page_token=token)

def plot_places(query_type: str, pin, color: str, akustiker_mode=False, alpha=1, marker_size=25):
    location_list = []
    token = None
    while True:
        results = get_results(query_type, token)
        places = results.get('results')
        generate_plot(places, pin, color, akustiker_mode, alpha, marker_size)
        token = results.get('next_page_token')
        if token == None:
            break
        else:
            print(f"Getting more results for {query_type}. Please wait...")
            time.sleep(2)
            pass

def generate_plot(places, pin, color, akustiker_mode, alpha, marker_size):
    for n in places:
        if [i for i in plz_list if i in n.get('formatted_address')]:
            if akustiker_mode:
                if [j for j in ketten if j in n.get('name')]:
                    x, y = transformer.transform(n.get('geometry').get('location').get('lat'), n.get('geometry').get('location').get('lng'))
                    plt.plot(x, y, color, marker=pin, markersize=marker_size)
                    ketten_laden.append(n.get('name'))
                else:
                    x, y = transformer.transform(n.get('geometry').get('location').get('lat'), n.get('geometry').get('location').get('lng'))
                    plt.plot(x, y, 'bo', marker=pin, markersize=marker_size)
                    fach_laden.append(n.get('name'))
            else:
                x, y = transformer.transform(n.get('geometry').get('location').get('lat'), n.get('geometry').get('location').get('lng'))
                plt.plot(x, y, color, marker=pin, markersize=marker_size, alpha=alpha)
                location_list.append(n.get('name'))

def load_data():
    return gpd.read_file('./data/input_v1.gpkg', dtype={'plz': str})


pizza = False
HNO = True

ketten = ['Fielmann', 'GEERS', 'KIND', 'Amplifon', 'Apollo']
ketten_laden, fach_laden, location_list = [], [], []
colormapping = {'Sehr hohes Potenzial' : 'green', 'Hohes Potenzial': 'orange', 'Mittleres Potenzial': 'deepskyblue'}
location_pin = parse_path("M12 0c-4.198 0-8 3.403-8 7.602 0 4.198 3.469 9.21 8 16.398 4.531-7.188 8-12.2 8-16.398 0-4.199-3.801-7.602-8-7.602zm0 11c-1.657 0-3-1.343-3-3s1.343-3 3-3 3 1.343 3 3-1.343 3-3 3z")
location_pin.vertices -= location_pin.vertices.mean(axis=0)
location_pin = location_pin.transformed(mpl.transforms.Affine2D().rotate_deg(180))
pizza_pin = parse_path("M 195.287,16.574 C 168.741,5.576 140.776,0 112.169,0 83.676,0 55.769,5.574 29.224,16.566 c -1.838,0.762 -3.298,2.223 -4.06,4.061 -0.761,1.838 -0.761,3.904 10e-4,5.742 l 11.992,28.932 c 0.001,0.004 0.005,0.008 0.007,0.012 l 68.16,164.574 c 1.168,2.818 3.917,4.625 6.926,4.625 0.218,0 0.437,-0.01 0.656,-0.029 2.85,-0.248 5.271,-2.088 6.311,-4.682 L 187.36,55.311 c 0.002,-0.004 0.004,-0.006 0.006,-0.01 l 11.98,-28.928 c 1.584,-3.828 -0.233,-8.215 -4.059,-9.799 z M 112.169,15 c 24.133,0 47.778,4.264 70.397,12.688 l -6.246,15.08 C 155.702,35.17 134.163,31.323 112.182,31.323 90.286,31.323 68.8,35.171 48.2,42.766 L 41.946,27.68 C 64.554,19.262 88.141,15 112.169,15 Z M 112.254,197.416 53.949,56.643 c 18.766,-6.846 38.317,-10.32 58.232,-10.32 20,0 39.605,3.477 58.389,10.324 z M 147.709,93.728996 A 14.146,14.146 0 0 1 133.563,107.875 14.146,14.146 0 0 1 119.417,93.728996 a 14.146,14.146 0 0 1 14.146,-14.146 14.146,14.146 0 0 1 14.146,14.146 z M 112.256,126.77 c -7.811,0 -14.145,6.334 -14.145,14.147 0,7.816 6.334,14.15 14.145,14.15 7.814,0 14.148,-6.334 14.148,-14.15 0,-7.813 -6.334,-14.147 -14.148,-14.147 z m -9.11,-52.343997 A 14.146,14.146 0 0 1 89,88.572002 14.146,14.146 0 0 1 74.854,74.426003 14.146,14.146 0 0 1 89,60.280003 a 14.146,14.146 0 0 1 14.146,14.146 z")
pizza_pin.vertices -= pizza_pin.vertices.mean(axis=0)
pizza_pin = pizza_pin.transformed(mpl.transforms.Affine2D().rotate_deg(180))
transformer = Transformer.from_crs('epsg:4326', 'epsg:3857')

layout = [
[sg.Text("Standortanalyse 2.0")], 
[sg.Text("Enter PLZs to plot, separated by commas (Primary PLZ first)")],
[sg.InputText()],
[sg.Button("Plot"), sg.Button("Close")]
]

window = sg.Window("Standortanalyse 2.0", layout)

while True:
    event, values = window.read()
    if 'germany_df' not in locals():
        germany_df = load_data()
    if event == sg.WIN_CLOSED or event == "Close":
        quit()
    elif event == "Plot":
        try:
            plz_list = values[0].replace(" ", "").split(",")
            for i in plz_list:
                n = int(i)
            break
        except:
            print("Invalid input, try again.")
            pass

window.close()

#plz_list = input("Enter PLZs to plot, separated by commas (Remember, primary PLZ first) >>> ").replace(" ","").split(",")
plot_df = germany_df[germany_df["plz"].isin(plz_list)].to_crs(epsg=3857)

fig, ax = plt.subplots()
ax = plot_df.plot(
ax=ax, legend=False, color=plot_df['potenzial'].map(colormapping), alpha=0.4, linewidth=0.5, edgecolor="black", categorical=True)

x_lim_input, y_lim_input = ax.get_xlim(), ax.get_ylim()
x_size = x_lim_input[1] - x_lim_input[0]
y_size = y_lim_input[1] - y_lim_input[0]

set_correct_limits(x_size, y_size)

#ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik, interpolation='sinc', attribution=False)
ctx.add_basemap(ax, source=ctx.providers.Thunderforest.Neighbourhood(apikey="4811d9ca2dcc4ac5a597a70cb6e263cb"), interpolation='sinc', attribution=False)
#ctx.add_basemap(ax, source='https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}.png?api_key=6791cad9-2687-433b-a86e-72ef2166907d', interpolation='sinc', attribution=False)

gmaps = googlemaps.Client(key='AIzaSyAfgPjz49pr0MmPfhB62AZZeCr3NNcN38c')

if HNO:
    plot_places('HNO', location_pin, 'gray', akustiker_mode=False, alpha=0.8, marker_size=15)
    HNO_list = location_list
if pizza:
    plot_places('Pizza', pizza_pin, 'cyan', akustiker_mode=False)
    pizza_list = location_list
plot_places('Hörgeräte', location_pin, 'ro', akustiker_mode=True)


plt.gca().set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
plt.margins(0,0)
#plt.gca().xaxis.set_major_locator(plt.NullLocator())
#plt.gca().yaxis.set_major_locator(plt.NullLocator())

plt.savefig('./graphs/{}.png'.format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")), bbox_inches='tight', dpi=300, pad_inches=0)

print('Es gibt {} Fachgeschäfte und {} Ketten in diesem Gebiet'.format(len(fach_laden), len(ketten_laden)))
print('Fachgeschäfte:\n', fach_laden, '\nKetten:\n', ketten_laden)

plt.show()

num_akustiker = len(fach_laden + ketten_laden)
termine = plot_df['kunden22'].sum()
anpasspauschale = termine * 850

output = f"{num_akustiker}\x09{len(fach_laden)}\x09\x09{len(HNO_list)}\x09{termine}\x09{anpasspauschale}"
pyperclip.copy(output)