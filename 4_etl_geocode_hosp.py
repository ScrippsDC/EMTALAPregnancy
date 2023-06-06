import pandas, geocoder, config

df = pandas.read_csv('data/processed/3_etl_facility_summary.csv')
df["to_geocode"] = df["address"] + ", " + df["city"] + ", " + df["state"]

def get_lat_lng(row):
    g = geocoder.google(row["to_geocode"],key=config.google_key)
    return g.latlng

df["lat_lng"] = df.apply(get_lat_lng, axis=1)
df["lat"] = df["lat_lng"].apply(lambda x: x[0])
df["lng"] = df["lat_lng"].apply(lambda x: x[1])
df.to_csv("data/processed/4_etl_geocoded_facility_summary.csv")