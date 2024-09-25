<<<<<<< HEAD
import pandas as pd
import datetime
import os
import json
from bson import decode_all
from dateutil.relativedelta import relativedelta
import numpy as np
import time 
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase
cred = credentials.Certificate("coshow-ffcc0-firebase-adminsdk-9q8er-a3795c1680.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'coshow-ffcc0.appspot.com'
})

# Get a reference to the storage service
bucket = storage.bucket()

os.system('mongodump --uri="mongodb+srv://web_scraping_read_only:SoPydc6a3teOP28q@cluster1.nfor3.mongodb.net/aicarsdb" --collection=deactivatedcars --out=./data')
os.system('mongodump --uri="mongodb+srv://web_scraping_read_only:SoPydc6a3teOP28q@cluster1.nfor3.mongodb.net/aicarsdb" --collection=cars --out=./data')

with open('./data/aicarsdb/cars.bson', 'rb') as file:
    cars_bson = decode_all(file.read())
    
with open('./data/aicarsdb/deactivatedcars.bson', 'rb') as file:
    deactivatedcars_bson = decode_all(file.read())

active = pd.DataFrame(cars_bson)
deactive = pd.DataFrame(deactivatedcars_bson)

active['day_of_week'] = active['createdOn'].dt.day_name()
active['month'] = active['createdOn'].dt.month_name()

deactive['day_of_week'] = deactive['deActivatedAt'].dt.day_name()
deactive['month'] = deactive['deActivatedAt'].dt.month_name()

active['make_model'] = active['make']+ " " + active['model']
deactive['make_model'] = active['make']+ " " + active['model']

current_time = datetime.datetime.now()

one_day_ago = current_time - datetime.timedelta(days=1)
seven_day_ago = current_time - datetime.timedelta(days=7)
fifteen_day_ago = current_time - datetime.timedelta(days=15)
thirty_day_ago = current_time - datetime.timedelta(days=30)
three_month_ago = current_time - relativedelta(months=3)
six_month_ago = current_time - relativedelta(months=6)
life_time = current_time - relativedelta(months=250)

durations = {
    "last one day": one_day_ago,
    "last seven days": seven_day_ago,
    "last fifteen days": fifteen_day_ago,
    "last thirty days": thirty_day_ago,
    "last three months": three_month_ago,
    "last six months": six_month_ago,
    "life time": life_time
    }

platforms = [
    "https://www.facebook.com/",
    "https://heycar.com/",
    "https://www.motors.co.uk/",
    "https://www.gumtree.com/",
    "https://www.autotrader.co.uk/",
    "https://aicarz.com/viewcar/"
    ]

added_new_cars = {}
most_added_make_model = {}
price_info = {}
mileage_info = {}
engine_size_info = {}
year_info = {}
top_5_expensive_make = {}
top_5_cheap_make = {}
top_5_expensive_make_model = {}
top_5_cheap_make_model = {}
top_5_active_cities = {}
top_5_active_fuel_type = {}
top_5_active_body_type = {}
top_5_active_gearbox = {}
active_modified = {}
active_days_stats = {}
active_month_stats = {}

sold_cars = {}
most_sold_make_model = {}
sold_price_info = {}
sold_mileage_info = {}
sold_engine_size_info = {}
sold_year_info = {}
top_5_expensive_sold_make = {}
top_5_cheap_sold_make = {}
top_5_expensive_sold_make_model = {}
top_5_cheap_sold_make_model = {}
top_5_sold_fuel_type = {}
top_5_sold_cities = {}
top_5_sold_body_type = {}
top_5_sold_gearbox = {}
sold_days_stats = {}
sold_month_stats = {}

