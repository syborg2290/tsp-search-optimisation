import pandas as pd
import numpy as np

cities = pd.read_csv("data/cities.csv")

# Inspect the dataset
print(cities.head())

# Dataset information
print(cities.info())

# Dataset dimensions
print(cities.shape)

# Missing values
print(cities.isnull().sum())

# Duplicate records
print(cities.duplicated().sum())