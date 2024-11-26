import lightningchart as lc
import pandas as pd
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
grouped_data_percent = grouped_data.div(grouped_data.sum(axis=1), axis=0) * 100

years = grouped_data.index.tolist()
absolute_values = grouped_data.fillna(0).values.T
relative_values = grouped_data_percent.fillna(0).values.T
activities = grouped_data.columns.tolist()

chart = lc.ChartXY(theme=lc.Themes.Dark, title="Total Waste (Tonnes)")
short_titles = [activity.split("(")[-1].strip(")") for activity in grouped_data.columns]

for activity, data, short_title in zip(grouped_data.columns, absolute_values, short_titles):
    series = chart.add_area_series().set_name(short_title)
    series.add(years, data.tolist())

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

chart.add_legend().add(chart)

chart.open()
