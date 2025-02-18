# VFB scRNAseq Ontology

The VFB scRNAseq ontology files contain scRNAseq data to be loaded into VFB.

This information is taken from [FlyBase](https://flybase.org/), which sources it from the [EMBL-EBI Single Cell Expression Atlas](https://www.ebi.ac.uk/gxa/sc/home), which compiles scRNAseq data from multiple sources.

For incorporation into VFB, datasets are filtered to only include those with some nervous system component(s) and only wild-type data.

Due to size, data is split by dataset. Metadata files with non-expression (external ontology) imports merged in and no import statements are in [metadata_release_files](metadata_release_files), unmerged metadata files that import their respective gene expression files (as well as external ontologies) are in [src/ontology/ontology_files](src/ontology/ontology_files). Compressed gene expression files are in [src/ontology/expression_data](src/ontology/expression_data) and can be uncompressed locally using `sh run.sh make unzip_exp_files` (assuming you are using [ODK](https://github.com/INCATools/ontology-development-kit)). While it is technically possible to open this all as one ontology by opening [src/ontology/VFB_scRNAseq-edit.ofn](src/ontology/VFB_scRNAseq-edit.ofn), this is not recommended due to large size and memory requirements.

### Editors' version

The -edit version, [src/ontology/VFB_scRNAseq-edit.ofn](src/ontology/VFB_scRNAseq-edit.ofn), is autogenerated and should not be manually edited.

## Contact

Please use this GitHub repository's [Issue tracker](https://github.com/VirtualFlyBrain/vfb-scRNAseq-ontology/issues) to report errors or specific concerns related to the ontology.

## Acknowledgements

This ontology repository was created using the [Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit).