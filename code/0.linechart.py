

import lightningchart as lc
import pandas as pd

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'dataset/Batteries.xlsx'
sheet_name = 'Unpivoted'
data = pd.read_excel(file_path, sheet_name=sheet_name)

filtered_data = data[
    (data['VALUE'] != 0) &
    (data['VALUE'].notnull()) &
    (data['Waste Category'] == 'Acid, alkaline or saline wastes[W012]')
]

all_activities_full = data.groupby(["Year", "NACE Rev. 2 Activity"])["VALUE"].sum().unstack()

# Define selected activities explicitly
selected_activities = [
    'Mining and quarrying (B)',
    'Services (except wholesale of waste and scrap)  (G-U_X_G4677)',
    'Construction (F)',
    'Manufacturing (C)','Manufacture of food products; beverages and tobacco products (C10-C12)',
    'Waste collection, treatment and disposal activities; materials recovery (E38)'
]

filtered_activities = all_activities_full[selected_activities]

# Extract shortened titles from activities (text inside parentheses)
short_titles = [activity.split("(")[-1].strip(")") for activity in filtered_activities.columns]

# Initialize a single ChartXY
chart = lc.ChartXY(
    theme=lc.Themes.Dark,
    title="Selected Activities Trends"
)

# Configure title position
chart.set_title_position("center-top")

# Add spline series for each activity with unique colors and proper legend labels
legend_box = chart.add_legend()
for activity, short_title in zip(filtered_activities.columns, short_titles):
    spline_series = chart.add_spline_series()
    spline_series.set_name(activity)  # Set the activity name as the legend label
    spline_series.append_samples(
        x_values=filtered_activities.index.tolist(),
        y_values=filtered_activities[activity].fillna(0).tolist()
    )
    legend_box.add(spline_series)  # Link the series to the legend



x_axis = chart.get_default_x_axis()
y_axis = chart.get_default_y_axis()

x_axis.set_title("year")
x_axis.set_tick_strategy('Empty')
y_axis.set_title("value")

years = all_activities_full.index.astype(int).tolist()
    # Add custom ticks for every 5 years
for year in range(min(years), max(years) + 1):
        if year % 1 == 0:
            custom_tick = x_axis.add_custom_tick()
            custom_tick.set_value(year)
            custom_tick.set_text(str(year))

x_axis.set_interval(min(years), max(years))
# Enable zoom and pan interactions
chart.set_mouse_interaction_wheel_zoom(True)
chart.set_mouse_interaction_pan(True)

# Open the chart
chart.open()
