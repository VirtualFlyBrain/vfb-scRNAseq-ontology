import pandas as pd

expression_cutoff = 0.5

# remove excluded datasets
cluster_data = pd.read_csv('tmp/raw_cluster_data.tsv', sep='\t')
sample_data = pd.read_csv('tmp/raw_sample_data.tsv', sep='\t')
dataset_data = pd.read_csv('tmp/raw_dataset_data.tsv', sep='\t')
excluded_datasets = pd.read_csv('excluded_datasets.tsv', sep='\t')
excluded_clusters = list(cluster_data[cluster_data['associated_dataset'].isin(excluded_datasets['id'])]['id'])

cluster_data = cluster_data[~cluster_data['associated_dataset'].isin(excluded_datasets['id'])]
cluster_data.to_csv('tmp/cluster_data.tsv', sep='\t', index=False)
sample_data = sample_data[~sample_data['associated_dataset'].isin(excluded_datasets['id'])]
sample_data.to_csv('tmp/sample_data.tsv', sep='\t', index=False)
dataset_data = dataset_data[~dataset_data['id'].isin(excluded_datasets['id'])]
dataset_data.to_csv('tmp/dataset_data.tsv', sep='\t', index=False)

# add existing clusters (ofn already exists) to exclusion list
existing_clusters = []
with open('tmp/existing_clusters.txt', 'r') as file:
    for line in file:
        existing_clusters.append("FlyBase:" + line.rstrip())
excluded_clusters.extend(existing_clusters)

# get headers from expression_data file
expression_data = pd.read_csv("tmp/raw_expression_data.tsv", sep='\t', nrows=0)

# read expression_data in chunksize
expression_reader = pd.read_csv("tmp/raw_expression_data.tsv", sep='\t', dtype={'@type': 'category', 'id': 'category', 'gene': 'category'}, chunksize=1000)

# filter each chunk and concatenate
for chunk in expression_reader:
    filtered = chunk[(chunk['expression_extent']>expression_cutoff) & (~chunk['id'].isin(excluded_clusters))]
    expression_data = pd.concat([expression_data, filtered])

# make a a tsv for each new cluster
clusters = expression_data['id'].unique()
for c in clusters:
    cluster_data = expression_data[expression_data['id']==c]
    cluster_id = c.replace("FlyBase:", "")
    cluster_data.to_csv("expression_data/%s.tsv" % cluster_id, sep='\t', index=False)
