
import lightningchart as lc
import pandas as pd
import numpy as np
from matplotlib import cm


with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)




file_path = 'dataset/Batteries.xlsx'
sheet_data = pd.read_excel(file_path, sheet_name="Unpivoted")
# Filter the dataset for the column "Waste Category" and select "Batteries and accumulators wastes[W0841]"
filtered_data = sheet_data[sheet_data["Waste Category"] == "Batteries and accumulators wastes[W0841]"]
filtered_data = sheet_data[~sheet_data["NACE Rev. 2 Activity"].str.strip().str.contains("TOTAL_HH", case=False, na=False)]


# Prepare the data for the Polar Heatmap
# Pivoting the data to create a matrix for 'VALUE' based on 'NACE Rev. 2 Activity' and 'Hazardousness'
heatmap_data = filtered_data.pivot_table(
    index='Hazardousness',
    columns='NACE Rev. 2 Activity',
    values='VALUE',
    aggfunc='sum',
    fill_value=0
)

# Convert data to a list of lists for the heatmap
heatmap_data_matrix = heatmap_data.values.tolist()



# Create a Polar Chart
chart = lc.PolarChart(theme=lc.Themes.TurquoiseHexagon, title="Polar Heatmap from Dataset")

# Add a Heatmap series with dimensions matching the data
heatmap_series = chart.add_heatmap_series(sectors=len(heatmap_data.columns), annuli=len(heatmap_data.index))

# Use the processed data for the heatmap
heatmap_series.invalidate_intensity_values(values=heatmap_data_matrix)

# Set the color palette
color= heatmap_series.set_palette_coloring(
    steps=[
        {'value': min(map(min, heatmap_data_matrix)), 'color': lc.Color('blue')},
        {'value': max(map(max, heatmap_data_matrix)) / 2, 'color': lc.Color('green')},
        {'value': max(map(max, heatmap_data_matrix)), 'color': lc.Color('red')},
    ],
    look_up_property='value',
    interpolate=True
)
chart.add_legend().add(color)
# Configure interpolation for smooth transitions
heatmap_series.set_intensity_interpolation('bilinear')

# Open the chart
chart.open()


# # پولار خطی
# # -----------------------------------------------------------------------------------------------------
import pandas as pd
import lightningchart as lc
import random
import numpy as np

file_path = 'dataset/Batteries.xlsx'
sheet_data = pd.read_excel(file_path, sheet_name="Unpivoted")
filtered_data = sheet_data[sheet_data["Waste Category"] == "Batteries and accumulators wastes[W0841]"]
filtered_data = sheet_data[~sheet_data["NACE Rev. 2 Activity"].str.strip().str.contains("TOTAL_HH", case=False, na=False)]

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

filtered_data = filtered_data[filtered_data['Hazardousness'].isin(['Hazardous[HAZ]', 'Non-hazardous[NHAZ]'])]
grouped_data = filtered_data.groupby(['Year', 'Hazardousness'])['VALUE'].sum().unstack()

chart = lc.PolarChart(theme=lc.Themes.TurquoiseHexagon, title="Hazardous and Non-Hazardous Waste Over Years").open(live=True)

# Define fixed colors for clarity
colors = {'Hazardous[HAZ]': lc.Color('red'), 'Non-hazardous[NHAZ]': lc.Color('blue')}
line_series = {}

for waste_type in ['Hazardous[HAZ]', 'Non-hazardous[NHAZ]']:
    series = chart.add_point_line_series().set_name(waste_type)
    series.set_stroke(thickness=2, color=colors[waste_type])
    line_series[waste_type] = series

legend = lc.ui.legend.Legend(chart, horizontal=False, title="Waste Types")
for waste_type, series in line_series.items():
    legend.add(series)
legend.set_font_size(14).set_padding(10)

years = grouped_data.index.values
min_year, max_year = int(min(years)), int(max(years))

def year_to_angle(year):
    return np.interp(year, (min_year, max_year), (0, 360))

for waste_type in ['Hazardous[HAZ]', 'Non-hazardous[NHAZ]']:
    points = []
    for year in years:
        if year in grouped_data.index:
            value = grouped_data.loc[year, waste_type] if waste_type in grouped_data.columns else 0
            angle = year_to_angle(int(year))
            points.append({'angle': angle, 'amplitude': float(value)})
    line_series[waste_type].set_data(points)

radial_axis = chart.get_radial_axis()
radial_axis.set_title("Total Waste")
radial_axis.set_interval(0, grouped_data.max().max())  # Automatically adjust based on max value

