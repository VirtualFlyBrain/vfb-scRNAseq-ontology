import pandas as pd

expression_data = pd.read_csv('tmp/raw_expression_data.tsv', sep='\t')

outfile = "reports/FBgn_list.txt"

def get_unique_terms_from_col(column):
    """Input is a pandas dataframe column, output is a unique list of values (excluding nulls)."""
    return list(column.dropna().unique())

FBgns = sorted([g.replace('FlyBase:', '') for g in get_unique_terms_from_col(expression_data['gene'])])

with open(outfile, 'w') as file:
    file.write('\n'.join(FBgns) + '\n')
