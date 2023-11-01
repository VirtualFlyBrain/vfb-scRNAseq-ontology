import pandas as pd
from  get_external_terms import get_unique_terms_from_col


expression_data = pd.read_csv('tmp/raw_expression_data.tsv', sep='\t')

outfile = "reports/FBgn_list.txt"

all_external_terms = [g.replace('FlyBase:', '') for g in get_unique_terms_from_col(expression_data['gene'])]

with open(outfile, 'w') as file:
    file.write('\n'.join(all_external_terms))
