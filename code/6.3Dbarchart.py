import pandas as pd
import lightningchart as lc
import numpy as np

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'dataset/Batteries.xlsx'
sheet_name = 'Unpivoted'
data = pd.read_excel(file_path, sheet_name=sheet_name)

filtered_data = data[
    (data['VALUE'] != 0) &
    (data['VALUE'].notnull()) &
    (data['Waste Category'] == 'Chemical wastes[W02A]')
]

top_activities = (
    filtered_data.groupby('NACE Rev. 2 Activity')['VALUE'].sum()
    .sort_values(ascending=False)
    .head(5).index
)
filtered_data = filtered_data[filtered_data['NACE Rev. 2 Activity'].isin(top_activities)]

filtered_data['Year'] = filtered_data['Year'].astype(int).apply(int)
filtered_data['VALUE'] = filtered_data['VALUE'].astype(float).apply(float)

activities = [activity.split('(')[-1].strip(')') for activity in filtered_data['NACE Rev. 2 Activity'].unique()]

years = sorted([int(year) for year in filtered_data['Year'].unique()])

chart = lc.Chart3D(
    theme=lc.Themes.Dark,
    title="3D Visualization of Chemical Wastes by Activity"
)

chart.get_default_x_axis().set_title("Year")
chart.get_default_y_axis().set_title("Value (Waste)")
chart.get_default_z_axis().set_title("Activity")

x_axis = chart.get_default_x_axis()
x_axis.set_interval(min(years), max(years))
x_axis.set_tick_strategy('Empty')

for year in years:
    tick = x_axis.add_custom_tick()
    tick.set_value(float(year))
    tick.set_text(str(year))

z_axis = chart.get_default_z_axis()
z_axis.set_interval(0, len(activities) - 1)
z_axis.set_tick_strategy('Empty')

for i, activity in enumerate(activities):
    tick = z_axis.add_custom_tick()
    tick.set_value(float(i))
    tick.set_text(activity)

box_series = chart.add_box_series()

color= box_series.set_palette_coloring(
    steps=[
        {'value': 0.0, 'color': lc.Color('blue')},
        {'value': 0.25, 'color': lc.Color('green')},
        {'value': 0.5, 'color': lc.Color('yellow')},
        {'value': 0.75, 'color': lc.Color('orange')},
        {'value': 1.0, 'color': lc.Color('red')}
    ],
    percentage_values=True,
    look_up_property='y'
)
chart.add_legend().add(color)
def generate_static_boxes(activities, years):
    boxes = []
    for i, activity_full in enumerate(filtered_data['NACE Rev. 2 Activity'].unique()):
        for year in years:
            total_value = filtered_data[
                (filtered_data['NACE Rev. 2 Activity'] == activity_full) &
                (filtered_data['Year'] == year)
            ]['VALUE'].sum()
            boxes.append({
                'xCenter': float(year),
                'yCenter': float(total_value) / 2,
                'zCenter': i,
                'xSize': 2.0,
                'ySize': float(total_value),
                'zSize': 1.0
            })
    return boxes

static_boxes = generate_static_boxes(activities, years)
box_series.add(static_boxes)

chart.open()