for duration in durations.values():
    activedata = active[active['createdOn'] >= duration]
    deactivedata = deactive[deactive['deActivatedAt'] >= duration]
    
    temp_dict_added_new_cars = {}
    temp_dict_most_added_make_model = {}
    temp_dict_sold_cars = {}
    temp_dict_most_sold_make_model = {}
    temp_active_day_dict = {}   
    temp_deactive_day_dict = {}   
    temp_active_month_dict = {}   
    temp_deactive_month_dict = {}
    
    for platform in platforms:
        temp_dict_added_new_cars[platform] = activedata[activedata['carBuyLink'].str.startswith(platform)].shape[0]
        
        try:
            temp_dict_most_added_make_model[platform] = activedata[activedata['carBuyLink'].str.startswith(platform)]['make_model'].value_counts().head(5).index.tolist()
        except:
            temp_dict_most_added_make_model[platform] = None
            
    try:
        temp_dict_most_added_make_model["All platforms"] = activedata['make_model'].value_counts().head(5).index.tolist()
    except:
        temp_dict_most_added_make_model["All platforms"] = None
    
    for platform in platforms:
        temp_dict_sold_cars[platform] = deactivedata[deactivedata['carBuyLink'].str.startswith(platform)].shape[0]
        
        try:
            temp_dict_most_sold_make_model[platform] = deactivedata[deactivedata['carBuyLink'].str.startswith(platform)].value_counts().head().index.tolist()
        except:
            temp_dict_most_sold_make_model[platform] = None
    
    temp_dict_most_sold_make_model["All platforms"] = deactivedata['make_model'].value_counts().head().index.tolist()
    
    avg_active_price = activedata['price'].mean()
    min_active_price = activedata['price'].min()
    max_active_price = activedata['price'].max()
    avg_active_price = None if np.isnan(avg_active_price) else avg_active_price
    min_active_price = None if np.isnan(min_active_price) else min_active_price
    max_active_price = None if np.isnan(max_active_price) else max_active_price
    temp_dict_price_info = {"avg active price": avg_active_price,"min active price": min_active_price,"max active price": max_active_price}
    
    avg_active_mileage = activedata['mileageInMiles'].mean()
    min_active_mileage = activedata['mileageInMiles'].min()
    max_active_mileage = activedata['mileageInMiles'].max()
    avg_active_mileage = None if np.isnan(avg_active_mileage) else avg_active_mileage
    min_active_mileage = None if np.isnan(min_active_mileage) else min_active_mileage
    max_active_mileage = None if np.isnan(max_active_mileage) else max_active_mileage
    temp_dict_mileage_info = {"avg active mileage": avg_active_mileage,"min active mileage": min_active_mileage,"max active mileage": max_active_mileage}
    
    avg_active_engine_size = activedata['engineSizeInLiter'].mean()
    min_active_engine_size = activedata['engineSizeInLiter'].min()
    max_active_engine_size = activedata['engineSizeInLiter'].max()
    avg_active_engine_size = None if np.isnan(avg_active_engine_size) else avg_active_engine_size
    min_active_engine_size = None if np.isnan(min_active_engine_size) else min_active_engine_size
    max_active_engine_size = None if np.isnan(max_active_engine_size) else max_active_engine_size
    temp_dict_engine_size_info = {"avg active engineSize": avg_active_engine_size,"min active engineSize": min_active_engine_size,"max active engineSize": max_active_engine_size}
    
    avg_active_year = activedata['year'].mean()
    min_active_year = activedata['year'].min()
    max_active_year = activedata['year'].max()
    avg_active_year = None if np.isnan(avg_active_year) else avg_active_year
    min_active_year = None if np.isnan(min_active_year) else min_active_year
    max_active_year = None if np.isnan(max_active_year) else max_active_year
    temp_dict_year_info = {"avg active year": avg_active_year,"min active year": min_active_year,"max active year": max_active_year}
    
    avg_deactive_price = deactivedata['price'].mean()
    min_deactive_price = deactivedata['price'].min()
    max_deactive_price = deactivedata['price'].max()
    avg_deactive_price = None if np.isnan(avg_deactive_price) else avg_deactive_price
    min_deactive_price = None if np.isnan(min_deactive_price) else min_deactive_price
    max_deactive_price = None if np.isnan(max_deactive_price) else max_deactive_price
    
    temp_dict_sold_price_info = {"avg deactive price": avg_deactive_price,"min deactive price": min_deactive_price,"max deactive price": max_deactive_price}
    
    avg_deactive_mileage = deactivedata['mileageInMiles'].mean()
    min_deactive_mileage = deactivedata['mileageInMiles'].min()
    max_deactive_mileage = deactivedata['mileageInMiles'].max()
    avg_deactive_mileage = None if np.isnan(avg_deactive_mileage) else avg_deactive_mileage
    min_deactive_mileage = None if np.isnan(min_deactive_mileage) else min_deactive_mileage
    max_deactive_mileage = None if np.isnan(max_deactive_mileage) else max_deactive_mileage
    
    temp_dict_sold_mileage_info = {"avg active mileage": avg_deactive_mileage,"min active mileage": min_deactive_mileage,"max active mileage": max_deactive_mileage}
    
    avg_deactive_engine_size = deactivedata['engineSizeInLiter'].mean()
    min_deactive_engine_size = deactivedata['engineSizeInLiter'].min()
    max_deactive_engine_size = deactivedata['engineSizeInLiter'].max()
    avg_deactive_engine_size = None if np.isnan(avg_deactive_engine_size) else avg_deactive_engine_size
    min_deactive_engine_size = None if np.isnan(min_deactive_engine_size) else min_deactive_engine_size
    max_deactive_engine_size = None if np.isnan(max_deactive_engine_size) else max_deactive_engine_size
    
    temp_dict_sold_engine_size_info = {"avg deactive engineSize": avg_deactive_engine_size,"min deactive engineSize": min_deactive_engine_size,"max deactive engineSize": max_deactive_engine_size}
    
    avg_deactive_year = deactivedata['year'].mean()
    min_deactive_year = deactivedata['year'].min()
    max_deactive_year = deactivedata['year'].max()
    avg_deactive_year = None if np.isnan(avg_deactive_year) else avg_deactive_year
    min_deactive_year = None if np.isnan(min_deactive_year) else min_deactive_year
    max_deactive_year = None if np.isnan(max_deactive_year) else max_deactive_year
    temp_dict_sold_year_info = {"avg deactive year": avg_deactive_year,"min deactive year": min_deactive_year,"max deactive year": max_deactive_year}
    
    temp_dict_top_5_expensive_make = activedata.groupby('make')['price'].mean().sort_values(ascending=False)[0:5]
    
    temp_dict_top_5_cheap_make = activedata.groupby('make')['price'].mean().sort_values(ascending=True)[0:5]
    
    temp_dict_top_5_expensive_make_model = activedata.groupby('make_model')['price'].mean().sort_values(ascending=False)[0:5]
    
    temp_dict_top_5_cheap_make_model = activedata.groupby('make_model')['price'].mean().sort_values(ascending=True)[0:5]
    
    temp_dict_top_5_active_cities = activedata['cityName'].value_counts().head(5)
    
    temp_dict_top_5_active_fuel_type = activedata['fuelType'].value_counts().head(5)
    
    temp_dict_top_5_active_body_type = activedata['bodyType'].value_counts().head(5)
    
    temp_dict_top_5_active_gearbox = activedata['gearbox'].value_counts().head(5)
    
    temp_dict_active_modified = activedata['lastModifiedAt'].count()
    
    temp_dict_top_5_expensive_sold_make = deactivedata.groupby('make')['price'].mean().sort_values(ascending=False)[0:5]
    
    temp_dict_top_5_cheap_sold_make = deactivedata.groupby('make')['price'].mean().sort_values(ascending=True)[0:5]
    
    temp_dict_top_5_expensive_sold_make_model = deactivedata.groupby('make_model')['price'].mean().sort_values(ascending=False)[0:5]
    
    temp_dict_top_5_cheap_sold_make_model = deactivedata.groupby('make_model')['price'].mean().sort_values(ascending=True)[0:5]
    
    temp_dict_top_5_sold_fuel_type = deactivedata['fuelType'].value_counts().head(5)
    
    temp_dict_top_5_sold_cities = deactivedata['cityName'].value_counts().head(5)
    
    temp_dict_top_5_sold_body_type = deactivedata['bodyType'].value_counts().head(5)
    
    temp_dict_top_5_sold_gearbox = deactivedata['gearbox'].value_counts().head(5)
    
    duration_key= next((k for k, v in durations.items() if v == duration), None)
    
    for day in active['day_of_week'].unique():
        if not pd.isna(day):
            temp_active_day_dict[day] = activedata[activedata['day_of_week']==day].count().sum() 
            
    for day in deactive['day_of_week'].unique():
        if not pd.isna(day):
            temp_deactive_day_dict[day] = deactivedata[deactivedata['day_of_week']==day].count().sum()   
    
    for month in active['month'].unique():
        if not pd.isna(month):
            temp_active_month_dict[month] = activedata[activedata['month']==month].count().sum()
            
    for month in deactive['month'].unique():
        if not pd.isna(month):
            temp_deactive_month_dict[month] = deactivedata[deactivedata['month']==month].count().sum()
    
    sold_month_stats[duration_key] = temp_deactive_month_dict
    active_month_stats[duration_key] = temp_active_month_dict
    sold_days_stats[duration_key] = temp_deactive_day_dict
    active_days_stats[duration_key] = temp_active_day_dict
    top_5_expensive_make[duration_key] = temp_dict_top_5_expensive_make.to_dict()
    top_5_cheap_make[duration_key] = temp_dict_top_5_cheap_make.to_dict()
    top_5_expensive_make_model[duration_key] = temp_dict_top_5_expensive_make_model.to_dict()
    top_5_cheap_make_model[duration_key] = temp_dict_top_5_cheap_make_model.to_dict()
    top_5_active_cities[duration_key] = temp_dict_top_5_active_cities.to_dict()
    top_5_active_fuel_type[duration_key] = temp_dict_top_5_active_fuel_type.to_dict()
    top_5_active_body_type[duration_key] = temp_dict_top_5_active_body_type.to_dict()
    top_5_active_gearbox[duration_key] = temp_dict_top_5_active_gearbox.to_dict()
    active_modified[duration_key] = temp_dict_active_modified
    year_info[duration_key] = temp_dict_year_info
    mileage_info[duration_key] = temp_dict_mileage_info
    engine_size_info[duration_key] = temp_dict_engine_size_info
    price_info[duration_key] = temp_dict_price_info   
    most_added_make_model[duration_key] = temp_dict_most_added_make_model
    added_new_cars[duration_key] = temp_dict_added_new_cars
    top_5_expensive_sold_make[duration_key] = temp_dict_top_5_expensive_sold_make.to_dict()
    top_5_cheap_sold_make[duration_key] = temp_dict_top_5_cheap_sold_make.to_dict()
    top_5_expensive_sold_make_model[duration_key] = temp_dict_top_5_expensive_sold_make_model.to_dict()
    top_5_cheap_sold_make_model[duration_key] = temp_dict_top_5_cheap_sold_make_model.to_dict()
    top_5_sold_fuel_type[duration_key] = temp_dict_top_5_sold_fuel_type.to_dict()
    top_5_sold_cities[duration_key] = temp_dict_top_5_sold_cities.to_dict()
    top_5_sold_body_type[duration_key] = temp_dict_top_5_sold_body_type.to_dict()
    top_5_sold_gearbox[duration_key] = temp_dict_top_5_sold_gearbox.to_dict()
    sold_year_info[duration_key] = temp_dict_sold_year_info
    sold_engine_size_info[duration_key] = temp_dict_sold_engine_size_info
    sold_mileage_info[duration_key] = temp_dict_sold_mileage_info
    sold_price_info[duration_key] = temp_dict_sold_price_info
    most_sold_make_model[duration_key] = temp_dict_most_sold_make_model
    sold_cars[duration_key] = temp_dict_sold_cars

