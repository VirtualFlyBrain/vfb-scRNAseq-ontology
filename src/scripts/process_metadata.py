import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--refresh", help="refresh all experiment metadata",
                    action="store_true")
args = parser.parse_args()

# excluded datasets and existing entities
excluded_datasets_and_samples_df = pd.read_csv('tmp/excluded_datasets_and_samples.tsv', sep='\t')
exclusions = excluded_datasets_and_samples_df.loc[:,'id'].tolist()
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
        #data['associated_dataset'] = data['associated_dataset'].map(lambda x: x.replace("FlyBase:", "http://flybase.org/reports/"))
    #if 'publication' in data.columns:
    #    data['publication'] = data['publication'].map(lambda x: x.replace("FlyBase:", "http://flybase.org/reports/"))

    # extra columns
    if data_type == 'dataset':
        data.loc[:,'neo_label'] = "DataSet"
        data.loc[:,'licence'] = "http://virtualflybrain.org/reports/VFBlicense_CC_BY_4_0"
        publication_data = pd.DataFrame({"@type":"Publication", "id":data.loc[:,"publication"].unique(), "neo_label":"pub"})
        publication_data.to_csv('tmp/publication_data.tsv', sep='\t', index=False)
    elif data_type == 'sample':
        data.loc[:,'neo_label'] = "Sample"
        data.drop(columns = ['associated_assay', 'control_assay'], inplace=True)
    elif data_type == 'cluster':
        data.loc[:,'neo_label'] = "Cluster"

    data.to_csv('tmp/%s_data.tsv' % data_type, sep='\t', index=False)

    return new_exclusions


dataset_data = pd.read_csv('tmp/raw_dataset_data.tsv', sep='\t')
new_ds_exc = filter_and_format('dataset', dataset_data, exclusions, existing_entities)
exclusions.extend(new_ds_exc)
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

