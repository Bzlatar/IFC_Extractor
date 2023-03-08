import os.path
import csv


# Create a list of dictionaries with the information of each element
def ifc_extractor(file_name, ifc_file):
    # Get all the elements in the file (on a list)
    elements = ifc_file.by_type('IfcProduct')

    # Get the properties of the file
    single_values = ifc_file.by_type("IfcPropertySingleValue")
    file_properties = {}
    for sv in single_values:
        file_properties[sv.Name] = sv.NominalValue.wrappedValue

    # Create a list to store file information
    file_output = []

    # List with elements and materials we don't want
    no_elements = ['IfcSite', 'IfcBuilding']
    # Iterate through all the elements in the file
    for el in elements:

        # Get dict with element info and type of element
        element_dict = el.get_info()
        element_type = element_dict.get('type')

        # Filter elements we dont want
        if element_type not in no_elements:

            # Get all property sets associated with the element
            property_sets = el.IsDefinedBy
            property_sets = [ps.RelatingPropertyDefinition for ps in property_sets if
                             hasattr(ps, "RelatingPropertyDefinition")]

            # Create a dictionary to store property values
            element_properties = {}
            # Loop through each set in the element
            for prop_set in property_sets:
                # Get all properties in the set
                props = prop_set.HasProperties
                # Loop through each property in the set
                for prop in props:
                    # Get the name and value of the property
                    prop_name = prop.Name
                    prop_value = prop.NominalValue.wrappedValue
                    # Store the value in the dictionary
                    element_properties[prop_name] = prop_value

            # Check if the properties dictionary is empty (if it is empty is not a element of interest)
            # if element_properties: (NOT IN USE)

            # Create dict to populate with info
            element_output = {
                'Source File': file_name,
                'GLOBALID': element_dict.get('GlobalId'),
                "TfNSW_ProjectAndContractName": file_properties.get('TfNSW_ProjectAndContractName'),
                "tbProjectContractCode": file_properties.get('tbProjectContractCode'),
                "tbAEOSuppCode": file_properties.get('tbAEOSuppCode'),
                "tbAEOSuppName": file_properties.get('tbAEOSuppName'),
                "tbDesignCompCode": file_properties.get('tbDesignCompCode'),
                "tbDesignCompName": file_properties.get('tbDesignCompName'),
                "tbCoordSys": file_properties.get('tbCoordSys'),
                "TfNSW_ProjectMilestoneDesc": file_properties.get('TfNSW_ProjectMilestoneDesc'),
                "TfNSW_StateDesc": file_properties.get('TfNSW_StateDesc'),
                "TfNSW_SuitabilityDesc": file_properties.get('TfNSW_SuitabilityDesc'),
                "TfNSW_DocumentNo": file_properties.get('TfNSW_DocumentNo'),
                "TfNSW_DocumentTitle": file_properties.get('TfNSW_DocumentTitle'),
                "tbAEODisciplineCode": file_properties.get('tbAEODisciplineCode'),
                "tbAEOSubDiscCode": file_properties.get('tbAEOSubDiscCode'),
                "TfNSW_AssetLocationID": element_properties.get('TfNSW_AssetLocationID'),
                "TfNSW_ParentAssetLocationID": element_properties.get('TfNSW_ParentAssetLocationID'),
                "TfNSW_ProjectAssetLocationID": element_properties.get('TfNSW_ProjectAssetLocationID'),
                "TfNSW_ParentProjectAssetLocationID": element_properties.get('TfNSW_ParentProjectAssetLocationID'),
                "TfNSW_AssetLocationCode": element_properties.get('TfNSW_AssetLocationCode'),
                "TfNSW_ParentAssetLocationCode": element_properties.get('TfNSW_ParentAssetLocationCode'),
                "TfNSW_AssetLocationDesc": element_properties.get('TfNSW_AssetLocationDesc'),
                "TfNSW_UniclassAssetLocationCode": element_properties.get('TfNSW_UniclassAssetLocationCode'),
                "TfNSW_UniclassAssetLocationTitle": element_properties.get('TfNSW_UniclassAssetLocationTitle'),
                "TfNSW_WorkZoneName": element_properties.get('TfNSW_WorkZoneName'),
                "TfNSW_WorkZoneCode": element_properties.get('TfNSW_WorkZoneCode'),
                "Uniclass_CoCode": element_properties.get('Uniclass_CoCode'),
                "Uniclass_CoTitle": element_properties.get('Uniclass_CoTitle'),
                "Uniclass_EnCode": element_properties.get('Uniclass_EnCode'),
                "Uniclass_EnTitle": element_properties.get('Uniclass_EnTitle'),
                "Uniclass_SLCode": element_properties.get('Uniclass_SLCode'),
                "Uniclass_SLTitle": element_properties.get('Uniclass_SLTitle'),
                "TfNSW_AssetID": element_properties.get('TfNSW_AssetID'),
                "TfNSW_ProjectAssetID": element_properties.get('TfNSW_ProjectAssetID'),
                "TfNSW_ParentAssetID": element_properties.get('TfNSW_ParentAssetID'),
                "TfNSW_ParentProjectAssetID": element_properties.get('TfNSW_ParentProjectAssetID'),
                "TfNSW_AssetDataStandard": element_properties.get('TfNSW_AssetDataStandard'),
                "TfNSW_AssetTypeCode": element_properties.get('TfNSW_AssetTypeCode'),
                "TfNSW_AssetInstance": element_properties.get('TfNSW_AssetInstance'),
                "TfNSW_AssetCode": element_properties.get('TfNSW_AssetCode'),
                "TfNSW_ParentAssetCode": element_properties.get('TfNSW_ParentAssetCode'),
                "TfNSW_AssetDescription": element_properties.get('TfNSW_AssetDescription'),
                "TfNSW_AssetLabel": element_properties.get('TfNSW_AssetLabel'),
                "TfNSW_UniclassAssetCode": element_properties.get('TfNSW_UniclassAssetCode'),
                "TfNSW_UniclassAssetTitle": element_properties.get('TfNSW_UniclassAssetTitle'),
                "TfNSW_AssetTypeConfigCode": element_properties.get('TfNSW_AssetTypeConfigCode'),
                "TfNSW_AssetTypeConfigDesc": element_properties.get('TfNSW_AssetTypeConfigDesc'),
                "TfNSW_DisciplineCode": element_properties.get('TfNSW_DisciplineCode'),
                "TfNSW_SubDisciplineCode": element_properties.get('TfNSW_SubDisciplineCode'),
                "TfNSW_WPDesignCode": element_properties.get('TfNSW_WPDesignCode'),
                "TfNSW_WPSupplyCode": element_properties.get('TfNSW_WPSupplyCode'),
                "TfNSW_WPConstructionCode": element_properties.get('TfNSW_WPConstructionCode'),
                "TfNSW_WPCommissioningCode": element_properties.get('TfNSW_WPCommissioningCode'),
                "TfNSW_AssetStatusCode": element_properties.get('TfNSW_AssetStatusCode'),
                "TfNSW_AssetOwnerOrgName": element_properties.get('TfNSW_AssetOwnerOrgName'),
                "TfNSW_AssetOperatorOrgName": element_properties.get('TfNSW_AssetOperatorOrgName'),
                "TfNSW_AssetMaintainerOrgName": element_properties.get('TfNSW_AssetMaintainerOrgName'),
                "TfNSW_StartKm": element_properties.get('TfNSW_StartKm'),
                "TfNSW_EndKm": element_properties.get('TfNSW_EndKm'),
                "TfNSW_GPSCoordinates": element_properties.get('TfNSW_GPSCoordinates'),
                "Uniclass_EFCode": element_properties.get('Uniclass_EFCode'),
                "Uniclass_EFTitle": element_properties.get('Uniclass_EFTitle'),
                "Uniclass_SsCode": element_properties.get('Uniclass_SsCode'),
                "Uniclass_SsTitle": element_properties.get('Uniclass_SsTitle'),
                "Uniclass_PrCode": element_properties.get('Uniclass_PrCode'),
                "Uniclass_PrTitle": element_properties.get('Uniclass_PrTitle')
            }
            file_output.append(element_output)

    return file_output