angular_axis = chart.get_radial_axis()
angular_axis.set_division(len(years) // 5)  # Show labels every 5 years
angular_axis.set_tick_labels([str(int(year)) for year in years])

chart.open()


# # -----------------------------------------------------------------------------------------------------


import pandas as pd
import lightningchart as lc
import numpy as np

file_path = 'dataset/Batteries.xlsx'
sheet_data = pd.read_excel(file_path, sheet_name="Unpivoted")
# Filter the dataset for the column "Waste Category" and select "Batteries and accumulators wastes[W0841]"
filtered_data = sheet_data[sheet_data["Waste Category"] == "Batteries and accumulators wastes[W0841]"]
filtered_data = sheet_data[~sheet_data["NACE Rev. 2 Activity"].str.strip().str.contains("TOTAL_HH", case=False, na=False)]
# License key
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Filter the data for hazardous and non-hazardous wastes
filtered_data = filtered_data[filtered_data['Hazardousness'].isin(['Hazardous[HAZ]', 'Non-hazardous[NHAZ]'])]

# Group data by year and hazardousness to calculate total values for each year
grouped_data = filtered_data.groupby(['Year', 'Hazardousness'])['VALUE'].sum().unstack()

# Get the list of years and waste types
years = [int(year) for year in grouped_data.index]  # Convert to standard Python integers
waste_types = ['Hazardous[HAZ]', 'Non-hazardous[NHAZ]']

# Prepare intensity values matrix
intensity_values = []
for waste_type in waste_types:
    intensity_values.append([
        float(grouped_data.loc[year, waste_type]) if year in grouped_data.index and waste_type in grouped_data.columns else 0.0
        for year in years
    ])

# Initialize the Polar Heatmap Chart
chart = lc.PolarChart(theme=lc.Themes.TurquoiseHexagon, title="Hazardous and Non-Hazardous Waste Heatmap")

# Add a heatmap series
heatmap_series = chart.add_heatmap_series(sectors=len(years), annuli=len(waste_types))

# Set intensity values for the heatmap
heatmap_series.invalidate_intensity_values(values=intensity_values)

# Define a color palette for the heatmap
color=heatmap_series.set_palette_coloring(
    steps=[
        {'value': 0, 'color': lc.Color('blue')},
        {'value': max(max(row) for row in intensity_values) / 2, 'color': lc.Color('yellow')},
        {'value': max(max(row) for row in intensity_values), 'color': lc.Color('red')},
    ],
    look_up_property='value',
    interpolate=True
)
chart.add_legend().add(color)
# Set intensity interpolation for smooth transitions
heatmap_series.set_intensity_interpolation('bilinear')

# Customize radial axis (years)
radial_axis = chart.get_radial_axis()
radial_axis.set_division(len(years))
radial_axis.set_tick_labels([str(year) for year in years])


# Display the chart
chart.open()


# -----------------------------------------------------------------------------------------------------
import pandas as pd
import lightningchart as lc
import numpy as np
import random

# Load your dataset
file_path = 'dataset/Batteries.xlsx'
sheet_data = pd.read_excel(file_path, sheet_name="Unpivoted")
# Filter the dataset for the column "Waste Category" and select "Batteries and accumulators wastes[W0841]"
filtered_data = sheet_data[sheet_data["Waste Category"] == "Batteries and accumulators wastes[W0841]"]

#
filtered_data = sheet_data[~sheet_data["NACE Rev. 2 Activity"].str.strip().str.contains("TOTAL_HH", case=False, na=False)]


# License key
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Group data by year and activity to calculate total values for each activity in each year
grouped_data = filtered_data.groupby(['Year', 'NACE Rev. 2 Activity'])['VALUE'].sum().unstack()

# Normalize data to calculate relative shares (percentages)
normalized_data = grouped_data.div(grouped_data.sum(axis=1), axis=0).fillna(0)

# Extract short titles (content inside parentheses)
short_titles = [activity.split("(")[-1].strip(")") for activity in grouped_data.columns]

# Get the list of years
years = [int(year) for year in grouped_data.index]

# Initialize the Polar Area Chart
chart = lc.PolarChart(
    title="Relative Share of Activities by Year",
    theme=lc.Themes.TurquoiseHexagon
)

# Add a legend to the chart
legend = chart.add_legend().set_title("Activities Legend")

# Function to generate random colors
def get_random_color():
    return lc.Color(f'#{random.randint(0, 0xFFFFFF):06x}')

# Add area series for each activity with custom colors
for activity, short_title in zip(grouped_data.columns, short_titles):
    # Prepare data points with angles (years mapped to 0-360) and amplitudes (relative share)
    data_points = [
        {"angle": angle, "amplitude": value}
        for angle, value in zip(np.linspace(0, 360, len(years)), normalized_data[activity].tolist())
    ]
    # Generate a random color for the activity
    color = get_random_color()
    series = chart.add_area_series().set_name(short_title).set_stroke(thickness=2, color=color).set_data(data_points)
    legend.add(series)  # Add the series to the legend

# Customize the radial axis
radial_axis = chart.get_radial_axis()
radial_axis.set_title("Relative Share (%)")
radial_axis.set_interval(0, 1)  # Percentages normalized to [0, 1]

# Customize the angular axis (years)
angular_axis = chart.get_radial_axis()
angular_axis.set_division(len(years))
angular_axis.set_tick_labels([str(year) for year in years])

# Open the chart
chart.open()