processed_data= {
        "Active_New car count with platform": added_new_cars,
        "Active_Make models with platform": most_added_make_model, 
        "Active_Price info": price_info,
        "Active_Mileage info": mileage_info,
        "Active_Engine size info": engine_size_info,
        "Active_Years info": year_info,
        "Active_Top 5 expensive makes": top_5_expensive_make,
        "Active_Top 5 cheap makes": top_5_cheap_make,
        "Active_Top 5 expensive make models": top_5_expensive_make_model,
        "Active_Top 5 cheap make models": top_5_cheap_make_model,
        "Active_Top 5 cities": top_5_active_cities,
        "Active_Top 5 fuel types": top_5_active_fuel_type,
        "Active_Top 5 body types": top_5_active_body_type,
        "Active_Top 5 gearbox": top_5_active_gearbox,
        "Active_Modified count": active_modified,
        "Active_Week days new cars count": active_days_stats,
        "Active_Months new cars count": active_month_stats,
        "Sold_car count with platform": sold_cars,
        "Sold_make models with platform": most_sold_make_model, 
        "Sold_price info": sold_price_info,
        "Sold_mileage info": sold_mileage_info,
        "Sold_engine size info": sold_engine_size_info,
        "Sold_years info": sold_year_info,
        "Sold_Top 5 expensive makes": top_5_expensive_sold_make,
        "Sold_Top 5 cheap makes": top_5_cheap_sold_make,
        "Sold_Top 5 expensive make models": top_5_expensive_sold_make_model,
        "Sold_Top 5 cheap make models": top_5_cheap_sold_make_model,
        "Sold_Top 5 cities": top_5_sold_cities,
        "Sold_Top 5 fuel types": top_5_sold_fuel_type,
        "Sold_Top 5 body types": top_5_sold_body_type,
        "Sold_Top 5 gearbox": top_5_sold_gearbox,
        "Sold_Week days cars count": sold_days_stats,
        "Sold_Months cars count": sold_month_stats,
        "Last updated time": round(time.time())
    }


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
    

