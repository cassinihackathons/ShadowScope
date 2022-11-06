import wrapper
import pandas as pd
import csv
import os


class Container:
    def __init__(self, latitude, longitude, mean):
        self.latitude = latitude
        self.longitude = longitude
        self.mean = mean


def DownloadInRange(start_latitude, end_latitude, start_longitude, end_longitude, step):
    # 1° = 111 km  (or 60 nautical miles)
    # 0.1° = 11.1 km
    # 0.01° = 1.11 km (2 decimals, km accuracy)
    # 0.001° = 111 m
    # 0.0001° = 11.1 m
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'data')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    Client = wrapper.Downloader()
    for latitude in range(start_latitude*10000, end_latitude*10000, step*10000):
        for longitude in range(start_longitude*10000, end_longitude*10000, step*10000):
            Client.GetData(latitude/10000, longitude/10000)


DownloadInRange(46, 48, 14, 16, 1)

output = open("mean.csv", "w", newline="")
header = ["Latitude", "Longitude", "MeanGHI"]
writer = csv.writer(output)
writer.writerow(header)

array_means = []
for filename in os.listdir("data"):
    with open(os.path.join("data", filename)) as f:
        file_name_split = filename.removesuffix(".csv").split("-")
        df = pd.read_csv(f, skiprows=42, sep=';', skipinitialspace=True)
        ghi_columns = df["GHI"]
        ghi_mean = ghi_columns.mean()
        array_means.append(
            Container(file_name_split[0], file_name_split[1], round(ghi_mean, 2)))

for container in array_means:
    data = [container.latitude, container.longitude, container.mean]
    writer.writerow((data))
