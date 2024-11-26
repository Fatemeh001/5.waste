


import lightningchart as lc
import pandas as pd

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'dataset/Batteries.xlsx'
sheet_name = 'Unpivoted'
data = pd.read_excel(file_path, sheet_name=sheet_name)


all_activities_full = data.groupby(["Year", "NACE Rev. 2 Activity"])["VALUE"].sum().unstack()

years = all_activities_full.index.astype(int).tolist()
all_activities_full = all_activities_full.astype(float) / 1e6

short_titles = [activity.split("(")[-1].strip(")") for activity in all_activities_full.columns]

rows, cols = 4, 5
dashboard = lc.Dashboard(columns=cols, rows=rows, theme=lc.Themes.Dark)

for i, (activity, short_title) in enumerate(zip(all_activities_full.columns, short_titles)):
    row_index = i // cols
    col_index = i % cols

    chart = dashboard.ChartXY(
        column_index=col_index,
        row_index=row_index,
        title=short_title
    )
    chart.set_title(short_title)

    chart.set_mouse_interaction_rectangle_zoom(True)
    chart.set_cursor_mode("show-all-interpolated")

    chart.add_area_series(data_pattern="ProgressiveX").append_samples(
        x_values=years,
        y_values=all_activities_full[activity].fillna(0).tolist()
    )

    x_axis = chart.get_default_x_axis()
    y_axis = chart.get_default_y_axis()

    x_axis.set_title("")
    x_axis.set_tick_strategy('Empty')

    # Add custom ticks for every 5 years
    for year in range(min(years), max(years) + 1):
        if year % 5 == 0:
            custom_tick = x_axis.add_custom_tick()
            custom_tick.set_value(year)
            custom_tick.set_text(str(year))

    x_axis.set_interval(min(years), max(years))

    if col_index == 0:
        y_axis.set_title("Value (Millions)")
    else:
        y_axis.set_title("")

dashboard.open()