def upload_file_to_firebase(local_file_path, firebase_file_path):
    bucket = storage.bucket()
    blob = bucket.blob(firebase_file_path)

    blob.upload_from_filename(local_file_path)

    blob.make_public()

    print(f"File uploaded to {blob.public_url}")

# data= processed_data
# flattened_data = {}

# def flatten_json(nested_data, parent_key=''):
#     for key, value in nested_data.items():
#         new_key = f"{parent_key}_{key}" if parent_key else key
#         if isinstance(value, dict):
#             flatten_json(value, new_key)
#         elif isinstance(value, list):
#             for i, item in enumerate(value, 1):
#                 list_key = f"{new_key}_list{i}"
#                 flattened_data[list_key] = item
#         else:
#             flattened_data[new_key] = value

# flatten_json(data)

with open('Processed data.json', 'w') as file:
    json.dump(processed_data, file, indent=4, cls=NpEncoder)

print(json.dumps(processed_data, cls=NpEncoder))
Processed_data_df = pd.DataFrame(processed_data)
Processed_data_df.to_csv("Processed data.csv")

# Loop through each duration and create separate CSV files
# for duration_key, duration_value in durations.items():
#     # Filter data for the current duration
#     activedata = active[active['createdOn'] >= duration_value]
#     deactivedata = deactive[deactive['deActivatedAt'] >= duration_value]
    
#     # Create a dictionary for storing processed data for the current duration
#     processed_data = {
#         "Active_New car count with platform": added_new_cars[duration_key],
#         "Active_Make models with platform": most_added_make_model[duration_key],
#         "Active_Price info": price_info[duration_key],
#         "Active_Mileage info": mileage_info[duration_key],
#         "Active_Engine size info": engine_size_info[duration_key],
#         "Active_Years info": year_info[duration_key],
#         "Active_Top 5 expensive makes": top_5_expensive_make[duration_key],
#         "Active_Top 5 cheap makes": top_5_cheap_make[duration_key],
#         "Active_Top 5 expensive make models": top_5_expensive_make_model[duration_key],
#         "Active_Top 5 cheap make models": top_5_cheap_make_model[duration_key],
#         "Active_Top 5 cities": top_5_active_cities[duration_key],
#         "Active_Top 5 fuel types": top_5_active_fuel_type[duration_key],
#         "Active_Top 5 body types": top_5_active_body_type[duration_key],
#         "Active_Top 5 gearbox": top_5_active_gearbox[duration_key],
#         "Active_Modified count": active_modified[duration_key],
#         "Active_Week days new cars count": active_days_stats[duration_key],
#         "Active_Months new cars count": active_month_stats[duration_key],
#         "Sold_car count with platform": sold_cars[duration_key],
#         "Sold_make models with platform": most_sold_make_model[duration_key],
#         "Sold_price info": sold_price_info[duration_key],
#         "Sold_mileage info": sold_mileage_info[duration_key],
#         "Sold_engine size info": sold_engine_size_info[duration_key],
#         "Sold_years info": sold_year_info[duration_key],
#         "Sold_Top 5 expensive makes": top_5_expensive_sold_make[duration_key],
#         "Sold_Top 5 cheap makes": top_5_cheap_sold_make[duration_key],
#         "Sold_Top 5 expensive make models": top_5_expensive_sold_make_model[duration_key],
#         "Sold_Top 5 cheap make models": top_5_cheap_sold_make_model[duration_key],
#         "Sold_Top 5 cities": top_5_sold_cities[duration_key],
#         "Sold_Top 5 fuel types": top_5_sold_fuel_type[duration_key],
#         "Sold_Top 5 body types": top_5_sold_body_type[duration_key],
#         "Sold_Top 5 gearbox": top_5_sold_gearbox[duration_key],
#         "Sold_Week days cars count": sold_days_stats[duration_key],
#         "Sold_Months cars count": sold_month_stats[duration_key],
#         "Last updated time": round(time.time())
#     }
    
#     # Save to a CSV file
#     filename = f"Processed_data_{duration_key.replace(' ', '_')}.csv"
#     Processed_data_df = pd.DataFrame(processed_data)
#     Processed_data_df.to_csv(filename)
    
    # Upload the CSV file to Firebase
    # upload_file_to_firebase(filename, filename)


