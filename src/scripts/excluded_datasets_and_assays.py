import pandas as pd
from vfb_connect.neo.neo4j_tools import Neo4jConnect, dict_cursor

# read data files
cluster_data = pd.read_csv('tmp/raw_cluster_data.tsv', sep='\t')
dataset_data = pd.read_csv('tmp/raw_dataset_data.tsv', sep='\t')
sample_data = pd.read_csv('tmp/raw_sample_data.tsv', sep='\t')
assay_data = pd.read_csv('tmp/raw_assay_data.tsv', sep='\t')

# Manual exclusions - add IDs of datasets to exclude in format "FlyBase:FBlc0000000": "FlyBase:FBlc0005362"
manual_exclusions = []
manually_excluded_datasets = dataset_data[dataset_data['id'].isin(manual_exclusions)][['id', 'name']]

# get :Nervous_system FBbt IDs from VFB
nc = Neo4jConnect('http://pdb.virtualflybrain.org', 'vfb', 'neo4j')
query = "MATCH (c:Class:Nervous_system) WHERE c.short_form STARTS WITH \"FBbt\" RETURN DISTINCT c.short_form AS FBbt_ID"
q = nc.commit_list([query])
FBbt_IDs = pd.DataFrame(dict_cursor(q))
FBbt_IDs = list(FBbt_IDs['FBbt_ID'].apply(lambda x: x.replace('_', ':')))

# check which datasets not linked to :Nervous_system FBbt terms
included_cluster_data = cluster_data[cluster_data['cell_type'].isin(FBbt_IDs)]
non_neuronal_datasets = dataset_data[~dataset_data['id'].isin(included_cluster_data['associated_dataset'])][['id', 'name']].drop_duplicates()

# assays to exclude based on relationship to a control assay by biological_reference_is
excluded_assays = assay_data[assay_data['control_assay'].notnull()][['id', 'name']].drop_duplicates()

# exclude datasets that would have no other assays after removing excluded assays
exc_dataset_list = []
for d in dataset_data['id'].unique().tolist():
    if len(assay_data[(assay_data['associated_dataset']==d) & (~assay_data['id'].isin(excluded_assays['id']))]) == 0:
        exc_dataset_list.append(d)

experimental_condition_datasets = dataset_data[dataset_data['id'].isin(exc_dataset_list)][['id', 'name']]

all_exclusions = pd.concat([manually_excluded_datasets, non_neuronal_datasets, excluded_assays, experimental_condition_datasets], axis=0).drop_duplicates()

included_datasets = [i for i in dataset_data['id'].tolist() if not (i in all_exclusions['id'].tolist())]

all_exclusions.to_csv("tmp/excluded_datasets_and_assays.tsv", sep='\t', index=None)

with open('tmp/included_dataset_list.txt', 'w') as f:
    f.write('\n'.join(included_datasets))
