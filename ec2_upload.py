import pymongo

def upload(fish_list):
    client = pymongo.MongoClient()
    db = client['FishMarket']
    db.fish_info.drop()
    db.create_collection('fish_info')
    for fish in fish_list:
        print(fish)
        db.fish_info.insert_one(fish)
