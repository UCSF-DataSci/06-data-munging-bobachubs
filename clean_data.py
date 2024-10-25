import argparse
import pandas as pd

DEFAULT_INPUT_FILE = 'messy_population_data.csv'
DEFAULT_OUTPUT_FILE = 'cleaned_population_data.csv'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a clean dataset from a messy CSV file.")
    parser.add_argument("--input_file", default=DEFAULT_INPUT_FILE, help="Path to the input CSV file")
    parser.add_argument("--output_file", default=DEFAULT_OUTPUT_FILE, help="Path to save the clean CSV file")
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file

# Need to get rid of null and duplicate values so we can start cleaning!
    df_messy = pd.read_csv(input_file)

    print(df_messy.info())
    print
    print("dropping NAs...")
    # Get rid of NAs, now all columns are even
    # print(df_messy.isnull().sum())
    df_messy.dropna(inplace=True)

    print(df_messy.info())
    print("dropping duplicates...")
    # Ger rid of duplicates
    # print(df_messy.duplicated().sum())
    df_messy = df_messy[~df_messy.duplicated()]

    print("changing datatypes...")
    # Change to correct datatypes
    df_messy.age = df_messy.age.astype(int)
    df_messy.gender = df_messy.gender.astype(int)
    df_messy.year = df_messy.year.astype(int)
    df_messy.population = df_messy.population.astype(int)
    # print(df_messy.info())

    print(df_messy.describe())
    print("dropping bogus values...")
    # get rid of bogus values
    df_messy = df_messy[df_messy.year <= 2024]
    df_messy = df_messy[df_messy.gender < 3]

    print(df_messy.describe())
    print("dropping outliers...")
    #get rid of outliers in the population using the 1-99% quantiles
    df_messy = df_messy[(df_messy.population.quantile (0.01) < df_messy.population) &
                        (df_messy.population < df_messy.population.quantile(0.99))]

    print(df_messy.describe())
    print(df_messy.info())

    df_messy.to_csv(output_file, index=False)
    print("Cleaned data saved to: ", output_file)