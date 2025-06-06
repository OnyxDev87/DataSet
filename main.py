# import necessary libraries
# pandas to read the CSV and to manipulate data
# matplotlib to plot the data
# mplcursors lets you hover over a line and see the value
# numpy for number stuff
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import numpy as np

# CSV filepath
CSV_FILE = "01 renewable-share-energy.csv"

# Check if the CSV file exists and read it
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    print(f"File not found: {CSV_FILE}")
    exit(1)
except Exception as e:
    print(f"Error reading file: {e}")
    exit(1)

# Check if the required columns are present in the DataFrame (DataFrame is a table-like structure in pandas)
required_columns = ["Entity", "Year", "Renewables (% equivalent primary energy)"]
if not all(col in df.columns for col in required_columns):
    print("CSV file missing required columns.")
    exit(1)

# Create a place to store the percent change of renewable energy generated for each entitiy
all_percent_changes = []
# Create a place to store the consistency scores for each entity
consistency_scores = []

# Function to calculate the percent change in renewable energy share for each entity
def calculate_percent_change(df, entity):
    # Make sure the entity exists in the DataFrame and sort the data by year
    entity_data = df[df["Entity"] == entity].sort_values("Year")
    # Calculate percent change from the first to the last year
    first_value = entity_data["Renewables (% equivalent primary energy)"].iloc[0]
    last_value = entity_data["Renewables (% equivalent primary energy)"].iloc[-1]
    percent_change = ((last_value - first_value) / first_value) * 100
    return percent_change

# Loop through each unique entity in the DataFrame and calculate the percent change
for entity in df["Entity"].unique():
    percent_change = calculate_percent_change(df, entity)
    all_percent_changes.append((entity, percent_change))

# Find the entity with the greatest and least percent change
greatest_change = max(all_percent_changes, key=lambda x: x[1])
least_change = min(all_percent_changes, key=lambda x: x[1])

# Print the summary of percent changes
def print_summary(all_percent_changes, greatest_change, least_change):
    # print("\nSummary of Percent Changes:")
    # for entity, change in all_percent_changes:
        # print(f"{entity}: {change:.2f}%")

    print(f"\nGreatest increase in renewable energy share: {greatest_change[0]} with {greatest_change[1]:.2f}%")
    print(f"Least increase in renewable energy share: {least_change[0]} with {least_change[1]:.2f}%")

# Function to plot the percent changes for all entities
def plot_percent_changes(all_percent_changes):
    plt.figure(figsize=(10, 6))
    # Plot each entity's renewable energy share over time
    for entity, change  in all_percent_changes:
        entity_data = df[df["Entity"] == entity].sort_values("Year")
        plt.plot(entity_data["Year"], entity_data["Renewables (% equivalent primary energy)"], marker='o', linestyle='-', label=entity)
    # Format the plot
    plt.title(f"Renewable Energy Share Over Time - ALL ENTITIES")
    plt.xlabel("Year")
    plt.ylabel("Renewables (% of primary energy)")
    plt.grid(True)
    plt.tight_layout()
    # Use mplcursors to let hovering show the value
    mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{sel.artist.get_label()}: {sel.target[1]:.2f}%"))
    plt.xticks(rotation=45)
    plt.show()

def calculate_consistency(df, entity):
    entity_data = df[df["Entity"] == entity].sort_values("Year")
    values = entity_data["Renewables (% equivalent primary energy)"].values
    if len(values) < 2:
        return None
    yearly_changes = np.diff(values)
    return np.std(yearly_changes)

for entity in df["Entity"].unique():
    std_dev = calculate_consistency(df, entity)
    if std_dev is not None:
        consistency_scores.append((entity, std_dev))

# Get the top 5 most consistent entities
top_consistent = sorted(consistency_scores, key=lambda x: x[1])[:5]

# Output functions
def write_percent_changes_to_file(all_percent_changes, filename="percent_changes.txt"):
    sorted_changes = sorted(all_percent_changes, key=lambda x: x[1], reverse=True)
    with open(filename, "w") as f:
        f.write("Ordered Percent Changes:\n")
        for entity, change in sorted_changes:
            f.write(f"{entity}: {change:.2f}%\n")
    return sorted_changes

def write_consistency_to_file(top_consistent, filename="most_consistent.txt"):
    with open(filename, "w") as f:
        f.write("Top 5 Most Consistent Entities (Lowest Std Dev):\n")
        for entity, std in top_consistent:
            f.write(f"{entity}: Std Dev = {std:.4f}\n")

def plot_current_renewable_share(df):
    # Plot the current renewable share for each entity
    plt.figure(figsize=(10, 6))
    current_year = df["Year"].max()
    current_data = df[df["Year"] == current_year]
    plt.bar(current_data["Entity"], current_data["Renewables (% equivalent primary energy)"], color='green')
    plt.title(f"Current Renewable Energy Share in {current_year}")
    plt.xlabel("Entity")
    plt.ylabel("Renewables (% of primary energy)")
    plt.xticks(rotation=90)
    plt.xticks(fontsize=7)
    plt.tight_layout()
    plt.show()

def print_ordered_percent_changes(all_percent_changes):
    # Sort the percent changes in descending order
    sorted_changes = sorted(all_percent_changes, key=lambda x: x[1], reverse=True)
    print("\nOrdered Percent Changes:")
    for entity, change in sorted_changes:
        print(f"{entity}: {change:.2f}%")

# Print the summary and plot the percent changes and write the stuff to files
sorted_changes = write_percent_changes_to_file(all_percent_changes)
write_consistency_to_file(top_consistent)
print_summary(all_percent_changes, greatest_change, least_change)
print_ordered_percent_changes(all_percent_changes)
# plot_percent_changes(all_percent_changes)
plot_current_renewable_share(df)
