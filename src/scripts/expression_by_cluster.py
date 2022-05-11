import pandas as pd

expression_cutoff = 0.9

full_expresssion_data = pd.read_csv("tmp/expression_data.tsv", sep='\t')
clusters = set(full_expresssion_data['id'])

for c in clusters:
    cluster_id = c.replace("FlyBase:", "")
    cluster_data = full_expresssion_data[full_expresssion_data['id'].str.match(c)]
    cluster_data[cluster_data['expression_extent']>expression_cutoff].to_csv("expression_data/%s.tsv" % cluster_id, sep='\t', index=False)
