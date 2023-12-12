import os
from bs4 import BeautifulSoup

upper_catalog_file = "catalog-v001.xml"
lower_catalog_file = "ontology_files/catalog-v001.xml"

# dataset metadata ontologies must already be in ontology_files
all_included_datasets = [filename.split('_')[2].replace('.owl', '')  for filename in os.listdir("ontology_files") if filename.endswith('.owl')]

with open(upper_catalog_file, 'r') as file1:
    upper_catalog = BeautifulSoup(file1, 'xml')
with open(lower_catalog_file, 'r') as file2:
    lower_catalog = BeautifulSoup(file2, 'xml')

     # Check if the metadata ontology import already exists in upper_catalog
    meta_check_upper = upper_catalog.find('uri', {"name": f"http://virtualflybrain.org/data/VFB/OWL/VFB_scRNAseq_{id}.owl"})

    if not meta_check_upper:
        # Update upper_catalog only if the tag doesn't exist
        upper_catalog.catalog.group.append(
            upper_catalog.new_tag('uri', attrs={
                "id":"User Entered Import Resolution",
                "name": f"http://virtualflybrain.org/data/VFB/OWL/VFB_scRNAseq_{id}.owl",
                "uri" : f"ontology_files/VFB_scRNAseq_{id}.owl"}))

    # Check if the expression import already exists in upper_catalog
    exp_check_upper = upper_catalog.find('uri', {"name": f"http://purl.obolibrary.org/obo/VFB_scRNAseq/expression_data/dataset_{id}.owl"})

    if not exp_check_upper:
        # Update upper_catalog only if the tag doesn't exist
        upper_catalog.catalog.group.append(
            upper_catalog.new_tag('uri', attrs={
                "id":"User Entered Import Resolution",
                "name": f"http://purl.obolibrary.org/obo/VFB_scRNAseq/expression_data/dataset_{id}.owl",
                "uri" : f"expression_data/dataset_{id}.owl"}))

    # Check if the expression import already exists in lower_catalog
    exp_check_lower = lower_catalog.find('uri', {"name": f"http://purl.obolibrary.org/obo/VFB_scRNAseq/expression_data/dataset_{id}.owl"})

    if not exp_check_lower:
        # Update lower_catalog only if the tag doesn't exist
        lower_catalog.catalog.group.append(
            lower_catalog.new_tag('uri', attrs={
                "id":"User Entered Import Resolution",
                "name": f"http://purl.obolibrary.org/obo/VFB_scRNAseq/expression_data/dataset_{id}.owl",
                "uri" : f"../expression_data/dataset_{id}.owl"}))

    # Check if the external terms import already exists in lower_catalog
    ext_check_lower = lower_catalog.find('uri', {"name": f"http://purl.obolibrary.org/obo/VFB_scRNAseq/imports/{id}_import.owl"})

    if not ext_check_lower:
        # Update lower_catalog only if the tag doesn't exist
        lower_catalog.catalog.group.append(
            lower_catalog.new_tag('uri', attrs={
                "id":"User Entered Import Resolution",
                "name": f"http://purl.obolibrary.org/obo/VFB_scRNAseq/imports/{id}_import.owl",
                "uri" : f"../imports/{id}_import.owl"}))

with open(upper_catalog_file, 'w') as file1:
    file1.write(upper_catalog.prettify())
with open(lower_catalog_file, 'w') as file2:
    file2.write(lower_catalog.prettify())
