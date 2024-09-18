import pandas as pd
import dask
import dask.dataframe as dd

schema = {
    'id': 'string',
    'gene': 'string',
    'expression_extent': 'float64',
    'expression_level': 'float64'
}

expression_data = dd.read_csv("tmp/raw_expression_data.tsv", sep='\t')
expression_data.to_parquet("tmp/expression_data/", schema=schema, partition_on='id', overwrite=True)
