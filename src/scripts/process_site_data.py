import pandas as pd

# new sites must be added to VFB KB, then add FB name and VFB short form here:
sites_dict= {'EMBL-EBI Single Cell Expression Atlas Datasets': 'scExpressionAtlas'}

dataset_data = pd.read_csv('tmp/dataset_data.tsv', sep='\t')

dataset_data['site'] = dataset_data['site_label'].apply(lambda x: "vfb:" + sites_dict[x])
dataset_data = dataset_data.drop(['source_linkout', 'site_label'], axis=1).drop_duplicates()

dataset_data = (dataset_data.groupby(['id', 'name', 'title', 'publication', 'licence', 'assay_type', 'site', 'neo_label'])\
  .agg({'accession': lambda x: "|".join(x)}).reset_index())

dataset_data.to_csv('tmp/dataset_data.tsv', sep='\t', index=False)

