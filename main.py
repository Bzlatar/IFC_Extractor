import ifcopenshell
import os
import glob
from functions import ifc_extractor, csv_asset, csv_project

# Get folder path
folder_path = 'C:/Users/BlasZlatar/Documents/Python Scripts/IFC Extractor/Input/'
path_list = glob.glob(os.path.join(folder_path, '*.ifc*'))

# Loop all files in the input folder
for file_path in path_list:

    # In case of an error
    try:
        # Get file name
        file_name = os.path.basename(file_path)
        print("File:", file_name)

        # Open IFC file
        ifc_file = ifcopenshell.open(file_path)

        # Create CSV Project file using csv_project function
        csv_project(file_name, ifc_file)
        print("CSV Project file created")

        # Create a list of dictionaries with the information of each element in the file using ifc_extractor function
        file_output = ifc_extractor(file_name, ifc_file)

        # Create CSV Asset file from the list of dictionaries from the extractor using csv_asset function
        csv_asset(file_name, file_output)
        print("CSV Asset file created")

        # Print the number of elements in the file
        n_elements = len(file_output)
        print("Number of elements in file:", n_elements, '\n')

    # In case of an error goes to next loop
    except (IndexError, TypeError, AttributeError) as e:
        print(f"Caught {type(e).__name__}: {e}", '\n')
        continue
