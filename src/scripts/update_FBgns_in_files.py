import modin.pandas as pd
pd.set_option('display.max_columns', 10)
import glob
import re
from process_expression_data import expression_file_loader
from filter_data import DataEntity

# ids to modify
mapping = pd.read_csv('tmp/id_validation_table.txt', sep='\t', low_memory=False)
changed_ids = mapping[~mapping['#submitted_item'].isin(mapping['validated_id'])]
changed_ids = changed_ids.set_index('#submitted_item', verify_integrity=True)
replacement_dict = changed_ids['validated_id'].to_dict()

exp_files = glob.glob('expression_data/*.owl')

regex = re.compile("|".join(replacement_dict))

for f in exp_files:
    dataset = 'FlyBase:' + re.search('FBlc[0-9]{7}', f)[0]
    # check whether file already contains both old and new terms for any entity
    with open((f + '.fbgns.tmp'), 'r') as genes:
        gene_list = [l.strip() for l in genes.readlines()]
    old_exists = changed_ids[changed_ids.index.isin(gene_list)]
    old_and_new = old_exists[old_exists['validated_id'].isin(gene_list)]
    prefixed_old_and_new = old_and_new.add_prefix('FlyBase:', axis=0)
    prefixed_old_and_new = prefixed_old_and_new.replace(r'FBgn([0-9]{7})', r'FlyBase:FBgn\1', regex=True)
    if len(prefixed_old_and_new) > 0:
        cluster_data = DataEntity(datatype='Cluster')
        clusters = cluster_data.dataframe[
            cluster_data.dataframe['associated_dataset']==dataset]['id'].drop_duplicates()
        raw_exp_dataset = expression_file_loader(clusters, 0)
        flybase_gene_usage = raw_exp_dataset[(raw_exp_dataset['gene'].isin(prefixed_old_and_new.index)) | raw_exp_dataset['gene'].isin(prefixed_old_and_new['validated_id'])]
        print(f'Old and new ids for same entity in use in {dataset}:')
        print(prefixed_old_and_new)
        print('Usage for this dataset in FlyBase:')
        print(flybase_gene_usage)
        print(f'Not updating file {f} - please check and edit manually.')
        raise ValueError("Usage of old and replacement gene IDs in same file!")
    if len(old_exists) == 0:
        print(f'nothing to update in {f}')
    else:
        with open(f, "r") as infile, open(f.replace('dataset_', 'processed_dataset_'), "w+") as outfile:
            for line in infile:
                outfile.write(regex.sub(lambda m: replacement_dict[m.group()], line))
            print(f'{f} updated!')
