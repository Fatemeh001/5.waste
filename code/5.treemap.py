# import pandas as pd
# import lightningchart as lc

# # Load and set the LightningChart license
# with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# # Load the dataset
# file_path = 'dataset/Batteries.xlsx'
# sheet_name = 'Unpivoted'
# data = pd.read_excel(file_path, sheet_name=sheet_name)

# # Apply all filters 
# filtered_data = data[
#     (data['VALUE'] != 0) &
#     (data['VALUE'].notnull()) &
#     (data['Waste Category'] == 'Health care and biological wastes[W05]') &
#     (data['Hazardousness'] != 'Hazardous and non-hazardous - Total[HAZ_NHAZ]') 
#     # (data['NACE Rev. 2 Activity'] != 'All NACE activities plus households (TOTAL_HH)')
# ]

# # Aggregate data by Year and NACE Rev. 2 Activity, summing up Hazardousness categories
# aggregated_data = filtered_data.groupby(
#     ["Year", "NACE Rev. 2 Activity"], as_index=False
# ).agg({"VALUE": "sum"})

# # Prepare TreeMap data grouped only by Year
# treemap_data_aggregated = []
# for year, year_group in aggregated_data.groupby("Year"):
#     year_node = {
#         "name": str(year),
#         "children": [
#             {"name": activity, "value": value}
#             for activity, value in zip(year_group["NACE Rev. 2 Activity"], year_group["VALUE"])
#         ]
#     }
#     treemap_data_aggregated.append(year_node)

# # Create the TreeMap chart
# chart = lc.TreeMapChart(
#     theme=lc.Themes.Dark,
# )
# chart.set_title=("Health Care and Biological Wastes by Year (Aggregated Hazardousness)")
# # Set TreeMap data
# chart.set_data(treemap_data_aggregated)

# # Customize node coloring based on aggregated VALUE
# min_value = aggregated_data["VALUE"].min()
# max_value = aggregated_data["VALUE"].max()

# color_aggregated = chart.set_node_coloring(
#     steps=[
#         {"value": min_value, "color": lc.Color("blue")},
#         {"value": (min_value + max_value) / 4, "color": lc.Color("green")},
#         {"value": (min_value + max_value) / 2, "color": lc.Color("yellow")},
#         {"value": (3 * (min_value + max_value)) / 4, "color": lc.Color("orange")},
#         {"value": max_value, "color": lc.Color("red")}
#     ]
# )

# # Add legend to explain colors
# legend = chart.add_legend()
# legend.set_position(30, 20)
# legend.set_margin(10)
# legend.add(color_aggregated)

# # Open the chart
# chart.open()


import pandas as pd
import lightningchart as lc

# Load and set the LightningChart license
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'dataset/Batteries.xlsx'
sheet_name = 'Unpivoted'
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Apply all filters
filtered_data = data[
    (data['VALUE'] != 0) &
    (data['VALUE'].notnull()) &
    (data['Waste Category'] == 'Health care and biological wastes[W05]') &
    (data['Hazardousness'] != 'Hazardous and non-hazardous - Total[HAZ_NHAZ]') &
    (data['NACE Rev. 2 Activity'] != 'All NACE activities plus households (TOTAL_HH)')
]

# Aggregate data by NACE Rev. 2 Activity
aggregated_data_no_year = filtered_data.groupby(
    "NACE Rev. 2 Activity", as_index=False
).agg({"VALUE": "sum"})

# Calculate percentage share for each activity
aggregated_data_no_year['Percentage'] = (aggregated_data_no_year['VALUE'] / aggregated_data_no_year['VALUE'].sum()) * 100

# Prepare TreeMap data
treemap_data_no_year = [
    {"name": f"{activity} ({percent:.1f}%)", "value": value}
    for activity, value, percent in zip(
        aggregated_data_no_year["NACE Rev. 2 Activity"],
        aggregated_data_no_year["VALUE"],
        aggregated_data_no_year["Percentage"]
    )
]

# Create the TreeMap chart
chart = lc.TreeMapChart(
    theme=lc.Themes.Dark,
    title="Health Care and Biological Wastes by Activity"
)

# Set TreeMap data
chart.set_data(treemap_data_no_year)

# Customize node coloring based on percentage share
# Customize node coloring based on aggregated VALUE
min_value = filtered_data["VALUE"].min()
max_value = filtered_data["VALUE"].max()

color_aggregated = chart.set_node_coloring(
    steps=[
        {"value": min_value, "color": lc.Color("blue")},
        {"value": (min_value + max_value) / 4, "color": lc.Color("green")},
        {"value": (min_value + max_value) / 2, "color": lc.Color("yellow")},
        {"value": (3 * (min_value + max_value)) / 4, "color": lc.Color("orange")},
        {"value": max_value, "color": lc.Color("red")}
    ]
)

# Add legend for color scale
legend_no_year = chart.add_legend()
legend_no_year.set_position(20, 20)
legend_no_year.set_margin(10)
legend_no_year.add(color_aggregated)

# Open the chart
chart.open()


