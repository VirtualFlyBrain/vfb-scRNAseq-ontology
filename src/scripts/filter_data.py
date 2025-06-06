import pandas as pd

## input and output
class DataEntity:
    dataset_id = ''
    datatype = ''
    raw_file = ''
    filtered_file = ''
    dataframe = None
    filtered_df = None
    def __init__(self, datatype, dataset_id=''):
        self.dataset_id = dataset_id
        self.datatype = datatype
        self.raw_file = 'tmp/raw_%s_data.tsv' % self.datatype.lower()
        self.filtered_file = 'tmp/filtered_%s_data.tsv' % self.datatype.lower()
        self.final_output_file = 'metadata_files/%s_%s_data.tsv' % (self.dataset_id, self.datatype.lower())
        try:
            self.dataframe = pd.read_csv(self.raw_file, sep='\t')
        except FileNotFoundError:
            self.dataframe = None
        try:
            self.filtered_df = pd.read_csv(self.filtered_file, sep='\t')
        except FileNotFoundError:
            self.filtered_df = None
    def write_filtered_tsv(self):
        self.dataframe.to_csv(self.filtered_file, sep='\t', index=None)
    def write_tsv_by_dataset(self):
        self.filtered_df.to_csv(self.final_output_file, sep='\t', index=None)
    def filter_by_other(self, owncol, other, othercol):
        """Keep only rows of self.dataframe where owncol (column name) value appears in other.dataframe[othercol]"""
        self.dataframe = self.dataframe[self.dataframe[owncol].isin(other.dataframe[othercol].drop_duplicates())]
    def split_filtered_df(self, datasets, split_by_col):
        new_sub_entites = []
        for i in datasets:
            new_sub_entity = DataEntity(datatype=self.datatype, dataset_id=i.replace('FlyBase:', ''))
            new_sub_entity.filtered_df = self.filtered_df[self.filtered_df[split_by_col]==i]
            new_sub_entites.append(new_sub_entity)
        return new_sub_entites


if __name__ == '__main__':

    from cypher_query import query_neo4j, pdb
    
    assay_data = DataEntity(datatype='Assay')
    sample_data = DataEntity(datatype='Sample')
    dataset_data = DataEntity(datatype='DataSet')
    clustering_data = DataEntity(datatype='Clustering')
    cluster_data = DataEntity(datatype='Cluster')


    ## Manual exclusions - add IDs of datasets to exclude in format "FlyBase:FBlc0000000"
    manual_exclusions = []
    dataset_data.dataframe = dataset_data.dataframe[~dataset_data.dataframe['id'].isin(manual_exclusions)]


    ## link assays and samples to the same dataset as any clusterings they appear in
    # (this may mean they end up linked to > 1 dataset)
    def update_dataset_from_clustering(input_df, clustering_data=clustering_data):
        """
        Expands dataset associations by creating additional rows with datasets from clustering data.
        Each input row may generate multiple output rows if additional dataset associations exist.
        Preserves the original associated_dataset values from input_df.
        
        Parameters:
        -----------
        input_df : pandas.DataFrame
            Input dataframe with 'id' and 'associated_dataset' columns
        clustering_data : object
            Object containing clustering information with a dataframe attribute
            that has 'associated_sample_or_assay_for_clustering' and 'associated_dataset' columns
        
        Returns:
        --------
        pandas.DataFrame
            Expanded dataframe with additional rows for new dataset associations
        """
        # Get unique id-dataset mappings from clustering data
        additional_datasets = (
            clustering_data.dataframe[['associated_sample_or_assay_for_clustering', 'associated_dataset']]
            .drop_duplicates()
            .rename(columns={'associated_sample_or_assay_for_clustering': 'id'})
        )
        
        # Initialize list to store dataframes
        result_dfs = [input_df.copy()]  # Start with the original data
        
        # For each unique ID, create additional rows with new dataset associations
        for id_val in input_df['id'].unique():
            entity_data = input_df[input_df['id'] == id_val]
            cluster_datasets = additional_datasets[additional_datasets['id'] == id_val]['associated_dataset']
            
            if not cluster_datasets.empty:
                for dataset in cluster_datasets:
                    new_rows = entity_data.copy()
                    new_rows['associated_dataset'] = dataset
                    result_dfs.append(new_rows)
        
        # Combine all dataframes
        output = pd.concat(result_dfs, ignore_index=True)
        output = output.drop_duplicates()
        return output

    assay_data.dataframe = update_dataset_from_clustering(assay_data.dataframe)
    sample_data.dataframe = update_dataset_from_clustering(sample_data.dataframe)


    ## filter for nervous system term-containing clusters
    # get :Nervous_system FBbt IDs from VFB
    query = "MATCH (c:Class:Nervous_system) WHERE c.short_form STARTS WITH \"FBbt\" RETURN DISTINCT c.short_form AS FBbt_ID"
    FBbt_IDs = query_neo4j(query, url=pdb)
    FBbt_IDs = list(FBbt_IDs['FBbt_ID'].apply(lambda x: x.replace('_', ':')))

    # check which clusters are linked to :Nervous_system FBbt terms
    ns_cluster_data = cluster_data.dataframe[cluster_data.dataframe['cell_type'].isin(FBbt_IDs)]
    # find datasets that are associated with nervous system clusters
    ns_datasets = ns_cluster_data['associated_dataset'].drop_duplicates()
    # filter datasets
    dataset_data.dataframe = dataset_data.dataframe[dataset_data.dataframe['id'].isin(ns_datasets)]

    # keep only assay, sample, cluster and clustering rows that are associated with a kept dataset
    for d in [cluster_data, clustering_data, assay_data, sample_data]:
        d.filter_by_other(owncol='associated_dataset', other = dataset_data, othercol = 'id')


    ## filtering based on experimental condition assays
    # assay ids to exclude based on relationship to a control assay by biological_reference_is
    excluded_assays = assay_data.dataframe[assay_data.dataframe['control_assay'].notnull()]['id'].drop_duplicates()
    # drop any clusterings that use an excluded assay
    excluded_clusters = clustering_data.dataframe[clustering_data.dataframe['associated_sample_or_assay_for_clustering'].isin(excluded_assays)]['id'].drop_duplicates()
    clustering_data.dataframe = clustering_data.dataframe[~clustering_data.dataframe['id'].isin(excluded_clusters)]

    # no longer need control_assay column
    for d in [assay_data, sample_data]:
        d.dataframe.drop('control_assay', axis=1, inplace=True)

    # keep only assay and sample rows that are associated with a kept clustering
    for d in [assay_data, sample_data]:
        d.filter_by_other(owncol='id', other = clustering_data, othercol = 'associated_sample_or_assay_for_clustering')

    # keep only dataset rows that are associated with a kept clustering
    dataset_data.filter_by_other(owncol='id', other = clustering_data, othercol = 'associated_dataset')

    # keep only cluster rows that are associated with a kept clustering
    cluster_data.filter_by_other(owncol='associated_clustering', other = clustering_data, othercol = 'id')


    ## output
    # filtered dataframes
    for d in [dataset_data, cluster_data, clustering_data, assay_data, sample_data]:
        d.write_filtered_tsv()

    # make a list of (all) inclusions (for process_metadata and process_expression_data)
    # this is different to internal_terms.txt, which is all entities currently incorporated into ontologies
    all_inclusions = []
    for d in [dataset_data, cluster_data, clustering_data, assay_data, sample_data]:
        all_inclusions.extend(d.dataframe['id'].drop_duplicates().to_list())

    with open('tmp/all_inclusions.txt', 'w') as f:
        f.write('\n'.join(all_inclusions))
