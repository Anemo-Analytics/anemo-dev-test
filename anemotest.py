import pandas as pd
import numpy as np

""" 1. Write a function that takes a string and returns the string in reverse order. For example, "hello" should become "olleh"."""


def reverse_string(string):
    pass


""" 2. Write a function that takes a string and returns the number of vowels in the string. 
You may assume that all the letters are lower cased. For example, "hello" should return 2."""


def vowels(s):
    pass


""" 3. Write a function that takes a list of numbers and returns the second largest number. For example, [1, 2, 3, 4] should return 3."""


def second_largest(l):
    pass


""" 4. Write a function that takes a list of numbers and returns True if the list contains an even number of even numbers. 
For example, [1, 2, 3, 4] should return True."""


def even_list(l):
    pass


""" 5. Write a function that takes a string and returns a list with the unique vowels and unique consonants of the string.
for example, "engineering" should return [e,i,n,g,r] IN ANY ORDER """


def vowels_consonants(s):
    pass


""" 6. using the load_devices() funtion from below, load the file ../conf_debug/meta_parks.json. 
This file is composed of a list of 5 documents, one per park. Each document has a parkid and a list of devices 
(each device is a dictionary). Each device has a device_type and an ip.

Write a function that prints the IPs of all the devices that 
are of "device_type"=="inverter module". Use only devices from parkids TEST_SPI or SPI. 
Use the load_devices() function to load the data from the file, so write your function after load_devices().
"""


def load_devices():
    import json
    with open('../conf_debug/meta_parks.json') as f:
        data = json.load(f)
    return data


""" 7. Create a class that represents a device (class Device) and a class that represents a solar park (SolarPark) 
whose fields are based on the meta_parks.json file.
- Create a blank class that is a Park and make SolarPark inherit from it. The Park class can be empty.
- The constructor of the Park class should take the park dictionary as an argument
- The constructor of the Device class should take the device dictionary as an argument
- Define a method in the park class that returns the devices of a given "device_type" 
- Define a method in the park class that returns the IP of a given device_id 
- Create a function that loads the devices with load_devices() and creates a list of park objects. This function return a park object based
 on an input argument "parkid". """


def load_sample_dataframe():
    index = pd.date_range(pd.Timestamp.now(), periods=10000, freq='s').round('s')
    columns = ['power', 'pitch', 'windspeed']
    df = pd.DataFrame(data=np.random.rand(len(index), len(columns)), columns=columns, index=index)
    df['windspeed'] *= 10
    df['power'] *= 1000
    df['pitch'] *= 5
    return df.copy()


def load_sample_dataframe2():
    df = load_sample_dataframe()
    df['status'] = np.random.choice([0, 1], size=len(df), p=[0.8, 0.2])
    return df.copy()


""" 9. Load the sample dataframe using load_sample_dataframe(). Calculate the hourly average power
of the three columns in the dataframe."""


def hourly_averages(df: pd.DataFrame) -> pd.DataFrame:
    return df.resample('h').mean()


""" 10. Load the sample dataframe using load_sample_dataframe(). Calculate
the hourly average values of one column, (`power` for instance) for different 
values of another column (`winspeeed`). Split the windspeed data in bins of size 1: (1,2,3,4,5...)"""


def hourly_grouped_averages(data: pd.DataFrame, average_column: str, grouping_colum: str,
        bin_size: int) -> pd.DataFrame:
    assert (average_column in data.columns) and (grouping_colum in data.columns)
    df = data.copy()
    bins = np.arange(int(df[grouping_colum].min()), round(df[grouping_colum].max() + bin_size), bin_size)
    df['groups'] = pd.cut(df[grouping_colum], bins=bins)
    return df.groupby('groups')['power'].mean()


""" 11. Load the second sample dataframe using load_sample_dataframe2(). This dataframe contains an extra column
called 'status' that can be either 0 or 1. Make a function that returns the average seconds passing between switches from 
status=1 to status=0. """


def average_seconds_between_off_switch(df: pd.DataFrame) -> float:
    df = df.copy()
    switches = df['status'].diff()
    return switches[switches == -1].index.to_series().diff().dt.total_seconds().mean()


class Device:
    def __init__(self, device_dict):
        self.device_type = device_dict['device_type']
        self.device_id = device_dict['device_id']
        self.ip = device_dict['ip']


class Park:
    pass


class SolarPark(Park):
    def __init__(self, park_dict):
        self.parkid = park_dict['parkid']
        self.devices = [Device(device) for device in park_dict['devices']]

    def get_devices(self, device_type):
        return [device for device in self.devices if device.device_type == device_type]

    def get_ip(self, device_id):
        return [device.ip for device in self.devices if device.device_id == device_id]


def get_park(parkid):
    data = load_devices()
    return SolarPark([park for park in data if park['parkid'] == parkid][0])


print(reverse_string("engineering"))
print(vowels("hello, how are you doing"))
print(second_largest([2, 2, 43, 43, 4, 5]))
print(even_list([1, 2, 3, 4]))
print(vowels_consonants("engineering"))
print(hourly_averages(load_sample_dataframe()))
print(hourly_grouped_averages(load_sample_dataframe(), 'power', 'windspeed', 1))
print(average_seconds_between_off_switch(load_sample_dataframe2()))