=======
import pandas as pd
import datetime
import os
import json
from bson import decode_all
from dateutil.relativedelta import relativedelta
import numpy as np
import time 
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase
cred = credentials.Certificate("coshow-ffcc0-firebase-adminsdk-9q8er-a3795c1680.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'coshow-ffcc0.appspot.com'
})

# Get a reference to the storage service
bucket = storage.bucket()

os.system('mongodump --uri="mongodb+srv://web_scraping_read_only:SoPydc6a3teOP28q@cluster1.nfor3.mongodb.net/aicarsdb" --collection=deactivatedcars --out=./data')
os.system('mongodump --uri="mongodb+srv://web_scraping_read_only:SoPydc6a3teOP28q@cluster1.nfor3.mongodb.net/aicarsdb" --collection=cars --out=./data')

with open('./data/aicarsdb/cars.bson', 'rb') as file:
    cars_bson = decode_all(file.read())
    
with open('./data/aicarsdb/deactivatedcars.bson', 'rb') as file:
    deactivatedcars_bson = decode_all(file.read())

active = pd.DataFrame(cars_bson)
deactive = pd.DataFrame(deactivatedcars_bson)

active['day_of_week'] = active['createdOn'].dt.day_name()
active['month'] = active['createdOn'].dt.month_name()

deactive['day_of_week'] = deactive['deActivatedAt'].dt.day_name()
deactive['month'] = deactive['deActivatedAt'].dt.month_name()

active['make_model'] = active['make']+ " " + active['model']
deactive['make_model'] = active['make']+ " " + active['model']

current_time = datetime.datetime.now()

one_day_ago = current_time - datetime.timedelta(days=1)
seven_day_ago = current_time - datetime.timedelta(days=7)
fifteen_day_ago = current_time - datetime.timedelta(days=15)
thirty_day_ago = current_time - datetime.timedelta(days=30)
three_month_ago = current_time - relativedelta(months=3)
six_month_ago = current_time - relativedelta(months=6)
life_time = current_time - relativedelta(months=250)

durations = {
    "last one day": one_day_ago,
    "last seven days": seven_day_ago,
    "last fifteen days": fifteen_day_ago,
    "last thirty days": thirty_day_ago,
    "last three months": three_month_ago,
    "last six months": six_month_ago,
    "life time": life_time
    }

platforms = [
    "https://www.facebook.com/",
    "https://heycar.com/",
    "https://www.motors.co.uk/",
    "https://www.gumtree.com/",
    "https://www.autotrader.co.uk/",
    "https://aicarz.com/viewcar/"
    ]

added_new_cars = {}
most_added_make_model = {}
price_info = {}
mileage_info = {}
engine_size_info = {}
year_info = {}
top_5_expensive_make = {}
top_5_cheap_make = {}
top_5_expensive_make_model = {}
top_5_cheap_make_model = {}
top_5_active_cities = {}
top_5_active_fuel_type = {}
top_5_active_body_type = {}
top_5_active_gearbox = {}
active_modified = {}
active_days_stats = {}
active_month_stats = {}

sold_cars = {}
most_sold_make_model = {}
sold_price_info = {}
sold_mileage_info = {}
sold_engine_size_info = {}
sold_year_info = {}
top_5_expensive_sold_make = {}
top_5_cheap_sold_make = {}
top_5_expensive_sold_make_model = {}
top_5_cheap_sold_make_model = {}
top_5_sold_fuel_type = {}
top_5_sold_cities = {}
top_5_sold_body_type = {}
top_5_sold_gearbox = {}
sold_days_stats = {}
sold_month_stats = {}

