import lightningchart as lc
import pandas as pd
import numpy as np
import random

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'dataset/Batteries.xlsx'
sheet_data = pd.read_excel(file_path, sheet_name="Unpivoted")

# chart 1: Intensity of Waste Production by Economic Activities and Hazard Types
dashboard = lc.Dashboard(columns=2, rows=2, theme=lc.Themes.TurquoiseHexagon)

filtered_data = sheet_data[sheet_data["Waste Category"] == "Batteries and accumulators wastes[W0841]"]
filtered_data = sheet_data[~sheet_data["NACE Rev. 2 Activity"].str.strip().str.contains("TOTAL_HH", case=False, na=False)]

chart = dashboard.PolarChart(column_index=0, row_index=0)
chart.set_title("Intensity of Waste Production by Economic Activities and Hazard Types")

heatmap_data = filtered_data.pivot_table(
    index='Hazardousness',
    columns='NACE Rev. 2 Activity',
    values='VALUE',
    aggfunc='sum',
    fill_value=0
)

heatmap_data_matrix = heatmap_data.values.tolist()

heatmap_series = chart.add_heatmap_series(sectors=len(heatmap_data.columns), annuli=len(heatmap_data.index))
heatmap_series.invalidate_intensity_values(values=heatmap_data_matrix)

color = heatmap_series.set_palette_coloring(
    steps=[
        {'value': min(map(min, heatmap_data_matrix)), 'color': lc.Color('blue')},
        {'value': max(map(max, heatmap_data_matrix)) / 2, 'color': lc.Color('green')},
        {'value': max(map(max, heatmap_data_matrix)), 'color': lc.Color('red')},
    ],
    look_up_property='value',
    interpolate=True
)
chart.add_legend().add(color)
heatmap_series.set_intensity_interpolation('bilinear')

# ---------------------------------------------------------------------------------------------------------------------
# chart 2: Annual Trends of Hazardous and Non-Hazardous Waste Production
filtered_data = filtered_data[filtered_data['Hazardousness'].isin(['Hazardous[HAZ]', 'Non-hazardous[NHAZ]'])]
grouped_data = filtered_data.groupby(['Year', 'Hazardousness'])['VALUE'].sum().unstack()

chart = dashboard.PolarChart(column_index=1, row_index=0)
chart.set_title("Annual Trends of Hazardous and Non-Hazardous Waste Production")


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
radial_axis.set_interval(0, grouped_data.max().max())

angular_axis = chart.get_radial_axis()
angular_axis.set_division(len(years))
angular_axis.set_tick_labels([str(year) for year in years])


# ---------------------------------------------------------------------------------------------------------------------
# chart 3: Yearly Waste Intensity by Hazardousness
filtered_data = filtered_data[sheet_data['Hazardousness'].isin(['Hazardous[HAZ]', 'Non-hazardous[NHAZ]'])]

grouped_data = filtered_data.groupby(['Year', 'Hazardousness'])['VALUE'].sum().unstack()

years = [int(year) for year in grouped_data.index]
waste_types = ['Hazardous[HAZ]', 'Non-hazardous[NHAZ]']

intensity_values = []
for waste_type in waste_types:
    intensity_values.append([
        float(grouped_data.loc[year, waste_type]) if year in grouped_data.index and waste_type in grouped_data.columns else 0.0
        for year in years
    ])

chart = dashboard.PolarChart(column_index=0, row_index=1)
chart.set_title("Yearly Waste Intensity by Hazardousness")


heatmap_series = chart.add_heatmap_series(sectors=len(years), annuli=len(waste_types))
heatmap_series.invalidate_intensity_values(values=intensity_values)

color = heatmap_series.set_palette_coloring(
    steps=[
        {'value': 0, 'color': lc.Color('blue')},
        {'value': max(max(row) for row in intensity_values) / 2, 'color': lc.Color('yellow')},
        {'value': max(max(row) for row in intensity_values), 'color': lc.Color('red')},
    ],
    look_up_property='value',
    interpolate=True
)
chart.add_legend().add(color)
heatmap_series.set_intensity_interpolation('bilinear')

radial_axis = chart.get_radial_axis()
radial_axis.set_division(len(years))
radial_axis.set_tick_labels([str(year) for year in years])

# ---------------------------------------------------------------------------------------------------------------------
# chart 4: Relative Contributions of Economic Activities to Waste Production
chart = dashboard.PolarChart(column_index=1, row_index=1)
chart.set_title("Relative Contributions of Economic Activities")

filtered_data = sheet_data[sheet_data["Waste Category"] == "Batteries and accumulators wastes[W0841]"]
filtered_data = sheet_data[~sheet_data["NACE Rev. 2 Activity"].str.strip().str.contains("TOTAL_HH", case=False, na=False)]
grouped_data = filtered_data.groupby(['Year', 'NACE Rev. 2 Activity'])['VALUE'].sum().unstack()

normalized_data = grouped_data.div(grouped_data.sum(axis=1), axis=0).fillna(0)

short_titles = [activity.split("(")[-1].strip(")") for activity in grouped_data.columns]

years = [int(year) for year in grouped_data.index]

legend = chart.add_legend().set_title("Activities Legend")

def get_random_color():
    return lc.Color(f'#{random.randint(0, 0xFFFFFF):06x}')

for activity, short_title in zip(grouped_data.columns, short_titles):
    data_points = [
        {"angle": angle, "amplitude": value}
        for angle, value in zip(np.linspace(0, 360, len(years)), normalized_data[activity].tolist())
    ]
    color = get_random_color()
    series = chart.add_area_series().set_name(short_title).set_stroke(thickness=2, color=color).set_data(data_points)
    legend.add(series)

radial_axis = chart.get_radial_axis()
radial_axis.set_title("Relative Share (%)")
radial_axis.set_interval(0, 1)

angular_axis = chart.get_radial_axis()
angular_axis.set_division(len(years))
angular_axis.set_tick_labels([str(year) for year in years])

dashboard.open()


# 
# This code creates a dashboard using the LightningChart library to display four Polar Charts. Each chart visualizes different aspects of waste production data from a dataset. The charts include:

# Polar Heatmap: Shows the intensity of waste production by different economic activities (NACE Rev. 2 Activity) and waste types (Hazardous and Non-Hazardous).
# Line Chart: Displays the trends of hazardous and non-hazardous waste over the years, using lines for each type.
# Yearly Heatmap: Visualizes the yearly intensity of waste production, categorized by hazardous and non-hazardous waste.
# Relative Share Chart: Illustrates the relative contributions of various economic activities to waste production over the years.