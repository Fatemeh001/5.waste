import lightningchart as lc
import pandas as pd

# Set license key
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load your dataset
file_path = 'dataset/acid.xlsx'
sheet1_data = pd.read_excel(file_path, sheet_name="Unpivoted")

# Process data to get required format
all_activities_full = sheet1_data.groupby(["Year", "NACE Rev. 2 Activity"])["VALUE"].sum().unstack()

# Convert index and data to Python native types
years = all_activities_full.index.astype(int).tolist()  # Convert index to a list of Python int
all_activities_full = all_activities_full.astype(float) / 1e6  # Scale values to millions

# Extract shortened titles from activities (text inside parentheses)
short_titles = [activity.split("(")[-1].strip(")") for activity in all_activities_full.columns]

# Initialize a Dashboard
rows, cols = 4, 5  # Adjust number of rows and columns for the dashboard layout
dashboard = lc.Dashboard(columns=cols, rows=rows, theme=lc.Themes.Dark)

# Add visually enhanced charts for each activity
for i, (activity, short_title) in enumerate(zip(all_activities_full.columns, short_titles)):
    row_index = i // cols
    col_index = i % cols

    # Create a chart for each activity
    chart = dashboard.ChartXY(
        column_index=col_index,
        row_index=row_index,
        title=short_title
    )
    chart.set_title(short_title)  # Set activity name as the chart title

    # Enable advanced interaction modes
    chart.set_mouse_interaction_rectangle_zoom(True)
    chart.set_cursor_mode("show-all-interpolated")

    # Add an Area Series for enhanced visualization
    chart.add_area_series(data_pattern="ProgressiveX").append_samples(
        x_values=years,
        y_values=all_activities_full[activity].fillna(0).tolist()
    )

    # Customize the axes
    x_axis = chart.get_default_x_axis()
    y_axis = chart.get_default_y_axis()

    # Hide X Axis titles for all charts
    x_axis.set_title("")
    x_axis.set_interval(min(years), max(years))  # Ensure consistent intervals

    # Show Y Axis title only for charts in the leftmost column
    if col_index == 0:
        y_axis.set_title("Value (Millions)")
    else:
        y_axis.set_title("")

# Adjust axis colors for better visibility using preset or default colors
x_axis.set_stroke(thickness=2, color=0xFFFFFF)  # White color in hex
y_axis.set_stroke(thickness=2, color=0xFFFFFF)  # White color in hex


# Open the dashboard
dashboard.open()
