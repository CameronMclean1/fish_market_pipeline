import boto3
import csv
from fish import fish
from ec2_upload import upload

s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")
bucket_name = "data-eng-resources"

bucket_name = "data-eng-resources"
bucket_contents = s3_client.list_objects_v2(Bucket = bucket_name, Prefix = 'python/fish-market')

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
        #print(row) #gathering for test
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

upload(fishmarket)

fields = list(fishmarket[0].keys())
data = []
for entry in fishmarket:
    new_data = []
    for field in fields:
        new_data.append(entry[field])
    data.append(new_data)


with open('fishmarket.csv', 'w') as fish_csv: #Fails if file is open
    write = csv.writer(fish_csv)
      
    write.writerow(fields)
    write.writerows(data)

s3_client.upload_file(Filename="fishmarket.csv", Bucket=bucket_name, Key="Data26/fish/CameronM-fish.csv") #Upload to s3 cloud
            
