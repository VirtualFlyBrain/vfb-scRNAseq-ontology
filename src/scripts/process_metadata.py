import pandas as pd
import argparse
from filter_data import DataEntity

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
dataset_data.filtered_df = (dataset_data.filtered_df.groupby(['id', 'name', 'title', 'publication', 'licence', 'assay_type', 'site']).agg({'accession': lambda x: "|".join(x)}).reset_index())

# make publication df
publication_data = DataEntity(datatype='pub')
publication_data.filtered_df = pd.DataFrame({"id":dataset_data.filtered_df["publication"], "pub_dataset":dataset_data.filtered_df["id"]})

# neo labels (not for Clustering)
for d in [dataset_data, cluster_data, assay_data, sample_data, publication_data]:
    d.filtered_df['neo_label'] = d.datatype


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
