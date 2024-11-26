import lightningchart as lc
import pandas as pd
import numpy as np

# Set up LightningChart license
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'dataset/Batteries.xlsx'
sheet_data = pd.read_excel(file_path, sheet_name="Unpivoted")

# Filter data to exclude total household and group by activities
filtered_data = sheet_data[~sheet_data["NACE Rev. 2 Activity"].str.strip().str.contains("TOTAL_HH", case=False, na=False)]
grouped_data = filtered_data.groupby('NACE Rev. 2 Activity')['VALUE'].sum()

# Normalize data to show intensity
normalized_values = grouped_data / grouped_data.sum()

# Prepare data for Polar Area Chart
activity_labels = [activity.split("(")[-1].strip(")") for activity in grouped_data.index]
intensity_values = normalized_values.tolist()

# Create the Polar Chart
chart = lc.PolarChart(
    title="Intensity of Waste Production by Economic Activities",
    theme=lc.Themes.TurquoiseHexagon,
)

# Add data as a single area series
data_points = [
    {"angle": angle, "amplitude": value}
    for angle, value in zip(np.linspace(0, 360, len(activity_labels), endpoint=False), intensity_values)
]
area_series = chart.add_area_series().set_name("Waste Intensity").set_data(data_points)

# Customize amplitude axis (radial axis)
amplitude_axis = chart.get_amplitude_axis()
amplitude_axis.set_title("Intensity")
amplitude_axis.set_interval(0, max(intensity_values) * 1.2)

# Customize radial axis (angular axis) labels
radial_axis = chart.get_radial_axis()
radial_axis.set_division(len(activity_labels))
radial_axis.set_tick_labels(activity_labels)

# Open the chart
chart.open()