for duration in durations.values():
    activedata = active[active['createdOn'] >= duration]
    deactivedata = deactive[deactive['deActivatedAt'] >= duration]
    
    temp_dict_added_new_cars = {}
    temp_dict_most_added_make_model = {}
    temp_dict_sold_cars = {}
    temp_dict_most_sold_make_model = {}
    temp_active_day_dict = {}   
    temp_deactive_day_dict = {}   
    temp_active_month_dict = {}   
    temp_deactive_month_dict = {}
    
    for platform in platforms:
        temp_dict_added_new_cars[platform] = activedata[activedata['carBuyLink'].str.startswith(platform)].shape[0]
        
        try:
            temp_dict_most_added_make_model[platform] = activedata[activedata['carBuyLink'].str.startswith(platform)]['make_model'].value_counts().head(5).index.tolist()
        except:
            temp_dict_most_added_make_model[platform] = None
            
    try:
        temp_dict_most_added_make_model["All platforms"] = activedata['make_model'].value_counts().head(5).index.tolist()
    except:
        temp_dict_most_added_make_model["All platforms"] = None
    
    for platform in platforms:
        temp_dict_sold_cars[platform] = deactivedata[deactivedata['carBuyLink'].str.startswith(platform)].shape[0]
        
        try:
            temp_dict_most_sold_make_model[platform] = deactivedata[deactivedata['carBuyLink'].str.startswith(platform)].value_counts().head().index.tolist()
        except:
            temp_dict_most_sold_make_model[platform] = None
    
    temp_dict_most_sold_make_model["All platforms"] = deactivedata['make_model'].value_counts().head().index.tolist()
    
    avg_active_price = activedata['price'].mean()
    min_active_price = activedata['price'].min()
    max_active_price = activedata['price'].max()
    avg_active_price = None if np.isnan(avg_active_price) else avg_active_price
    min_active_price = None if np.isnan(min_active_price) else min_active_price
    max_active_price = None if np.isnan(max_active_price) else max_active_price
    temp_dict_price_info = {"avg active price": avg_active_price,"min active price": min_active_price,"max active price": max_active_price}
    
    avg_active_mileage = activedata['mileageInMiles'].mean()
    min_active_mileage = activedata['mileageInMiles'].min()
    max_active_mileage = activedata['mileageInMiles'].max()
    avg_active_mileage = None if np.isnan(avg_active_mileage) else avg_active_mileage
    min_active_mileage = None if np.isnan(min_active_mileage) else min_active_mileage
    max_active_mileage = None if np.isnan(max_active_mileage) else max_active_mileage
    temp_dict_mileage_info = {"avg active mileage": avg_active_mileage,"min active mileage": min_active_mileage,"max active mileage": max_active_mileage}
    
    avg_active_engine_size = activedata['engineSizeInLiter'].mean()
    min_active_engine_size = activedata['engineSizeInLiter'].min()
    max_active_engine_size = activedata['engineSizeInLiter'].max()
    avg_active_engine_size = None if np.isnan(avg_active_engine_size) else avg_active_engine_size
    min_active_engine_size = None if np.isnan(min_active_engine_size) else min_active_engine_size
    max_active_engine_size = None if np.isnan(max_active_engine_size) else max_active_engine_size
    temp_dict_engine_size_info = {"avg active engineSize": avg_active_engine_size,"min active engineSize": min_active_engine_size,"max active engineSize": max_active_engine_size}
    
    avg_active_year = activedata['year'].mean()
    min_active_year = activedata['year'].min()
    max_active_year = activedata['year'].max()
    avg_active_year = None if np.isnan(avg_active_year) else avg_active_year
    min_active_year = None if np.isnan(min_active_year) else min_active_year
    max_active_year = None if np.isnan(max_active_year) else max_active_year
    temp_dict_year_info = {"avg active year": avg_active_year,"min active year": min_active_year,"max active year": max_active_year}
    
    avg_deactive_price = deactivedata['price'].mean()
    min_deactive_price = deactivedata['price'].min()
    max_deactive_price = deactivedata['price'].max()
    avg_deactive_price = None if np.isnan(avg_deactive_price) else avg_deactive_price
    min_deactive_price = None if np.isnan(min_deactive_price) else min_deactive_price
    max_deactive_price = None if np.isnan(max_deactive_price) else max_deactive_price
    
    temp_dict_sold_price_info = {"avg deactive price": avg_deactive_price,"min deactive price": min_deactive_price,"max deactive price": max_deactive_price}
    
    avg_deactive_mileage = deactivedata['mileageInMiles'].mean()
    min_deactive_mileage = deactivedata['mileageInMiles'].min()
    max_deactive_mileage = deactivedata['mileageInMiles'].max()
    avg_deactive_mileage = None if np.isnan(avg_deactive_mileage) else avg_deactive_mileage
    min_deactive_mileage = None if np.isnan(min_deactive_mileage) else min_deactive_mileage
    max_deactive_mileage = None if np.isnan(max_deactive_mileage) else max_deactive_mileage
    
    temp_dict_sold_mileage_info = {"avg active mileage": avg_deactive_mileage,"min active mileage": min_deactive_mileage,"max active mileage": max_deactive_mileage}
    
    avg_deactive_engine_size = deactivedata['engineSizeInLiter'].mean()
    min_deactive_engine_size = deactivedata['engineSizeInLiter'].min()
    max_deactive_engine_size = deactivedata['engineSizeInLiter'].max()
    avg_deactive_engine_size = None if np.isnan(avg_deactive_engine_size) else avg_deactive_engine_size
    min_deactive_engine_size = None if np.isnan(min_deactive_engine_size) else min_deactive_engine_size
    max_deactive_engine_size = None if np.isnan(max_deactive_engine_size) else max_deactive_engine_size
    
    temp_dict_sold_engine_size_info = {"avg deactive engineSize": avg_deactive_engine_size,"min deactive engineSize": min_deactive_engine_size,"max deactive engineSize": max_deactive_engine_size}
    
    avg_deactive_year = deactivedata['year'].mean()
    min_deactive_year = deactivedata['year'].min()
    max_deactive_year = deactivedata['year'].max()
    avg_deactive_year = None if np.isnan(avg_deactive_year) else avg_deactive_year
    min_deactive_year = None if np.isnan(min_deactive_year) else min_deactive_year
    max_deactive_year = None if np.isnan(max_deactive_year) else max_deactive_year
    temp_dict_sold_year_info = {"avg deactive year": avg_deactive_year,"min deactive year": min_deactive_year,"max deactive year": max_deactive_year}
    
    temp_dict_top_5_expensive_make = activedata.groupby('make')['price'].mean().sort_values(ascending=False)[0:5]
    
    temp_dict_top_5_cheap_make = activedata.groupby('make')['price'].mean().sort_values(ascending=True)[0:5]
    
    temp_dict_top_5_expensive_make_model = activedata.groupby('make_model')['price'].mean().sort_values(ascending=False)[0:5]
    
    temp_dict_top_5_cheap_make_model = activedata.groupby('make_model')['price'].mean().sort_values(ascending=True)[0:5]
    
    temp_dict_top_5_active_cities = activedata['cityName'].value_counts().head(5)
    
    temp_dict_top_5_active_fuel_type = activedata['fuelType'].value_counts().head(5)
    
    temp_dict_top_5_active_body_type = activedata['bodyType'].value_counts().head(5)
    
    temp_dict_top_5_active_gearbox = activedata['gearbox'].value_counts().head(5)
    
    temp_dict_active_modified = activedata['lastModifiedAt'].count()
    
    temp_dict_top_5_expensive_sold_make = deactivedata.groupby('make')['price'].mean().sort_values(ascending=False)[0:5]
    
    temp_dict_top_5_cheap_sold_make = deactivedata.groupby('make')['price'].mean().sort_values(ascending=True)[0:5]
    
    temp_dict_top_5_expensive_sold_make_model = deactivedata.groupby('make_model')['price'].mean().sort_values(ascending=False)[0:5]
    
    temp_dict_top_5_cheap_sold_make_model = deactivedata.groupby('make_model')['price'].mean().sort_values(ascending=True)[0:5]
    
    temp_dict_top_5_sold_fuel_type = deactivedata['fuelType'].value_counts().head(5)
    
    temp_dict_top_5_sold_cities = deactivedata['cityName'].value_counts().head(5)
    
    temp_dict_top_5_sold_body_type = deactivedata['bodyType'].value_counts().head(5)
    
    temp_dict_top_5_sold_gearbox = deactivedata['gearbox'].value_counts().head(5)
    
    duration_key= next((k for k, v in durations.items() if v == duration), None)
    
    for day in active['day_of_week'].unique():
        if not pd.isna(day):
            temp_active_day_dict[day] = activedata[activedata['day_of_week']==day].count().sum() 
            
    for day in deactive['day_of_week'].unique():
        if not pd.isna(day):
            temp_deactive_day_dict[day] = deactivedata[deactivedata['day_of_week']==day].count().sum()   
    
    for month in active['month'].unique():
        if not pd.isna(month):
            temp_active_month_dict[month] = activedata[activedata['month']==month].count().sum()
            
    for month in deactive['month'].unique():
        if not pd.isna(month):
            temp_deactive_month_dict[month] = deactivedata[deactivedata['month']==month].count().sum()
    
    sold_month_stats[duration_key] = temp_deactive_month_dict
    active_month_stats[duration_key] = temp_active_month_dict
    sold_days_stats[duration_key] = temp_deactive_day_dict
    active_days_stats[duration_key] = temp_active_day_dict
    top_5_expensive_make[duration_key] = temp_dict_top_5_expensive_make.to_dict()
    top_5_cheap_make[duration_key] = temp_dict_top_5_cheap_make.to_dict()
    top_5_expensive_make_model[duration_key] = temp_dict_top_5_expensive_make_model.to_dict()
    top_5_cheap_make_model[duration_key] = temp_dict_top_5_cheap_make_model.to_dict()
    top_5_active_cities[duration_key] = temp_dict_top_5_active_cities.to_dict()
    top_5_active_fuel_type[duration_key] = temp_dict_top_5_active_fuel_type.to_dict()
    top_5_active_body_type[duration_key] = temp_dict_top_5_active_body_type.to_dict()
    top_5_active_gearbox[duration_key] = temp_dict_top_5_active_gearbox.to_dict()
    active_modified[duration_key] = temp_dict_active_modified
    year_info[duration_key] = temp_dict_year_info
    mileage_info[duration_key] = temp_dict_mileage_info
    engine_size_info[duration_key] = temp_dict_engine_size_info
    price_info[duration_key] = temp_dict_price_info   
    most_added_make_model[duration_key] = temp_dict_most_added_make_model
    added_new_cars[duration_key] = temp_dict_added_new_cars
    top_5_expensive_sold_make[duration_key] = temp_dict_top_5_expensive_sold_make.to_dict()
    top_5_cheap_sold_make[duration_key] = temp_dict_top_5_cheap_sold_make.to_dict()
    top_5_expensive_sold_make_model[duration_key] = temp_dict_top_5_expensive_sold_make_model.to_dict()
    top_5_cheap_sold_make_model[duration_key] = temp_dict_top_5_cheap_sold_make_model.to_dict()
    top_5_sold_fuel_type[duration_key] = temp_dict_top_5_sold_fuel_type.to_dict()
    top_5_sold_cities[duration_key] = temp_dict_top_5_sold_cities.to_dict()
    top_5_sold_body_type[duration_key] = temp_dict_top_5_sold_body_type.to_dict()
    top_5_sold_gearbox[duration_key] = temp_dict_top_5_sold_gearbox.to_dict()
    sold_year_info[duration_key] = temp_dict_sold_year_info
    sold_engine_size_info[duration_key] = temp_dict_sold_engine_size_info
    sold_mileage_info[duration_key] = temp_dict_sold_mileage_info
    sold_price_info[duration_key] = temp_dict_sold_price_info
    most_sold_make_model[duration_key] = temp_dict_most_sold_make_model
    sold_cars[duration_key] = temp_dict_sold_cars

