import pandas as pd
import re

sites_dict= {'EMBL-EBI Single Cell Expression Atlas Datasets': 'scExpressionAtlas'}

dataset_data = pd.read_csv('tmp/dataset_data.tsv', sep='\t')

dataset_data['site'] = dataset_data['site_label'].apply(lambda x: "vfb:" + sites_dict[x])
dataset_data = dataset_data.drop(['source_linkout', 'site_label'], axis=1).drop_duplicates()

dataset_data.to_csv('tmp/dataset_data.tsv', sep='\t', index=False)

