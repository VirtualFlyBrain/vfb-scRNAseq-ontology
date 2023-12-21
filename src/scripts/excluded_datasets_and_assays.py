import pandas as pd
from vfb_connect.neo.neo4j_tools import Neo4jConnect, dict_cursor


## input and output
class DataEntity:
    name = ''
    input_file = ''
    output_file = ''
    dataframe = None
    def __init__(self, name):
        self.name = name
        self.input_file = 'tmp/raw_%s_data.tsv' % self.name
        self.output_file = 'tmp/filtered_%s_data.tsv' % self.name
        self.dataframe = pd.read_csv(self.input_file, sep='\t')
    def write_tsv(self):
        self.dataframe.to_csv(self.output_file, sep='\t', index=None)
    def filter_by_other(self, owncol, other, othercol):
        """Keep only rows of self.dataframe where owncol (column name) value appears in other.dataframe[othercol]"""
        self.dataframe = self.dataframe[self.dataframe[owncol].isin(other.dataframe[othercol].drop_duplicates())]

assay_data = DataEntity(name='assay')
sample_data = DataEntity(name='sample')
dataset_data = DataEntity(name='dataset')
clustering_data = DataEntity(name='clustering')
cluster_data = DataEntity(name='cluster')


## Manual exclusions - add IDs of datasets to exclude in format "FlyBase:FBlc0000000"
manual_exclusions = []
dataset_data.dataframe = dataset_data.dataframe[~dataset_data.dataframe['id'].isin(manual_exclusions)]


## link assays and samples to the same dataset as any clusterings they appear in
# (this may mean they end up linked to > 1 dataset)
def update_dataset_from_clustering(input_df):
    updated_entity_df_list = []
    for a in input_df['id'].drop_duplicates():
        single_entity_data = input_df[input_df['id']==a]
        clustering_datasets = clustering_data.dataframe[clustering_data.dataframe['associated_sample_or_assay_for_clustering']==a]['associated_dataset'].drop_duplicates()
        updated_dataset_df_list = []
        for ds in clustering_datasets:
            updated_dataset = single_entity_data
            updated_dataset['associated_dataset']=ds
            updated_dataset_df_list.append(updated_dataset)
        updated_entity_df_list.append(pd.concat(updated_dataset_df_list))
    return pd.concat(updated_entity_df_list)

assay_data.dataframe = update_dataset_from_clustering(assay_data.dataframe)
sample_data.dataframe = update_dataset_from_clustering(sample_data.dataframe)


## filter for nervous system term-containing clusters
# get :Nervous_system FBbt IDs from VFB
nc = Neo4jConnect('http://pdb.virtualflybrain.org', 'vfb', 'neo4j')
query = "MATCH (c:Class:Nervous_system) WHERE c.short_form STARTS WITH \"FBbt\" RETURN DISTINCT c.short_form AS FBbt_ID"
q = nc.commit_list([query])
FBbt_IDs = pd.DataFrame(dict_cursor(q))
FBbt_IDs = list(FBbt_IDs['FBbt_ID'].apply(lambda x: x.replace('_', ':')))

# check which clusters are linked to :Nervous_system FBbt terms
ns_cluster_data = cluster_data.dataframe[cluster_data.dataframe['cell_type'].isin(FBbt_IDs)]
# find datasets that are associated with nervous system clusters
ns_datasets = ns_cluster_data['associated_dataset'].drop_duplicates()
# filter datasets
dataset_data.dataframe = dataset_data.dataframe[dataset_data.dataframe['id'].isin(ns_datasets)]

# keep only assay, sample, cluster and clustering rows that are associated with a kept dataset
for d in [cluster_data, clustering_data, assay_data, sample_data]:
    d.filter_by_other(owncol='associated_dataset', other = dataset_data, othercol = 'id')


## filtering based on experimental condition assays
# assay ids to exclude based on relationship to a control assay by biological_reference_is
excluded_assays = assay_data.dataframe[assay_data.dataframe['control_assay'].notnull()]['id'].drop_duplicates()
# drop any clusterings that use an excluded assay
excluded_clusters = clustering_data.dataframe[clustering_data.dataframe['associated_sample_or_assay_for_clustering'].isin(excluded_assays)]['id'].drop_duplicates()
clustering_data.dataframe = clustering_data.dataframe[~clustering_data.dataframe['id'].isin(excluded_clusters)]

# no longer need control_assay column
assay_data.dataframe.drop('control_assay', axis=1, inplace=True)

# keep only assay and sample rows that are associated with a kept clustering
for d in [assay_data, sample_data]:
    d.filter_by_other(owncol='id', other = clustering_data, othercol = 'associated_sample_or_assay_for_clustering')

# keep only dataset rows that are associated with a kept clustering
dataset_data.filter_by_other(owncol='id', other = clustering_data, othercol = 'associated_dataset')

# keep only cluster rows that are associated with a kept clustering
cluster_data.filter_by_other(owncol='associated_clustering', other = clustering_data, othercol = 'id')


## output
# filtered dataframes
for d in [dataset_data, cluster_data, clustering_data, assay_data, sample_data]:
    d.write_tsv()

# make a list of (all) inclusions (for process_metadata and process_expression_data)
# this is different to internal_terms.txt, which is all entities currently incorporated into ontologies
all_inclusions = []
for d in [dataset_data, cluster_data, clustering_data, assay_data, sample_data]:
    all_inclusions.extend(d.dataframe['id'].drop_duplicates().to_list())

with open('tmp/all_inclusions.txt', 'w') as f:
    f.write('\n'.join(all_inclusions))
