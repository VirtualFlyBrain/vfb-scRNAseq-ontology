import pandas as pd
import argparse

# new sites must be added to VFB KB, then add FB name and VFB short form here:
sites_dict= {'EMBL-EBI Single Cell Expression Atlas Datasets': 'scExpressionAtlas'}

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--refresh", help="refresh all experiment metadata",
                    action="store_true")
args = parser.parse_args()

# excluded datasets and existing entities
excluded_datasets_and_assays_df = pd.read_csv('tmp/excluded_datasets_and_assays.tsv', sep='\t')
exclusions = excluded_datasets_and_assays_df.loc[:,'id'].tolist()
existing_entities = []
if not args.refresh:
    with open('tmp/existing_entities.txt', 'r') as file:
        for line in file:
            existing_entities.append("FlyBase:" + line.rstrip())

with open ('tmp/included_dataset_list.txt', 'r') as file:
    included_datasets = file.read().splitlines()

included_datasets = [i for i in included_datasets if not (i in existing_entities)]

def filter_and_format(data_type, data, exclusion_list, existing_list, sites_dict=sites_dict, included_datasets=included_datasets):
    """
    Remove excluded and existing (if not 'refresh'-ing) entities and reformat FB IDs.
    Also returns list of entities with an 'associated_' column value on the exclusion list.
    data is a DataFrame from a raw data output file from FlyBase SQL query.
    exclusion_list and existing_list are lists.
    """
    ignore_list = list(set(exclusion_list + existing_list))
    data = data.loc[~data['id'].isin(ignore_list)]

    def filter_by_associated_data(data=data, exclusion_list=ignore_list):
        """get 'associated_' columns and exclude any rows where value is on ignore list."""
        colnames = [col for col in data.columns.tolist() if 'associated_' in col]
        new_exclusions = []

        for col in colnames:
            new_exclusions.extend(data.loc[data[col].isin(exclusion_list),'id'].tolist())
        new_exclusions = list(set(new_exclusions))
        data = data.loc[~data['id'].isin(new_exclusions)]

        return (data, new_exclusions)

    output = filter_by_associated_data()
    data = output[0]
    new_exclusions = output[1]

    # extra columns
    split_by_col = 'associated_dataset'
    if data_type == 'dataset':
        split_by_col = 'id'
        data['neo_label'] = "DataSet"
        data['licence'] = "http://virtualflybrain.org/reports/VFBlicense_CC_BY_4_0"
        data['site'] = data['site_label'].apply(lambda x: "vfb:" + sites_dict[x])
        data = data.drop(['source_linkout', 'site_label'], axis=1).drop_duplicates()
        data = (data.groupby(['id', 'name', 'title', 'publication', 'licence', 'assay_type', 'site', 'neo_label']).agg({'accession': lambda x: "|".join(x)}).reset_index())
        publication_data = pd.DataFrame({"id":data.loc[:,"publication"].unique(), "neo_label":"pub"})
        publication_data.to_csv('tmp/publication_data.tsv', sep='\t', index=False)
    elif data_type == 'sample':
        data['neo_label'] = "Sample"
        data.drop(columns = ['control_assay'], inplace=True)
    elif data_type == 'cluster':
        data['neo_label'] = "Cluster"
    elif data_type == 'assay':
        data['neo_label'] = "Assay"
        data.drop(columns = ['control_assay'], inplace=True)

    for i in included_datasets:
        data[data[split_by_col]==i].to_csv('metadata_files/%s_%s_data.tsv' % (i.replace('FlyBase:', ''), data_type), sep='\t', index=False)

    return new_exclusions


dataset_data = pd.read_csv('tmp/raw_dataset_data.tsv', sep='\t')
new_ds_exc = filter_and_format('dataset', dataset_data, exclusions, existing_entities)
exclusions.extend(new_ds_exc)
assay_data = pd.read_csv('tmp/raw_assay_data.tsv', sep='\t')
new_assay_exc = filter_and_format('assay', assay_data, exclusions, existing_entities)
exclusions.extend(new_assay_exc)
sample_data = pd.read_csv('tmp/raw_sample_data.tsv', sep='\t')
new_sample_exc = filter_and_format('sample', sample_data, exclusions, existing_entities)
exclusions.extend(new_sample_exc)
clustering_data = pd.read_csv('tmp/raw_clustering_data.tsv', sep='\t')
clustering_exc = filter_and_format('clustering', clustering_data, exclusions, existing_entities)
exclusions.extend(clustering_exc)
cluster_data = pd.read_csv('tmp/raw_cluster_data.tsv', sep='\t')
cluster_exc = filter_and_format('cluster', cluster_data, exclusions, existing_entities)

with open('tmp/excluded_clusters.txt', 'w') as file:
    for c in cluster_exc:
        file.write(c + '\n')
