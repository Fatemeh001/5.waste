

import lightningchart as lc
import pandas as pd
import numpy as np


with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the simplified dataset
file_path = 'dataset/Book1.xlsx'
sheet1_data = pd.read_excel(file_path, sheet_name='Sheet1')


# Filter the data for top NACE Rev. 2 Activities.
top_activities = [
   
    "Services (except wholesale of waste and scrap)  (G-U_X_G4677)",
    "Households (EP_HH)",
    'Mining and quarrying (B)',
    'Manufacturing (C)',
    'Waste collection, treatment and disposal activities; materials recovery (E38)'
]
filtered_data = sheet1_data[sheet1_data["NACE Rev. 2 Activity"].isin(top_activities)]

# Ensure only even years are considered.
filtered_data = filtered_data[filtered_data["Year"].astype(int) % 2 == 0]

# Check if only even years remain.
even_years = filtered_data["Year"].unique()
print(f"Remaining Years: {even_years}")

# Aggregate data by Year and Activity.
grouped_data = filtered_data.groupby(["Year", "NACE Rev. 2 Activity"])["VALUE"].sum().unstack()

# Ensure the data is sorted by year.
grouped_data = grouped_data.sort_index()

# Prepare data for stacked area chart.
x_values = grouped_data.index.astype(int).tolist()
series_data = grouped_data.fillna(0).values.T

# Initialize LightningChart.
chart = lc.ChartXY(
    theme=lc.Themes.Light,
    title="Stacked Area Chart - Top NACE Rev. 2 Activities (Even Years)"
)


for activity, data in zip(grouped_data.columns, series_data):
    area_series = chart.add_area_series()
    area_series.set_name(activity)
    area_series.add(x_values, data.tolist()) 
# Customize axes.
chart.get_default_x_axis().set_title("Year")
chart.get_default_y_axis().set_title("Waste Generated (Tonnes)")

# Add legend.
chart.add_legend(data=chart).set_position(x=40, y=60)

# Open the chart.
chart.open()


# selected_activities = [
#     'Mining and quarrying (B)',
#     'Services (except wholesale of waste and scrap)  (G-U_X_G4677)',
#     'Manufacturing (C)',
#     'Waste collection, treatment and disposal activities; materials recovery (E38)'
# ]
# filtered_data = sheet1_data[sheet1_data["NACE Rev. 2 Activity"].isin(selected_activities)]

# # Ensure only even years are considered.
# filtered_data = filtered_data[filtered_data["Year"].astype(int) % 2 == 0]

# # Aggregate data by Year and Activity.
# grouped_data = filtered_data.groupby(["Year", "NACE Rev. 2 Activity"])["VALUE"].sum().unstack()

# # Ensure the data is sorted by year.
# grouped_data = grouped_data.sort_index()

# # Prepare data for stacked area chart.
# x_values = grouped_data.index.astype(int).tolist()
# series_data = grouped_data.fillna(0).values.T

# # Initialize LightningChart.
# chart = lc.ChartXY(
#     theme=lc.Themes.Light,
#     title="Stacked Area Chart - Selected NACE Rev. 2 Activities (Even Years)"
# )

# # Add area series for each activity.
# cumulative_data = np.zeros(len(x_values))
# for activity, data in zip(grouped_data.columns, series_data):
#     cumulative_data += data
#     area_series = chart.add_area_series()
#     area_series.set_name(activity)
#     area_series.add(x_values, cumulative_data)

# # Customize axes.
# chart.get_default_x_axis().set_title("Year")
# chart.get_default_y_axis().set_title("Waste Generated (Tonnes)")

# # Add legend.
# chart.add_legend(data=chart)

# # Open the chart.
# chart.open()