import lightningchart as lc
import numpy as np
import pandas as pd

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'dataset/Batteries.xlsx'
data = pd.read_excel(file_path, sheet_name="Unpivoted")

filtered_data = data[
    (data['VALUE'] > 0) & 
    (data['VALUE'].notnull()) & 
    (data['Hazardousness'].notnull()) & 
    (~data['Hazardousness'].str.contains("Total", case=False, na=False))
]

grouped_data = filtered_data.groupby(['Year', 'Hazardousness'])['VALUE'].sum().unstack(fill_value=0)

x_values = grouped_data.index.to_numpy()
hazardousness_categories = grouped_data.columns
stacked_data = np.cumsum(grouped_data.values, axis=1)

chart = lc.ChartXY(
    theme=lc.Themes.Black,
    title="Hazardous vs Non-Hazardous Waste Over Time"
)

for i, category in enumerate(hazardousness_categories):
    series = chart.add_area_series()
    series.set_name(category)
    series.add(x_values, stacked_data[:, i])
    series.set(False)

x_axis = chart.get_default_x_axis()
x_axis.set_title("Year")
x_axis.set_tick_strategy('Empty')

years = grouped_data.index.astype(int).tolist()
for year in range(min(years), max(years) + 1):
    custom_tick = x_axis.add_custom_tick()
    custom_tick.set_value(year)
    custom_tick.set_text(str(year))

y_axis = chart.get_default_y_axis()
y_axis.set_title("Value (Tonnes)")

chart.add_legend(data=chart)

chart.open()
