import glob
import re

# REPLACEMENTS HERE
replacement_dict = {'<custom:hide_in_terminfo>None</custom:hide_in_terminfo>': '<custom:hide_in_terminfo rdf:datatype="http://www.w3.org/2001/XMLSchema#boolean">true</custom:hide_in_terminfo>'}

exp_files = glob.glob('expression_data/*.owl')

regex = re.compile("|".join(replacement_dict))
print(replacement_dict)
print(regex)

def process_file(filename, pattern=regex, replacement_dict=replacement_dict):
    output_filename = filename.replace('VFB_scRNAseq_exp_', 'processed_dataset_')
    with open(filename, "r") as infile, open(output_filename, "w") as outfile:
        for line in infile:
            processed_line = pattern.sub(lambda m: replacement_dict[m.group(0)], line)
            outfile.write(processed_line)
    print(f'{filename} successfully processed to {output_filename}!')

for f in exp_files:
    process_file(f)
