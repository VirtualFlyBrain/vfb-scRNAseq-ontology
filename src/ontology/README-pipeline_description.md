# Description of VFB_scRNAseq update process 

###### Switches (in VFB_scRNAseq.Makefile):

UPDATE_FROM_FB = true
 - Get fresh data from FlyBase (only needed after a new FB release)

REFRESH_EXP = false
 - Flush and replace all expression data files (very slow - several days)
 
REFRESH_META = true
 - Flush and replace all metadata files

## Overview

To run a standard release with the defaults above:

`sh run_release.sh`

This includes three main processing steps:
1. `sh run.sh make all_tsvs -B`:
Produce tsv files with metadata and expression data for new (and existing if a REFRESH switch is true) datasets.

2. `sh run.sh make update_ontology_files -B`:
Create an ontology file from each tsv from step 1, overwriting an existing ontology file if it exists, then remove the tsv.


3. `sh run.sh make prepare_release_notest -B`:
Create and update external imports for each dataset, merge imports into metadata files and move to `metadata_release_files`.


An `-edit` file that imports all of the datasets is (automatically) maintained and all information could theoretically be viewed as a whole on a machine with sufficient memory. However, we are unable do the normal ODK merging and preprocessing steps on most ordinary computers, so all of the processing is by dataset, requiring significant changes to ODK defaults. Notably generation of EDIT_PREPROCESSED, SRCMERGED and PRESEED files is overwritten to avoid processing the full ontology.

## In more detail

#### Data file generation (steps 1 and 2)

The first step is to run sql queries against the public FlyBase chado with the `get_FB_data` target (if UPDATE_FROM_FB = true) to extract metadata for scRNAseq datasets, samples, assays, clusterings and clusters, and summarised gene expression data for each cluster.
This data is then processed to produce tsvs that can be parsed by linkml-owl to produce ontology files according to `VFB_scRNAseq_schema.yaml`.

Metadata files with information about datasets, samples, assays, clusterings and clusters are all regenerated unless REFRESH_META = false, in which case only new dataset metadata will be processed into new ontology files. We exclude any datasets with no clusters annotated with nervous system cell types. We also exclude any clusters that are not from control/wild type samples. This filtering is carried out by the `filter_data.py` script.
Datasets, samples, assays, clusterings and clusters are processed into separate tsvs by `process_metadata.py`, converted to ontologies with linkml-owl, then merged by dataset to produce files in the `ontology_files` directory.

Existing expression data files are not regenerated unless REFRESH_EXP = true (as this may take several days processing time). Expression data is also not processed for any clusters that are excluded from VFB. We set a cutoff of extent=0.2 for included data (i.e. a gene must be expressed in at least 20% of cells in its cluster to be included).
Expression data for each cluster is processed into tsvs by `process_expression_data.py`, converted to ontologies with linkml-owl, then merged by dataset to produce files in the `expression_data` directory.


#### Imports (part of step 3)

 Seed files of imported term IDs are created for each dataset and used to extract dataset-specific imports (`imports/%_import.owl`) from `mirror/merged.owl`, which is created according to ODK defaults. A file (`imports/merged_import.owl`) with all imported terms for all datasets is created from a merged seed file, `merged_terms_combined.txt`.
