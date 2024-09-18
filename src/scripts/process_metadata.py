import pandas as pd
import dask
import dask.dataframe as dd
pd.set_option('display.max_columns',100)
import argparse
from filter_data import DataEntity
from process_expression_data import expression_file_loader

expression_cutoff = 0.2

# new sites must be added to VFB KB, then add FB name and VFB short form here:
sites_dict= {'EMBL-EBI Single Cell Expression Atlas Datasets': 'scExpressionAtlas'}

# can specify whether to regenerate tsvs for all existing datasets. New datasets will always be generated.
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--refresh", help="refresh all existing metadata",
                    action="store_true")
args = parser.parse_args()

# excluded remove existing entities if required
existing_entities = []
if not args.refresh:
    with open('tmp/internal_terms.txt', 'r') as file:
        for line in file:
            existing_entities.append("FlyBase:" + line.rstrip())

with open ('tmp/all_inclusions.txt', 'r') as file:
    all_included_entities = file.read().splitlines()

all_inclusions_to_process = [i for i in all_included_entities if not (i in existing_entities)]


## load filtered data
assay_data = DataEntity(datatype='Assay')
sample_data = DataEntity(datatype='Sample')
dataset_data = DataEntity(datatype='DataSet')
clustering_data = DataEntity(datatype='Clustering')
cluster_data = DataEntity(datatype='Cluster')


## keep only rows where id in all_inclusions_to_process
for d in [dataset_data, cluster_data, clustering_data, assay_data, sample_data]:
    d.filtered_df = d.filtered_df[d.filtered_df['id'].isin(all_inclusions_to_process)]

datasets_to_process = dataset_data.filtered_df['id'].drop_duplicates()


## formatting steps

# extra processing for DataSet
dataset_data.filtered_df['licence'] = "http://virtualflybrain.org/reports/VFBlicense_CC_BY_4_0"
dataset_data.filtered_df['site'] = dataset_data.filtered_df['site_label'].apply(lambda x: "vfb:" + sites_dict[x])
dataset_data.filtered_df = dataset_data.filtered_df.drop(['source_linkout', 'site_label'], axis=1).drop_duplicates()

# make publication df
publication_data = DataEntity(datatype='pub')
publication_data.filtered_df = pd.DataFrame({"id":dataset_data.filtered_df["publication"], "pub_dataset":dataset_data.filtered_df["id"]})

# neo labels (not for Clustering)
for d in [dataset_data, cluster_data, assay_data, sample_data, publication_data]:
    d.filtered_df['neo_label'] = d.datatype

# get numbers of genes in each cluster and dataset
def get_gene_counts(input_dataframe, cutoff):
    """Needs id as index and columns ['gene', 'expression_extent'] (at least).
       Output has id as index and columns = ['all_gene_counts', 'filtered_gene_counts']"""
    unfiltered_genes = input_dataframe.loc[:,['gene']]
    filtered_genes = input_dataframe.loc[input_dataframe['expression_extent'] > cutoff,['gene']]
    all_gene_counts = unfiltered_genes.index.value_counts().to_frame(name='all_gene_counts')
    filtered_gene_counts = filtered_genes.index.value_counts().to_frame(name='filtered_gene_counts')
    gene_counts = all_gene_counts.join(filtered_gene_counts, how='outer').compute()
    return gene_counts

# clusters
cluster_ids = cluster_data.filtered_df['id'].drop_duplicates().to_list()
exp_data = expression_file_loader(cluster_ids, 0)

cluster_gene_counts = get_gene_counts(exp_data, expression_cutoff)
cluster_data.filtered_df = cluster_data.filtered_df.merge(cluster_gene_counts, how='left', right_index=True, left_on='id')

# datasets
exp_data = exp_data.merge(cluster_data.filtered_df[['id', 'associated_dataset']], how='left', left_index=True, right_on='id')
exp_data = exp_data.set_index('associated_dataset')

dataset_gene_counts = get_gene_counts(exp_data, expression_cutoff)
dataset_data.filtered_df = dataset_data.filtered_df.merge(dataset_gene_counts, how='left', right_index=True, left_on='id')

# if a cluster or dataset has no genes after filtering, drop it (not actually expected to happen)
cluster_data.filtered_df = cluster_data.filtered_df[cluster_data.filtered_df['filtered_gene_counts'].notnull()]
dataset_data.filtered_df = dataset_data.filtered_df[dataset_data.filtered_df['filtered_gene_counts'].notnull()]


## spilt data and make new tsvs
for d in [cluster_data, clustering_data, assay_data, sample_data]:
    new_entites = d.split_filtered_df(datasets = datasets_to_process, split_by_col = 'associated_dataset')
    for e in new_entites:
        e.write_tsv_by_dataset()

new_datasets = dataset_data.split_filtered_df(datasets = datasets_to_process, split_by_col = 'id')
for e in new_datasets:
    e.write_tsv_by_dataset()

new_pubs = publication_data.split_filtered_df(datasets = datasets_to_process, split_by_col = 'pub_dataset')
for e in new_pubs:
    e.write_tsv_by_dataset()
