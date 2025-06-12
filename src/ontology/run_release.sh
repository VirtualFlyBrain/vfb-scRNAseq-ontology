set -e

# Create tsv files for all ofns that need updating
sh run.sh make all_tsvs -B

# Update ofns (expression and metadata for each dataset) and remove tsvs
sh run.sh make update_ontology_files -B

# Release - update imports, merge meta, exp and imports for each ds and put zipped versions in release_files.
sh run.sh make prepare_release_notest -B