# Create CSV Asset file from the list of dictionaries from the extractor
def csv_asset(file_name, file_output):
    # CSV file name
    new_name = file_name.replace('.ifc', '_Asset.csv')
    csv_name = os.path.join('Output', new_name)
    headers = list(file_output[0].keys())

    # Open the CSV file in write mode
    with open(csv_name, mode='w', newline='') as file:
        # Create a CSV writer object
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write the headers to the CSV file
        writer.writeheader()

        # Write the rows to the CSV file
        for row in file_output:
            writer.writerow(row)


# Create CSV Project file
def csv_project(file_name, ifc_file):
    # Get all the elements in the file (on a list)
    single_values = ifc_file.by_type('IfcPropertySingleValue')

    # Loop through each property and creates dictionary with info
    project_values = {}
    for sv in single_values:
        project_values[sv.Name] = sv.NominalValue.wrappedValue

    # Create dict to populate with info
    project_output = {
        'Source File': file_name,
        'GLOBALID': project_values.get('GlobalId'),
        "TfNSW_ProjectAndContractName": project_values.get('TfNSW_ProjectAndContractName'),
        "tbProjectContractCode": project_values.get('tbProjectContractCode'),
        "tbAEOSuppCode": project_values.get('tbAEOSuppCode'),
        "tbAEOSuppName": project_values.get('tbAEOSuppName'),
        "tbDesignCompCode": project_values.get('tbDesignCompCode'),
        "tbDesignCompName": project_values.get('tbDesignCompName'),
        "tbCoordSys": project_values.get('tbCoordSys'),
        "TfNSW_ProjectMilestoneDesc": project_values.get('TfNSW_ProjectMilestoneDesc'),
        "TfNSW_StateDesc": project_values.get('TfNSW_StateDesc'),
        "TfNSW_SuitabilityDesc": project_values.get('TfNSW_SuitabilityDesc'),
        "TfNSW_DocumentNo": project_values.get('TfNSW_DocumentNo'),
        "TfNSW_DocumentTitle": project_values.get('TfNSW_DocumentTitle'),
        "tbAEODisciplineCode": project_values.get('tbAEODisciplineCode'),
        "tbAEOSubDiscCode": project_values.get('tbAEOSubDiscCode')
    }
    # CSV file name
    new_name = file_name.replace('.ifc', '_Project.csv')
    csv_name = os.path.join('Output', new_name)
    headers = list(project_output.keys())

    # Open the CSV file in write mode
    with open(csv_name, mode='w', newline='') as file:
        # Create a CSV writer object
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write the headers to the CSV file
        writer.writeheader()
        writer.writerow(project_output)
