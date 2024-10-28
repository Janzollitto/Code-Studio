import geopandas as gpd
import pandas as pd
import numpy as np
import os

# Ask the user for the shapefile location and filename
shapefile_location = input("Enter the folder path for the shapefile: ")
shapefile_name = input("Enter the shapefile name (e.g., Urbanized Area Parcels.shp): ")

# Load the shapefile
shapefile_path = os.path.join(shapefile_location, shapefile_name)
gdf = gpd.read_file(shapefile_path)

# Drop rows with null geometries
gdf = gdf.dropna(subset=['geometry'])

# Calculate width using the bounding box and convert acres to square feet
# Assuming 'width' refers to one dimension and you're converting area to square footage
gdf['width'] = gdf.geometry.apply(lambda geom: (geom.bounds[2] - geom.bounds[0]) * 43560

# Ask the user for the field to use
field_name = input("Enter the field name to use for grouping: ")

# Prompt for output folder name and location
output_folder_name = input("Please enter the name of the new folder: ")
output_location = input("Please enter the full path where you want to save the folder (e.g., C:/Users/YourName/Documents): ")

# Create the full folder path
folder_path = os.path.join(output_location, output_folder_name)

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created.")
else:
    print(f"Folder '{folder_path}' already exists.")

# Save the original data with all columns including the new width column
data_file_path = os.path.join(folder_path, f"lot_width_data.csv")
gdf.to_csv(data_file_path, index=False)

# Calculate statistics by the user-defined field
stats = gdf.groupby(field_name)['width'].describe()
stats_file_path = os.path.join(folder_path, f"lot_width_stats.csv")
stats.to_csv(stats_file_path)

# Define bin edges for histogram
bin_edges = np.arange(0, gdf['width'].max() + 5, 5)

# Initialize a list to hold histogram data for each group
hist_data = []

# Calculate the histogram for each unique value in the user-defined field
for value in gdf[field_name].unique():
    value_data = gdf[gdf[field_name] == value]['width'].dropna()
    hist, _ = np.histogram(value_data, bins=bin_edges)
    hist_data.append(hist)

    # Count occurrences of the value in the user-defined field
    count = gdf[field_name].value_counts().get(value, 0)
    print(f"Count of {value} parcels: {count}")

# Create bin labels based on edges
bin_labels = [f"{bin_edges[i]} - {bin_edges[i + 1]}" for i in range(len(bin_edges) - 1)]

# Create a DataFrame with histogram data
hist_df = pd.DataFrame(hist_data, columns=bin_labels, index=gdf[field_name].unique())

# Save the histogram DataFrame to CSV
hist_file_path = os.path.join(folder_path, f"lot_width_histogram_table.csv")
hist_df.to_csv(hist_file_path)

# Create a README file with detailed content
readme_content = """# Lot Width Analysis README

This document provides an overview of the output files generated from the Lot Width Analysis.

## Output Files
1. **lot_width_data.csv**:
    - Contains the original dataset with an added column for "width," which represents the calculated width of each parcel.
2. **lot_width_stats.csv**:
    - Contains aggregated statistics grouped by the specified field. The following statistics are included:
     - **Average Width**: The mean width of parcels within each group.
     - **Minimum Width**: The smallest width recorded in the group.
     - **Maximum Width**: The largest width recorded in the group.
     - **Count**: The total number of parcels within the group.
     - **Standard Deviation (Std_Dev)**: Measures the amount of variation or dispersion in widths.
     - **Variance**: The square of the standard deviation, representing the dispersion of widths.
     - **Median**: The middle value of the widths when sorted.
     - **Q1**: The first quartile (25th percentile) of widths.
     - **Q3**: The third quartile (75th percentile) of widths.
     - **IQR**: The interquartile range, calculated as Q3 - Q1, which measures the spread of the middle 50% of data.
3. **lot_width_histogram_table.csv**:
    - Contains histogram data that shows the frequency of width values for each group. The histogram is divided into bins of width 5.
     - **Bin Start**: The starting value of each bin.
     - **Bin End**: The ending value of each bin.
     - **Frequency**: The number of parcels that fall within each bin range.

## Interpreting the Statistics
- **Understanding Width Statistics**: The statistics help you understand the distribution of parcel widths in different groups. The average gives a general idea of the typical parcel size, while the minimum and maximum provide the range.
- **Variation and Consistency**: Standard deviation and variance indicate how much the widths vary within each group. A low standard deviation means the widths are similar, while a high standard deviation indicates more variability.
- **Quartiles and IQR**: The quartiles and IQR can help identify outliers and understand the spread of the data. If the IQR is small relative to the range, the widths are closely grouped around the median.

This analysis can help inform zoning decisions, development planning, and land use assessments.

## Contact Information
For further questions or clarifications, please contact Jonathan Anzollitto.
"""

# Save the README file
readme_file_path = os.path.join(folder_path, "README.txt")
with open(readme_file_path, 'w') as readme_file:
    readme_file.write(readme_content)

print("All output files have been saved successfully.")
