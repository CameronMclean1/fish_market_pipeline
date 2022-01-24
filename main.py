import boto3
from pprint import pprint as pp
import pandas as pd
import csv
import os

s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")
bucket_name = "data-eng-resources"

bucket_name = "data-eng-resources"
bucket_contents = s3_client.list_objects_v2(Bucket = bucket_name, Prefix = 'python/fish-market')

class fish:
    def __init__(self, entry):
        self.species = entry['\ufeffSpecies']
        self.stats = {}
        print(type(self.stats))
        for key in list(entry.keys()):
            if key!='\ufeffSpecies':
                self.stats[key] = [float(entry[key])]

    def update(self, entry):
        '''Add new entry to fish's stats'''
        for key in list(entry.keys()):
            if key!='\ufeffSpecies':
                self.stats[key].append(float(entry[key]))

    def average(self):
        '''Returns the average stats for the fish'''
        mean_fish = {}
        mean_fish['Species'] = self.species
        for key in list(self.stats.keys()):
            if key!='\ufeffSpecies':
                mean_fish[key] = sum(self.stats[key]) / len(self.stats[key])
        return(mean_fish)

fishmarket = []
fish_list = []

def check_if_exists(species):
    '''Check if specific type of fish has already been seen
            If has been seen, return relevant object
            If has not been seen, return False'''
    for f in fish_list:
        if f.species==species:
            return f
    return False

for object in bucket_contents["Contents"]: #For each relevant file
    print(object['Key'])
    s3_object = s3_client.get_object(Bucket=bucket_name, Key=object['Key'])
    lines = s3_object['Body'].read().decode('utf-8').split()
    for row in csv.DictReader(lines): #For each entry in file
        active_fish = row['\ufeffSpecies']
        check = check_if_exists(active_fish) 
        if check==False:
            fish_list.append(fish(row))
        else:
            check.update(row)


for f in fish_list:
    '''Create list of each fishes average stats
            fishmarket will be a list of dictionaries
            could be done during writing of csv, but would be messy'''
    fishmarket.append(f.average())

fields = list(fishmarket[0].keys())
data = []
for entry in fishmarket:
    new_data = []
    for field in fields:
        new_data.append(entry[field])
    data.append(new_data)


with open('fishmarket.csv', 'w') as fish_csv: #Fails if file is 
    write = csv.writer(fish_csv)
      
    write.writerow(fields)
    write.writerows(data)

s3_client.upload_file(Filename="fishmarket.csv", Bucket=bucket_name, Key="Data26/fish/CameronM-fish.csv") #Upload to s3 cloud
            
