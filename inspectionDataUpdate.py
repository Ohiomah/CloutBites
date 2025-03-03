import csv
import pandas as pd


# def process_restaurant_data(input_filepath, output_filepath):
#     """Processes restaurant data from a CSV, keeps selected columns,
#     removes duplicates, and writes the cleaned data to a new CSV.
#     """
#     try:

#         # Pandas for efficient CSV processing
#         df = pd.read_csv(input_filepath)

#         # Select desired columns
#         selected_columns = ["DBA", "BORO", "CUISINE DESCRIPTION", "SCORE", "GRADE"]
#         df = df[selected_columns]

#         # Remove duplicate rows
#         df.drop_duplicates(inplace=True)

#         # Write to new CSV
#         df.to_csv(output_filepath, index=False)  # index=False avoids writing row numbers
#         print(f"Cleaned restaurant data saved to {output_filepath}")

#     except FileNotFoundError:
#         print(f"Error: Input file '{input_filepath}' not found.")
#     except Exception as e:
#         print(f"An error occurred during processing: {e}")


# INPUT_FILEPATH = "outputs/NYC_Restaurant_Inspections.csv"    
# OUTPUT_FILEPATH = "outputs/cleaned_restaurants.csv"  

# process_restaurant_data(INPUT_FILEPATH, OUTPUT_FILEPATH)

# now merge the restaurants and inspections

def merge_restaurant_data(csv1_path, csv2_path, output_path):

    """Merges two restaurant CSV files based on matching names (case-insensitive)."""
    try:
        df1 = pd.read_csv(csv1_path)
        df2 = pd.read_csv(csv2_path)


        # Convert names to lowercase for case-insensitive matching
        df1['DBA'] = df1['DBA'].str.lower()
        df2['name'] = df2['name'].str.lower()




        # Merge based on lowercase names
        merged_df = pd.merge(df2, df1, left_on='name', right_on='DBA', how='left')  # how='left' keeps all rows from df2

        merged_df.dropna(subset=['SCORE'], inplace=True) # drop rows with no inspection score        
        # merge on A, B, C
        
        grade_order = ['A', 'B', 'C']
        
        merged_df['GRADE'] = pd.Categorical(merged_df['GRADE'], categories=grade_order, ordered=True)
        
        # sort
        merged_df.sort_values(by=['GRADE', 'SCORE'], ascending=[False, False], na_position='last', inplace=True)
        
        merged_df.drop_duplicates(subset='name', keep='first', inplace=True) # de duplicate
        # Select the desired columns
        final_columns = ['id', 'name', 'rating', 'review_count', 'categories_list', 'BORO', 'SCORE', 'GRADE']
        merged_df = merged_df[final_columns]




        # Write the merged data to a new CSV
        merged_df.to_csv(output_path, index=False)
        print(f"Merged restaurant data saved to {output_path}")

    except FileNotFoundError:
        print(f"Error: One or both input files not found.")
    except KeyError as e:
        print(f"Error: Column '{e}' not found in one of the input files. Check headers.")
    except Exception as e:
        print(f"An error occurred during merging: {e}")


# Example usage:
CSV1_PATH = "outputs/cleaned_restaurants.csv"  # Replace with path to the first CSV
CSV2_PATH = "outputs/nyc_borough_cuisines.csv"  # Replace with path to the second CSV
OUTPUT_PATH = "outputs/merged_restaurant_data.csv"  # Replace with desired output path


merge_restaurant_data(CSV1_PATH, CSV2_PATH, OUTPUT_PATH)