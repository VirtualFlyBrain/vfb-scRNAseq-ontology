import pandas as pd
from  get_external_terms import get_unique_terms_from_col

# read data files
cluster_data = pd.read_csv('tmp/raw_cluster_data.tsv', sep='\t')
dataset_data = pd.read_csv('tmp/raw_dataset_data.tsv', sep='\t')
sample_data = pd.read_csv('tmp/raw_sample_data.tsv', sep='\t')
assay_data = pd.read_csv('tmp/raw_assay_data.tsv', sep='\t')
clustering_data = pd.read_csv('tmp/raw_clustering_data.tsv', sep='\t')

outfile = "tmp/FBlc_terms.txt"

# grab unique values from columns containing terms from external ontologies
# these all seem to come as curies, but I think iri v curie doesn't matter for robot
ID_columns = [
sample_data['id'],
dataset_data['id'],
cluster_data['id'],
clustering_data['id'],
assay_data['id']]

all_ids = []
for c in ID_columns:
    all_ids.extend(get_unique_terms_from_col(c))

all_ids = set([i.replace('FlyBase:','http://flybase.org/reports/') for i in all_ids])

with open(outfile, 'w') as file:
    file.write('\n'.join(all_ids) + '\n')