processed_data= {
        "Active_New car count with platform": added_new_cars,
        "Active_Make models with platform": most_added_make_model, 
        "Active_Price info": price_info,
        "Active_Mileage info": mileage_info,
        "Active_Engine size info": engine_size_info,
        "Active_Years info": year_info,
        "Active_Top 5 expensive makes": top_5_expensive_make,
        "Active_Top 5 cheap makes": top_5_cheap_make,
        "Active_Top 5 expensive make models": top_5_expensive_make_model,
        "Active_Top 5 cheap make models": top_5_cheap_make_model,
        "Active_Top 5 cities": top_5_active_cities,
        "Active_Top 5 fuel types": top_5_active_fuel_type,
        "Active_Top 5 body types": top_5_active_body_type,
        "Active_Top 5 gearbox": top_5_active_gearbox,
        "Active_Modified count": active_modified,
        "Active_Week days new cars count": active_days_stats,
        "Active_Months new cars count": active_month_stats,
        "Sold_car count with platform": sold_cars,
        "Sold_make models with platform": most_sold_make_model, 
        "Sold_price info": sold_price_info,
        "Sold_mileage info": sold_mileage_info,
        "Sold_engine size info": sold_engine_size_info,
        "Sold_years info": sold_year_info,
        "Sold_Top 5 expensive makes": top_5_expensive_sold_make,
        "Sold_Top 5 cheap makes": top_5_cheap_sold_make,
        "Sold_Top 5 expensive make models": top_5_expensive_sold_make_model,
        "Sold_Top 5 cheap make models": top_5_cheap_sold_make_model,
        "Sold_Top 5 cities": top_5_sold_cities,
        "Sold_Top 5 fuel types": top_5_sold_fuel_type,
        "Sold_Top 5 body types": top_5_sold_body_type,
        "Sold_Top 5 gearbox": top_5_sold_gearbox,
        "Sold_Week days cars count": sold_days_stats,
        "Sold_Months cars count": sold_month_stats,
        "Last updated time": round(time.time())
    }


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
    

