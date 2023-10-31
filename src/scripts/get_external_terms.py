import pandas as pd

# read data files
cluster_data = pd.read_csv('tmp/raw_cluster_data.tsv', sep='\t')
dataset_data = pd.read_csv('tmp/raw_dataset_data.tsv', sep='\t')
sample_data = pd.read_csv('tmp/raw_sample_data.tsv', sep='\t')
assay_data = pd.read_csv('tmp/raw_assay_data.tsv', sep='\t')

outfile = "imports/external_terms.txt"

def get_unique_terms_from_col(column):
    """Input is a pandas dataframe column, output is a unique list of values (excluding nulls)."""
    return list(column.dropna().unique())

# grab unique values from columns containing terms from external ontologies
# these all seem to come as curies, but I think iri v curie doesn't matter for robot
external_term_columns = [
sample_data['sample_tissue'],
sample_data['stage'],
dataset_data['assay_type'],
cluster_data['stage'],
cluster_data['cell_type'],
assay_data['method']]

all_external_terms = []
for c in external_term_columns:
    all_external_terms.extend(get_unique_terms_from_col(c))

all_external_terms = set(all_external_terms)

with open(outfile, 'w') as file:
    file.write('\n'.join(all_external_terms))
