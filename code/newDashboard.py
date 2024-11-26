import lightningchart as lc
import pandas as pd
import numpy as np

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

dashboard = lc.Dashboard(rows=2, columns=2, theme=lc.Themes.TurquoiseHexagon)

file_path = 'dataset/Batteries.xlsx'
sheet_name = 'Unpivoted'
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Chart 1
filtered_data = data[
    (data['VALUE'] != 0) &
    (data['VALUE'].notnull()) &
    (data['Waste Category'] == 'Acid, alkaline or saline wastes[W012]')
]
all_activities_full = data.groupby(["Year", "NACE Rev. 2 Activity"])["VALUE"].sum().unstack()
selected_activities = [
    'Mining and quarrying (B)',
    'Services (except wholesale of waste and scrap)  (G-U_X_G4677)',
    'Construction (F)',
    'Manufacturing (C)', 'Manufacture of food products; beverages and tobacco products (C10-C12)',
    'Waste collection, treatment and disposal activities; materials recovery (E38)'
]
filtered_activities = all_activities_full[selected_activities]
short_titles = [activity.split("(")[-1].strip(")") for activity in filtered_activities.columns]
chart1 = dashboard.ChartXY(row_index=0, column_index=0, column_span=2, title="Trends of Selected Activities (Acid, Alkaline, or Saline Wastes)")
chart1.set_title_position("center-top")
legend_box1 = chart1.add_legend()
for activity, short_title in zip(filtered_activities.columns, short_titles):
    spline_series = chart1.add_spline_series()
    spline_series.set_name(short_title)
    spline_series.append_samples(
        x_values=filtered_activities.index.astype(int).tolist(),
        y_values=filtered_activities[activity].fillna(0).tolist()
    )
    legend_box1.add(spline_series)
x_axis1 = chart1.get_default_x_axis()
y_axis1 = chart1.get_default_y_axis()
x_axis1.set_title("year")
x_axis1.set_tick_strategy('Empty')
y_axis1.set_title("value")
years1 = filtered_activities.index.astype(int).tolist()
for year in range(int(min(years1)), int(max(years1)) + 1):
    custom_tick = x_axis1.add_custom_tick()
    custom_tick.set_value(int(year))  
    custom_tick.set_text(str(year))
x_axis1.set_interval(int(min(years1)), int(max(years1)))
chart1.set_mouse_interaction_wheel_zoom(True)
chart1.set_mouse_interaction_pan(True)

# Chart 2
filtered_data = data[
    (data['VALUE'] != 0) &
    (data['VALUE'].notnull()) &
    (data['Waste Category'] == 'Batteries and accumulators wastes[W0841]')
]
top_activities = (
    filtered_data.groupby('NACE Rev. 2 Activity')['VALUE'].sum()
    .sort_values(ascending=False)
    .head(5).index
)
filtered_data = filtered_data[filtered_data['NACE Rev. 2 Activity'].isin(top_activities)]
filtered_data['Year'] = filtered_data['Year'].astype(int)
filtered_data = filtered_data[filtered_data['Year'] % 2 == 0]
grouped_data = filtered_data.groupby(["Year", "NACE Rev. 2 Activity"])["VALUE"].sum().unstack()
absolute_values = grouped_data.fillna(0).values.T
activities = grouped_data.columns.tolist()
short_titles2 = [activity.split("(")[-1].strip(")") for activity in grouped_data.columns]
chart2 = dashboard.ChartXY(column_index=1, row_index=1, title="Total Waste from Top Activities (Batteries and Accumulators)")
for activity, data, short_title in zip(grouped_data.columns, absolute_values, short_titles2):
    series = chart2.add_area_series().set_name(short_title)
    series.add(grouped_data.index.astype(int).tolist(), data.tolist())
x_axis2 = chart2.get_default_x_axis()
x_axis2.set_title("Year")
x_axis2.set_tick_strategy('Empty')
for year in grouped_data.index.astype(int).tolist():
    custom_tick = x_axis2.add_custom_tick()
    custom_tick.set_value(int(year))  # تبدیل به int
    custom_tick.set_text(str(year))
y_axis2 = chart2.get_default_y_axis()
y_axis2.set_title("Value (Tonnes)")
chart2.add_legend().add(chart2)

# Chart 3

file_path = 'dataset/Batteries.xlsx'
sheet_name = 'Unpivoted'
data = pd.read_excel(file_path, sheet_name=sheet_name)

data['Waste Category'] = data['Waste Category'].str.strip()

if 'Chemical wastes[W02A]' in data['Waste Category'].unique():
    filtered_data = data[
        (data['VALUE'] != 0) & 
        (data['VALUE'].notnull()) &
        (data['Waste Category'] == 'Chemical wastes[W02A]')
    ]
else:
    raise ValueError("The specified 'Waste Category' value does not exist in the dataset.")

filtered_data['Year'] = filtered_data['Year'].astype(int)
filtered_data['VALUE'] = filtered_data['VALUE'].astype(float)
top_activities = (
    filtered_data.groupby('NACE Rev. 2 Activity')['VALUE'].sum()
    .sort_values(ascending=False)
    .head(5).index
)
filtered_data = filtered_data[filtered_data['NACE Rev. 2 Activity'].isin(top_activities)]
activities3 = [activity.split("(")[-1].strip(")") for activity in filtered_data['NACE Rev. 2 Activity'].unique()]
years3 = sorted(filtered_data['Year'].astype(int).unique())
chart3 = dashboard.Chart3D(column_index=0, row_index=1, title="Top 5 Activities (Chemical Wastes)")
chart3.get_default_x_axis().set_title("Year")
chart3.get_default_y_axis().set_title("Value (Waste)")
chart3.get_default_z_axis().set_title("Activity")
x_axis3 = chart3.get_default_x_axis()
x_axis3.set_interval(int(min(years3)), int(max(years3)))
x_axis3.set_tick_strategy('Empty')
for year in years3:
    tick = x_axis3.add_custom_tick()
    tick.set_value(int(year))  # تبدیل به int
    tick.set_text(str(year))
z_axis3 = chart3.get_default_z_axis()
z_axis3.set_interval(0, len(activities3) - 1)
z_axis3.set_tick_strategy('Empty')
for i, activity in enumerate(activities3):
    tick = z_axis3.add_custom_tick()
    tick.set_value(float(i))
    tick.set_text(activity)
box_series = chart3.add_box_series()
color = box_series.set_palette_coloring(
    steps=[
        {'value': 0.0, 'color': lc.Color('blue')},
        {'value': 0.25, 'color': lc.Color('yellow')},
        {'value': 0.5, 'color': lc.Color('green')},
        {'value': 0.75, 'color': lc.Color('orange')},
        {'value': 1.0, 'color': lc.Color('red')}
    ],
    percentage_values=True,
    look_up_property='y'
)
chart3.add_legend().add(color)

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
                'xSize': 2,
                'ySize': float(total_value),
                'zSize': 1
            })
    return boxes

static_boxes = generate_static_boxes(activities3, years3)
box_series.add(static_boxes)

dashboard.open()
