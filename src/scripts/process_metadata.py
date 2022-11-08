import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--refresh", help="refresh all experiment metadata",
                    action="store_true")
args = parser.parse_args()

# FILTER EXISTING entities

# excluded datasets and existing entities
excluded_datasets_df = pd.read_csv('tmp/excluded_datasets.tsv', sep='\t')
excluded_datasets = list(excluded_datasets_df['id'])
existing_entities = []
if not args.refresh:
    with open('tmp/existing_entities.txt', 'r') as file:
        for line in file:
            existing_entities.append("FlyBase:" + line.rstrip())


def filter_and_format(data_type, data, exclusion_list, existing_list):
    """
    Remove excluded and existing (if not 'refresh'-ing) entities and reformat FB IDs.
    Also returns list of entities with an 'associated_dataset' on the exclusion list
    data is a DataFrame with an 'id' column and optional 'associated_dataset' column.
    exclusion_list and existing_list are lists.
    """
    ignore_list = set(exclusion_list + existing_list)
    data = data[~data['id'].isin(ignore_list)]
    new_exclusions = []
    if 'associated_dataset' in data.columns:
        new_exclusions = list(data[data['associated_dataset'].isin(exclusion_list)]['id'])
        data = data[~data['associated_dataset'].isin(exclusion_list)]
        data['associated_dataset'] = data['associated_dataset'].map(lambda x: x.replace("FlyBase:", "http://flybase.org/reports/"))
    if 'publication' in data.columns:
        data['publication'] = data['publication'].map(lambda x: x.replace("FlyBase:", "http://flybase.org/reports/"))
        
    if data_type == 'dataset':
        data['neo_label'] = "scRNAseq_DataSet"
        data['licence'] = "http://virtualflybrain.org/reports/VFBlicense_CC_BY_4_0"
        publication_data = pd.DataFrame({"@type":"Publication", "id":data["publication"].unique()})
        publication_data.to_csv('tmp/publication_data.tsv', sep='\t', index=False)
    elif data_type == 'cluster':
        data['neo_label'] = "Cluster"
    elif data_type == 'sample':
        data['neo_label'] = "Sample"
        
    data.to_csv('tmp/%s_data.tsv' % data_type, sep='\t', index=False)
    
    new_exclusions = set(new_exclusions)
    return new_exclusions


dataset_data = pd.read_csv('tmp/raw_dataset_data.tsv', sep='\t')
filter_and_format('dataset', dataset_data, excluded_datasets, existing_entities)
sample_data = pd.read_csv('tmp/raw_sample_data.tsv', sep='\t')
filter_and_format('sample', sample_data, excluded_datasets, existing_entities)
clustering_data = pd.read_csv('tmp/raw_clustering_data.tsv', sep='\t')
filter_and_format('clustering', clustering_data, excluded_datasets, existing_entities)
cluster_data = pd.read_csv('tmp/raw_cluster_data.tsv', sep='\t')
excluded_clusters = filter_and_format('cluster', cluster_data, excluded_datasets, existing_entities)

with open('tmp/excluded_clusters.txt', 'w') as file:
    for c in excluded_clusters:
        file.write(c + '\n')

