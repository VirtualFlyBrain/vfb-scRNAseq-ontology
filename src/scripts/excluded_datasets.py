import pandas as pd
from vfb_connect.neo.neo4j_tools import Neo4jConnect, dict_cursor

# Manual exclusions - add IDs of Datasets to exclude in format "FlyBase:FBlc0000000":
manual_exclusions = ["FlyBase:FBlc0005362"]

# get :Nervous_system FBbt IDs from VFB
nc = Neo4jConnect('http://pdb.virtualflybrain.org', 'vfb', 'neo4j')
query = "MATCH (c:Class:Nervous_system) WHERE c.short_form STARTS WITH \"FBbt\" RETURN DISTINCT c.short_form AS FBbt_ID"
q = nc.commit_list([query])
FBbt_IDs = pd.DataFrame(dict_cursor(q))
FBbt_IDs = list(FBbt_IDs['FBbt_ID'].apply(lambda x: x.replace('_', ':')))

# check which datasets not linked to :Nervous_system FBbt terms
cluster_data = pd.read_csv('tmp/raw_cluster_data.tsv', sep='\t')
dataset_data = pd.read_csv('tmp/raw_dataset_data.tsv', sep='\t')

included_cluster_data = cluster_data[cluster_data['cell_type'].isin(FBbt_IDs)]
excluded_datasets = dataset_data[~dataset_data['id'].isin(included_cluster_data['associated_dataset'])][['id', 'name']].drop_duplicates()

# add manual exclusions
if manual_exclusions:
    manually_excluded_datasets = dataset_data[dataset_data['id'].isin(manual_exclusions)][['id', 'name']]
    print(manually_excluded_datasets)
    excluded_datasets = pd.concat([excluded_datasets, manually_excluded_datasets], axis=0).drop_duplicates()
    print(excluded_datasets)

excluded_datasets.to_csv("tmp/excluded_datasets.tsv", sep='\t')
