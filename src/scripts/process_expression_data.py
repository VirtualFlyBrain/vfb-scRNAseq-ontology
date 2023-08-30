import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--refresh", help="refresh all experiment metadata",
                    action="store_true")
args = parser.parse_args()

expression_cutoff = 0.5

# excluded clusters and existing entities
excluded_clusters = []
with open('tmp/excluded_clusters.txt', 'r') as file:
    for line in file:
        excluded_clusters.append(line.rstrip())

existing_entities = []
if not args.refresh:
    with open('tmp/existing_entities.txt', 'r') as file:
        for line in file:
            existing_entities.append("FlyBase:" + line.rstrip())

ignored_entities = excluded_clusters + existing_entities

# EXPRESSION DATA

# get headers from expression_data file
expression_data = pd.read_csv("tmp/raw_expression_data.tsv", sep='\t', nrows=0)

# read expression_data in chunksize
expression_reader = pd.read_csv("tmp/raw_expression_data.tsv", sep='\t', dtype={'id': 'category', 'gene': 'category'}, chunksize=1000)

# filter each chunk and concatenate
for chunk in expression_reader:
    filtered = chunk[(chunk['expression_extent']>expression_cutoff) & (~chunk['id'].isin(ignored_entities))]
    expression_data = pd.concat([expression_data, filtered])

# make a a tsv for each new cluster
clusters = expression_data['id'].unique()
print(str(len(clusters)) + ' clusters')
for c in clusters:
    cluster_data = expression_data[expression_data['id']==c]
    cluster_data = cluster_data.assign(hide_in_terminfo = 'true')
    cluster_id = c.replace("FlyBase:", "")
    cluster_data.to_csv("expression_data/%s.tsv" % cluster_id, sep='\t', index=False)
