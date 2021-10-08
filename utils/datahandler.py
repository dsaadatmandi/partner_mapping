# Class to handle data sources

import csv

class DataHandler():
    def __init__(self):
        self.country = self.csv2dict()
    
    def csv2dict(self):
        with open('./sources.csv', mode='r') as file:
            reader = csv.reader(file)
            return {rows[0]: rows[1] for rows in reader}