def upload_file_to_firebase(local_file_path, firebase_file_path):
    bucket = storage.bucket()
    blob = bucket.blob(firebase_file_path)

    blob.upload_from_filename(local_file_path)

    blob.make_public()

    print(f"File uploaded to {blob.public_url}")

# data= processed_data
# flattened_data = {}

# def flatten_json(nested_data, parent_key=''):
#     for key, value in nested_data.items():
#         new_key = f"{parent_key}_{key}" if parent_key else key
#         if isinstance(value, dict):
#             flatten_json(value, new_key)
#         elif isinstance(value, list):
#             for i, item in enumerate(value, 1):
#                 list_key = f"{new_key}_list{i}"
#                 flattened_data[list_key] = item
#         else:
#             flattened_data[new_key] = value

# flatten_json(data)

with open('Processed data.json', 'w') as file:
    json.dump(processed_data, file, indent=4, cls=NpEncoder)

print(json.dumps(processed_data, cls=NpEncoder))
Processed_data_df = pd.DataFrame(processed_data)
Processed_data_df.to_csv("Processed data.csv")

# Loop through each duration and create separate CSV files
# for duration_key, duration_value in durations.items():
#     # Filter data for the current duration
#     activedata = active[active['createdOn'] >= duration_value]
#     deactivedata = deactive[deactive['deActivatedAt'] >= duration_value]
    
#     # Create a dictionary for storing processed data for the current duration
#     processed_data = {
#         "Active_New car count with platform": added_new_cars[duration_key],
#         "Active_Make models with platform": most_added_make_model[duration_key],
#         "Active_Price info": price_info[duration_key],
#         "Active_Mileage info": mileage_info[duration_key],
#         "Active_Engine size info": engine_size_info[duration_key],
#         "Active_Years info": year_info[duration_key],
#         "Active_Top 5 expensive makes": top_5_expensive_make[duration_key],
#         "Active_Top 5 cheap makes": top_5_cheap_make[duration_key],
#         "Active_Top 5 expensive make models": top_5_expensive_make_model[duration_key],
#         "Active_Top 5 cheap make models": top_5_cheap_make_model[duration_key],
#         "Active_Top 5 cities": top_5_active_cities[duration_key],
#         "Active_Top 5 fuel types": top_5_active_fuel_type[duration_key],
#         "Active_Top 5 body types": top_5_active_body_type[duration_key],
#         "Active_Top 5 gearbox": top_5_active_gearbox[duration_key],
#         "Active_Modified count": active_modified[duration_key],
#         "Active_Week days new cars count": active_days_stats[duration_key],
#         "Active_Months new cars count": active_month_stats[duration_key],
#         "Sold_car count with platform": sold_cars[duration_key],
#         "Sold_make models with platform": most_sold_make_model[duration_key],
#         "Sold_price info": sold_price_info[duration_key],
#         "Sold_mileage info": sold_mileage_info[duration_key],
#         "Sold_engine size info": sold_engine_size_info[duration_key],
#         "Sold_years info": sold_year_info[duration_key],
#         "Sold_Top 5 expensive makes": top_5_expensive_sold_make[duration_key],
#         "Sold_Top 5 cheap makes": top_5_cheap_sold_make[duration_key],
#         "Sold_Top 5 expensive make models": top_5_expensive_sold_make_model[duration_key],
#         "Sold_Top 5 cheap make models": top_5_cheap_sold_make_model[duration_key],
#         "Sold_Top 5 cities": top_5_sold_cities[duration_key],
#         "Sold_Top 5 fuel types": top_5_sold_fuel_type[duration_key],
#         "Sold_Top 5 body types": top_5_sold_body_type[duration_key],
#         "Sold_Top 5 gearbox": top_5_sold_gearbox[duration_key],
#         "Sold_Week days cars count": sold_days_stats[duration_key],
#         "Sold_Months cars count": sold_month_stats[duration_key],
#         "Last updated time": round(time.time())
#     }
    
#     # Save to a CSV file
#     filename = f"Processed_data_{duration_key.replace(' ', '_')}.csv"
#     Processed_data_df = pd.DataFrame(processed_data)
#     Processed_data_df.to_csv(filename)
    
    # Upload the CSV file to Firebase
    # upload_file_to_firebase(filename, filename)


>>>>>>> 222f1dee3f04cf95e7eb12c66294b2f7efee6525
upload_file_to_firebase('Processed data.json', 'Processed data.json')