"""
Project Title: Global Data Center Infrastructure & Sustainability Explorer
Developer: Marbu Franklin Neal Jr.
Course: ISMG 4400 - Python Data Exploration Application
University: University of Colorado Denver

Project Description
-------------------
This Python application explores a global data center infrastructure dataset
using a menu-driven interface. The program allows users to load a dataset,
view summary statistics, search the data, perform analysis, create data
visualizations, and generate AI-driven insights.

The dataset examines global data center infrastructure including metrics
such as total data centers by country, hyperscale and colocation facilities,
power capacity, renewable energy usage, and internet infrastructure.

Technologies Used
-----------------
Python 3.13
Pandas - data loading and analysis
NumPy - numerical calculations
Matplotlib - data visualization
Regex - input validation and data cleaning
OpenAI API - AI-generated insights
python-dotenv - secure API key management
ChatGPT - coding structure and debugging assistance

Challenges & Solutions
----------------------
Two primary challenges occurred during development:

1. File Path Issues
The dataset initially failed to load due to directory differences between
Desktop, OneDrive, and the VS Code working environment. This was solved by
implementing a path-agnostic loading method using Python's os.path module,
which automatically locates the dataset in the script directory.

2. Data Cleaning
Several numeric columns contained non-numeric characters such as commas,
tildes (~), and percentage symbols. Regular Expressions (Regex) were used
to remove these characters before converting the values into numeric types
for statistical analysis.

AI Integration
--------------
The OpenAI API is integrated to generate AI-driven insights about global
data center infrastructure based on the dataset. API credentials are stored
securely using environment variables and a .env file rather than being
hardcoded in the script.

Dataset Source
--------------
Kaggle Dataset:
https://www.kaggle.com/datasets/rockyt07/da7
ta-center-dataset/data

Author
------
Marbu Franklin Neal Jr.
Colossians 3:23

# ==================================================
# IMPORT LIBRARIES
# ==================================================

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import re
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

# ==================================================
# GLOBAL VARIABLES
# ==================================================
data = None

# ==================================================
# DATASET COLUMN DEFINITIONS
# ==================================================
NUMERIC_COLUMNS = [
    "total_data_centers",
    "hyperscale_data_centers",
    "colocation_data_centers",
    "floor_space_sqft_total",
    "power_capacity_MW_total",
    "average_renewable_energy_usage_percent",
    "internet_penetration_percent",
    "avg_latency_to_global_hubs_ms",
    "number_of_fiber_connections",
    "growth_rate_of_data_centers_percent_per_year",
]
# ==================================================
# MENU DISPLAY AND INPUT VALIDATION
# ==================================================
# Dictionary to store menu options for application
MENU_OPTIONS = {
    "1": "Load up your Dataset",
    "2": "Display Summary Statistics",
    "3": "Search Dataset",
    "4": "Perform Data Analysis",
    "5": "Create Visualization",
    "6": "API Data Lookup",
    "7": "Exit"
}
#Here's a function to display the main menu
def display_menu():
    """
    Displays the main menu for the application.
    """
    print("\n===== Global Data Center Exploration Menu =====")
    
    for key, value in MENU_OPTIONS.items():
        print(f"{key}. {value}")

#Here's a function to validate the user's menu choice using regex
def validate_menu_choice():
    """
    Gives the user a menu of options 
    and validates that they enter a valid choice.
    Uses regex to ensure the input is a number between 1 and 7.
    """
    while True:
        choice = input ("What would you like to do today? (1-7): ").strip()

        # Regular expression to validate input
        if re.fullmatch(r"[1-7]", choice):
            return choice
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

# ==================================================
# DATASET LOADING AND CLEANING
# ==================================================
def load_dataset():
    """
    Loads Data Center Data from the script's local directory.
    """
    global data

    # 1. Automatically find the folder where THIS script is saved
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Use the exact name seen in your screenshot (try both common versions)
    file_options = ["Data Center Data.csv", "Data Center Data.csv.csv"]
    
    file_path = None
    for f in file_options:
        temp_path = os.path.join(script_dir, f)
        if os.path.exists(temp_path):
            file_path = temp_path
            break

    if not file_path:
        print(f"\n[ERROR] Still can't find the file in: {script_dir}")
        print(f"Files actually in this folder: {os.listdir(script_dir)}")
        return

    try:
        data = pd.read_csv(file_path)

        # CLEANING: Remove symbols like ~, %, and commas so numbers work
        for col in NUMERIC_COLUMNS:
            if col in data.columns:
                data[col] = data[col].astype(str).str.replace(r'[~,%\+]', '', regex=True)
                data[col] = pd.to_numeric(data[col], errors='coerce')

        print(f"\nSuccess! Loaded and cleaned: {os.path.basename(file_path)}")
        print(data.head())

    except Exception as e:
        print(f"An error occurred: {e}")
# ==================================================
# DATA EXPLORATION FUNCTIONS
# ==================================================
def display_summary_statistics():
    """
    Displays summary statistics for the numeric columns in the dataset.
    Checks if the dataset is loaded before attempting to display statistics.
    """
    global data

    if data is None:
        print("Please load a dataset first (Option 1) before trying to display summary statistics.")
        return
    
    print("\nSummary Statistics for Numeric Columns:")
    print(data[NUMERIC_COLUMNS].describe().transpose())

def search_dataset():
    """
    Allows the user to search the dataset based on a country or cloud provider.
    """
    global data

    if data is None:
        print("Please load a dataset first (Option 1).")
        return
    
    print("\nSearch Options:")
    print("1. Search by Country")
    print("2. Search by Cloud Provider")

    search_choice = input("Choose an option (1 or 2): ").strip()

    # Search by Country
    if search_choice == "1":
        search_term = input("Enter the country name: ").strip()
        column = "country"
        display_cols = ["country", "total_data_centers", "cloud_provider"]

    # Search by Cloud Provider
    elif search_choice == "2":
        search_term = input("Enter the cloud provider name: ").strip()
        column = "cloud_provider"
        display_cols = ["cloud_provider", "total_data_centers", "country"]

    else:
        print("Invalid Search Option. Please enter 1 or 2.")
        return

    # Perform the search
    try:
        # Check if the column actually exists (handles 'country' vs 'Country')
        actual_col = next((c for c in data.columns if c.lower() == column), None)
        
        if actual_col:
            # We use regex=False so users don't accidentally break it with symbols like + or *
            results = data[data[actual_col].astype(str).str.contains(search_term, case=False, na=False, regex=False)]
            
            print(f"\nFound {len(results)} matching result(s):")
            if not results.empty:
                print(results[display_cols].to_string(index=False))
            else:
                print("No matches found.")
        else:
            print(f"Error: Column '{column}' not found in the dataset.")

    except Exception as e:
        print(f"An error occurred during search: {e}")
# ==================================================
# DATA ANALYSIS FUNCTION(S)
# ==================================================
def data_analysis():
    """
    Performs data analysis using Pandas & Numpy.
    Includes sorting, averages, and comparisons between data centers based on various metrics.
    Checks if the dataset is loaded before attempting to perform data analysis.
    """
    global data

    if data is None:
        print("Please load a dataset first (Option 1) before trying to perform data analysis.")
        return
    
    print("\nData Analysis Options:")
    print("1. Top 10 Countries by Total Data Centers")
    print("2. Average Power Capacity")
    print("3. Compare Hyperscale vs Colocation Data Centers")
    print("4. Countries above average renewable energy usage")
    
    choice = input("Choose an option (1-4): ").strip()

    if choice == "1":
        top_10 = data.sort_values(by="total_data_centers", ascending=False).head(10)
        print("\nTop 10 Countries by Total Data Centers:")
        print(top_10[["country", "total_data_centers"]].to_string(index=False))

    elif choice == "2":
        # Use .median() and .max() directly on the dataframe column
        avg_power = data["power_capacity_MW_total"].mean()
        median_power = data["power_capacity_MW_total"].median() # Fixed
        max_power = data["power_capacity_MW_total"].max()

        print("\nPower Capacity Analysis:")
        print(f"Average Power Capacity (MW): {avg_power:.2f}")
        print(f"Median Power Capacity (MW): {median_power:.2f}")
        print(f"Maximum Power Capacity (MW): {max_power:.2f}")

    elif choice == "3":
        total_hyperscale = np.sum(data["hyperscale_data_centers"])
        total_colocation = np.sum(data["colocation_data_centers"])

        print("\nHyperscale vs Colocation Data Centers:")
        print(f"Total Hyperscale Data Centers: {int(total_hyperscale)}")
        print(f"Total Colocation Data Centers: {int(total_colocation)}")

        if total_hyperscale > total_colocation:
            print("Hyperscale data centers are more prevalent globally.")
        elif total_colocation > total_hyperscale:
            print("Colocation data centers are more prevalent globally.")
        else:
            print("Hyperscale and Colocation data centers are equally prevalent globally.")
    
    elif choice == "4":
        above_avg_renewable = data[data["average_renewable_energy_usage_percent"] > data["average_renewable_energy_usage_percent"].mean()]
        print(f"\nCountries with above average renewable energy usage ({len(above_avg_renewable)} countries):")
        print(above_avg_renewable[["country", "average_renewable_energy_usage_percent"]].to_string(index=False))

    
    else:
        print("Invalid analysis option. Please enter a number between 1 and 4.")

# ==================================================
# DATA VISUALIZATION
# ==================================================
def data_visualization():
    """
    Creates visualizations using Matplotlib.
    Includes bar chart, histogram, and scatter plot to visualize trends and comparisons in the data.
    Checks if the dataset is loaded before attempting to create visualizations.
    """
    global data

    if data is None:
        print("Please load a dataset first (Option 1) before trying to create visualizations.")
        return
    
    print("\nData Visualization Options:")
    print("1. Bar Chart: Top 10 Data Centers by Country")
    print("2. Histogram: Power Capacity")
    print("3. Pie Chart: Hyperscale vs Colocation Data Centers")    
    print("4. Scatter Plot: Renewable Energy vs Total Data Centers")

    choice = input("Choose an option (1-4): ").strip()

    if choice == "1":
        top_10 = data.sort_values(by="total_data_centers", ascending=False).head(10)

        plt.figure(figsize=(10,6))
        plt.bar(top_10["country"], top_10["total_data_centers"])

        plt.title("Top 10 Countries by Total Data Centers")
        plt.xlabel("Country")
        plt.ylabel("Total Data Centers")

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    elif choice == "2":
        plt.figure(figsize=(10,6))

        plt.hist(data["power_capacity_MW_total"], bins=15)

        plt.title("Distribution of Data Center Power Capacity")
        plt.xlabel("Power Capacity (MW)")
        plt.ylabel("Number of Countries")

        plt.tight_layout()
        plt.show()

    elif choice == "3":
        hyperscale = data["hyperscale_data_centers"].sum()
        colocation = data["colocation_data_centers"].sum()

        plt.figure(figsize=(8,8))

        plt.pie(
            [hyperscale, colocation],
            labels=["Hyperscale", "Colocation"],
            autopct="%1.1f%%"
        )

        plt.title("Hyperscale vs Colocation Data Centers")
        plt.show()
    
    elif choice == "4":
        plt.figure(figsize=(10,6))

        plt.scatter(
            data["average_renewable_energy_usage_percent"],
            data["total_data_centers"]
        )

        plt.title("Renewable Energy Usage vs Total Data Centers")
        plt.xlabel("Renewable Energy Usage (%)")
        plt.ylabel("Total Data Centers")

        plt.grid(True)
        plt.tight_layout()
        plt.yscale('log')
        plt.show()
    
    else:
        print("Invalid visualization option. Please enter a number between 1 and 4.")
# ==================================================
# AI API INTEGRATION
# ==================================================
def api_integration():
    global data
    if data is None:
        print("Please load a dataset first.")
        return

    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("API Key not found! Make sure your .env file is set up.")
        return

    client = OpenAI(api_key=api_key)

    # Use the dataset to generate a prompt for the AI. For example, we can ask about the country with the most data centers.
    top_country = data.sort_values(by="total_data_centers", ascending=False).iloc[0]["country"]
    prompt = f"In my dataset, {top_country} has the most data centers. Can you explain why this country is a global leader in data center infrastructure?"

    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Using a newer, faster model
            messages=[{"role": "user", "content": prompt}]
        )
        print("\n--- AI Insights ---")
        print(response.choices[0].message.content)
    
    except Exception as e:
        print(f"API Error: {e}")
# ==================================================
# MAIN PROGRAM CONTROLLER
# ==================================================
def main():
    """
    Main function to run the Data Center Exploration application.
    Displays the menu and calls the appropriate functions based on user input.
    Runs in a loop until the user chooses to exit.
    """
    while True:
        display_menu()
        choice = validate_menu_choice()

        if choice == "1":
            load_dataset()
        elif choice == "2":
            display_summary_statistics()
        elif choice == "3":
            search_dataset()
        elif choice == "4":
            data_analysis()
        elif choice == "5":
            data_visualization()
        elif choice == "6":
            api_integration()
        elif choice == "7":
            print("Exiting the application. Data Centers are pretty cool!")
            artistic_exit()
            break
# ==================================================
# USER ACCESS LOGGING SYSTEM
# ==================================================
# This section records who opens the program.
# The user is prompted to enter their name when the
# application starts. Their name and a timestamp are
# saved to a CSV file called "access_log.csv".
# This creates a simple audit trail showing who has
# accessed the Data Center Explorer application.
def log_user_access():
    """
    Prompts the user for their name and logs access to a CSV file.
    """
    user_name = input("Enter your name to access the Data Center Explorer: ").strip()

    if not user_name:
        user_name = "Anonymous"

    log_file = "access_log.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = pd.DataFrame([{
        "name": user_name,
        "timestamp": timestamp
    }])

    try:
        if os.path.exists(log_file):
            log_entry.to_csv(log_file, mode="a", header=False, index=False)
        else:
            log_entry.to_csv(log_file, mode="w", header=True, index=False)

        print(f"\nWelcome, {user_name}!")
        print("Your access has been logged.\n")

    except Exception as e:
        print(f"Error writing to access log: {e}")

    return user_name
# ==================================================
# TERMINAL ARTISTIC EXIT DISPLAY
# ==================================================
# This section prints a small ASCII art scene when the
# user exits the application. It serves as a creative
# visual element and signature for the program.
def artistic_exit():
    """
    Prints an artistic ASCII scene when the program exits.
    """
    print("""  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                 GLOBAL DATA CENTER EXPLORER

                       ___  ___  ___
                      |___||___||___|
                      |___||___||___|
                      |___||___||___|

                       \\   ||   //
                        \\  ||  //
                         \\ || //
                          \\||//
                           \\/
                          /\\
                         /  \\
                        / || \\
                       /  ||  \\
                      /   ||   \\

                   ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
                ~  DATA CENTERS IN THE CLOUD  ~
                   ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

           Hands on the keyboard. Systems in the cloud.

                     Built by FRNK.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""")


# Start the application
main()
