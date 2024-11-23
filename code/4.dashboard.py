import pandas as pd
import lightningchart as lc
import numpy as np
import random

# License key
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load dataset
file_path = 'dataset/Batteries.xlsx'
sheet_data = pd.read_excel(file_path, sheet_name="Unpivoted")

# Filter the dataset
filtered_data = sheet_data[sheet_data["Waste Category"] == "Batteries and accumulators wastes[W0841]"]
filtered_data = sheet_data[~sheet_data["NACE Rev. 2 Activity"].str.strip().str.contains("TOTAL_HH", case=False, na=False)]

# Initialize the Dashboard
dashboard = lc.Dashboard(columns=2, rows=2, theme=lc.Themes.TurquoiseHexagon)

# Polar Heatmap
heatmap_data = filtered_data.pivot_table(
    index='Hazardousness',
    columns='NACE Rev. 2 Activity',
    values='VALUE',
    aggfunc='sum',
    fill_value=0
)
heatmap_data_matrix = heatmap_data.values.tolist()

polar_heatmap = dashboard.PolarChart(column_index=0, row_index=0)
polar_heatmap.set_title("Polar Heatmap")
heatmap_series = polar_heatmap.add_heatmap_series(sectors=len(heatmap_data.columns), annuli=len(heatmap_data.index))
heatmap_series.invalidate_intensity_values(values=heatmap_data_matrix)
heatmap_series.set_palette_coloring(
    steps=[
        {'value': 0, 'color': lc.Color('blue')},
        {'value': max(map(max, heatmap_data_matrix)) / 2, 'color': lc.Color('green')},
        {'value': max(map(max, heatmap_data_matrix)), 'color': lc.Color('red')}
    ],
    look_up_property='value',
    interpolate=True
)

# Polar Line Chart
filtered_data = filtered_data[filtered_data['Hazardousness'].isin(['Hazardous[HAZ]', 'Non-hazardous[NHAZ]'])]
grouped_data = filtered_data.groupby(['Year', 'Hazardousness'])['VALUE'].sum().unstack()

polar_line_chart = dashboard.PolarChart(column_index=1, row_index=0)
polar_line_chart.set_title("Line Chart: Waste Types")

colors = {'Hazardous[HAZ]': lc.Color('red'), 'Non-hazardous[NHAZ]': lc.Color('blue')}
line_series = {}
years = grouped_data.index.values
min_year, max_year = int(min(years)), int(max(years))

def year_to_angle(year):
    return np.interp(year, (min_year, max_year), (0, 360))

for waste_type in ['Hazardous[HAZ]', 'Non-hazardous[NHAZ]']:
    points = []
    for year in years:
        value = grouped_data.loc[year, waste_type] if waste_type in grouped_data.columns else 0
        angle = year_to_angle(int(year))
        points.append({'angle': angle, 'amplitude': float(value)})
    series = polar_line_chart.add_point_line_series().set_name(waste_type).set_stroke(thickness=2, color=colors[waste_type])
    series.set_data(points)

# Polar Area Chart
grouped_data = filtered_data.groupby(['Year', 'NACE Rev. 2 Activity'])['VALUE'].sum().unstack()
normalized_data = grouped_data.div(grouped_data.sum(axis=1), axis=0).fillna(0)
short_titles = [activity.split("(")[-1].strip(")") for activity in grouped_data.columns]

polar_area_chart = dashboard.PolarChart(column_index=0, row_index=1)
polar_area_chart.set_title("Relative Shares")
for activity, short_title in zip(grouped_data.columns, short_titles):
    data_points = [
        {"angle": angle, "amplitude": value}
        for angle, value in zip(np.linspace(0, 360, len(years)), normalized_data[activity].tolist())
    ]
    polar_area_chart.add_area_series().set_name(short_title).set_data(data_points)

# Polar Heatmap by Year
intensity_values = []
for waste_type in ['Hazardous[HAZ]', 'Non-hazardous[NHAZ]']:
    intensity_values.append([
        float(grouped_data.loc[year, waste_type]) if year in grouped_data.index and waste_type in grouped_data.columns else 0.0
        for year in years
    ])

polar_year_heatmap = dashboard.PolarChart(column_index=1, row_index=1)
polar_year_heatmap.set_title("Heatmap: Yearly Hazardousness")
yearly_heatmap_series = polar_year_heatmap.add_heatmap_series(sectors=len(years), annuli=len(['Hazardous[HAZ]', 'Non-hazardous[NHAZ]']))
yearly_heatmap_series.invalidate_intensity_values(values=intensity_values)
yearly_heatmap_series.set_palette_coloring(
    steps=[
        {'value': 0, 'color': lc.Color('blue')},
        {'value': max(max(row) for row in intensity_values) / 2, 'color': lc.Color('yellow')},
        {'value': max(max(row) for row in intensity_values), 'color': lc.Color('red')}
    ],
    look_up_property='value',
    interpolate=True
)

# Open the Dashboard
dashboard.open()
