import pandas as pd
import matplotlib.pyplot as plt

# Ask the user for the CSV file path
file_path = input("Enter the full path to the existing CSV file WITH the \file name: ")

# Load data from the provided CSV file
df = pd.read_csv(file_path)

# Define bin intervals with steps of 5,000 up to 1,000,000
bins = list(range(0, 1000001, 5000))
labels = [f'{i}-{i+4999}' for i in range(0, 1000000, 5000)]

# Initialize a dictionary to store all counts
all_counts = {'Label': labels}

# Loop through each column and process
for column in df.columns:
    data = df[column]

    # Create the histogram with specified bins
    counts, _, _ = plt.hist(data, bins=bins, alpha=0.7, color='blue', edgecolor='black')

    """
    # Add titles and labels
    plt.title(f'Histogram with 5000 Interval Bins for {column}')
    plt.xlabel('Value')
    plt.ylabel('Frequency')

    # Display the plot
    plt.show()
    """

    # Print the counts in each bin
    print(f'Counts for {column}:')
    non_zero_counts = []
    for label, count in zip(labels, counts):
        if count > 0:
            print(f'{label}: {count}')
            non_zero_counts.append(count)
        else:
            non_zero_counts.append(0)  # Keep zero counts for consistency

    all_counts[column] = non_zero_counts

# Ask the user for the output CSV file path
output_file_name = input("Enter the name for the output CSV file (without extension): ")
output_file_path = input("Enter the path to save the output CSV file: ")

# Construct the full output file path
output_file = f'{output_file_path}\\{output_file_name}.csv'

# Export all counts data to a single CSV file
counts_df = pd.DataFrame(all_counts)
counts_df = counts_df.loc[(counts_df.drop(columns=['Label']) != 0).any(axis=1)]  # Filter out rows where all columns except 'Label' are zero
counts_df.to_csv(output_file, index=False)

print(f'All counts data saved to {output_file}')

