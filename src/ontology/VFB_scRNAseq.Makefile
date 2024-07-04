## Customize Makefile settings for VFB_scRNAseq
##
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

.PHONY: prepare_release_notest
# this prepares a release without updating the source files or running any tests - run using command in run_release.sh
prepare_release_notest: $(SRC) update_catalog_files all_imports release_ontology_files $(REPORTDIR)/FBgn_list.txt gen_docs
	rm -f $(CLEANFILES) $(ALL_TERMS_COMBINED) &&\
	echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on your git hosting site such as GitHub or GitLab"

# flags to bypass recreation of existing gene expression and experiment metadata
# NB refreshing expression data will greatly increase processing time (may take several days)
UPDATE_FROM_FB = true
REFRESH_EXP = false
REFRESH_META = false
IMPORTS_ONLY = false
IMP = true

########## directories and commands

EXPDIR = expression_data
METADATADIR = metadata_files
ONTOLOGYDIR = ontology_files
RELEASEDIR = ../../metadata_release_files

$(EXPDIR) $(METADATADIR) $(RELEASEDIR) $(ONTOLOGYDIR):
	mkdir -p $@

LINKML = linkml-data2owl -s VFB_scRNAseq_schema.yaml
ROBOT_O = robot --catalog $(CATALOG_O)
CATALOG_O = $(ONTOLOGYDIR)/catalog-v001.xml

.DEFAULT:
	echo $@
	# Default recipe for anything that doesn't have a recipe
	# Stops make complaining that no recipe exists for tsvs

########## Installations

.PHONY: install_linkml
install_linkml:
	python3 -m pip install linkml-owl

.PHONY: install_postgresql
install_postgresql:
	apt-get update
	apt-get -y install postgresql-client

########## get data from FlyBase and generate input tsvs

.PHONY: get_FB_data
get_FB_data: install_postgresql | $(EXPDIR) $(TMPDIR)
ifeq ($(UPDATE_FROM_FB),true)
	psql -h chado.flybase.org -U flybase flybase -f ../sql/dataset_query.sql \
	 > $(TMPDIR)/raw_dataset_data.tsv
	psql -h chado.flybase.org -U flybase flybase -f ../sql/sample_query.sql \
	 > $(TMPDIR)/raw_sample_data.tsv
	psql -h chado.flybase.org -U flybase flybase -f ../sql/assay_query.sql \
	 > $(TMPDIR)/raw_assay_data.tsv
	psql -h chado.flybase.org -U flybase flybase -f ../sql/clustering_query.sql \
	 > $(TMPDIR)/raw_clustering_data.tsv
	psql -h chado.flybase.org -U flybase flybase -f ../sql/cluster_query.sql \
	 > $(TMPDIR)/raw_cluster_data.tsv
	psql -h chado.flybase.org -U flybase flybase -f ../sql/expression_query.sql \
	 > $(TMPDIR)/raw_expression_data.tsv
else
	echo "Not updating FlyBase data."
endif

.PHONY: unzip_exp_files
# unzip expression files - overwrites any existing owl files, keeping .gz version too
unzip_exp_files:
	for FILE in $(EXPDIR)/*.owl.gz; \
	do gzip -dkf $$FILE; done

# get all FBlc terms
$(TMPDIR)/internal_terms.txt: | $(TMPDIR)
	touch $@
	for FILE in $(ONTOLOGYDIR)/*.owl; \
	do $(ROBOT_O) query --input $$FILE \
	--query ../sparql/internal_terms.sparql $(TMPDIR)/internal_terms-raw.txt &&\
	cat $(TMPDIR)/internal_terms-raw.txt $@ | grep -oE 'FBlc[0-9]+' | sort | uniq > $@-tmp.txt &&\
	mv $@-tmp.txt $@; done &&\
	rm -f $(TMPDIR)/internal_terms-raw.txt

# filter data to only get nervous system associated data and only wild-type non-experimental samples
$(TMPDIR)/all_inclusions.tsv: get_FB_data | $(TMPDIR)
	python3 -m pip install vfb-connect
	python3 $(SCRIPTSDIR)/filter_data.py

.PHONY: process_FB_metadata
# filter FB data to remove metadata for excluded datasets/assays and, if REFRESH_META is false, remove existing metadata (i.e. entities in a file in ontology_files) from input
process_FB_metadata: $(TMPDIR)/internal_terms.txt get_FB_data $(TMPDIR)/all_inclusions.tsv | $(METADATADIR)
ifeq ($(REFRESH_META),true)
	python3 $(SCRIPTSDIR)/process_metadata.py -r
else
	python3 $(SCRIPTSDIR)/process_metadata.py
endif

.PHONY: process_FB_expdata
# filter FB data to remove clusters for excluded datasets/assays and, if REFRESH_EXP is false, remove existing clusters (i.e. those in a file in ontology_files) from input
# also split into tsvs for each cluster and filter by extent
process_FB_expdata: $(TMPDIR)/internal_terms.txt get_FB_data $(TMPDIR)/all_inclusions.tsv process_FB_metadata | $(EXPDIR) $(METADATADIR)
ifeq ($(REFRESH_EXP),true)
	python3 $(SCRIPTSDIR)/process_expression_data.py -r
else
	python3 $(SCRIPTSDIR)/process_expression_data.py
endif

.PHONY: all_tsvs
all_tsvs: unzip_exp_files get_FB_data process_FB_metadata process_FB_expdata
	echo  "Input tsvs generated"


########## make ontology files from input tsvs


# metatdata owl files for datasets that have 'dataset' metadata files
DATASET_META_FILES = $(patsubst $(METADATADIR)/%_dataset_data.tsv,$(ONTOLOGYDIR)/VFB_scRNAseq_%.owl,$(wildcard $(METADATADIR)/*_dataset_data.tsv))

.PHONY: update_metadata_files
# tsvs must already be in place before makefile is read to generate owl files
update_metadata_files: $(DATASET_META_FILES)
	echo  "Metadata ontologies updated"

# make an ontology from existing linkml metadata templates
$(ONTOLOGYDIR)/VFB_scRNAseq_%.owl: install_linkml
	$(LINKML) -C Dataset $(METADATADIR)/$*_dataset_data.tsv -o $(METADATADIR)/$*_dataset_data.ofn &&\
	$(LINKML) -C Publication $(METADATADIR)/$*_pub_data.tsv -o $(METADATADIR)/$*_pub_data.ofn &&\
	$(LINKML) -C Sample $(METADATADIR)/$*_sample_data.tsv -o $(METADATADIR)/$*_sample_data.ofn &&\
	$(LINKML) -C Assay $(METADATADIR)/$*_assay_data.tsv -o $(METADATADIR)/$*_assay_data.ofn &&\
	$(LINKML) -C Cluster $(METADATADIR)/$*_cluster_data.tsv -o $(METADATADIR)/$*_cluster_data.ofn &&\
	$(LINKML) -C Clustering $(METADATADIR)/$*_clustering_data.tsv -o $(METADATADIR)/$*_clustering_data.ofn &&\
	$(ROBOT) merge \
	--input $(METADATADIR)/$*_dataset_data.ofn \
	--input $(METADATADIR)/$*_pub_data.ofn \
	--input $(METADATADIR)/$*_sample_data.ofn \
	--input $(METADATADIR)/$*_assay_data.ofn \
	--input $(METADATADIR)/$*_cluster_data.ofn \
	--input $(METADATADIR)/$*_clustering_data.ofn \
	--include-annotations true --collapse-import-closure false \
	annotate --ontology-iri "http://virtualflybrain.org/data/VFB/OWL/VFB_scRNAseq_$*.owl" \
	--annotation dc:description "An ontology of Drosophila melanogaster scRNAseq data from a single dataset ($*). This information is taken from FlyBase, which sources it from the EMBL-EBI Single Cell Expression Atlas, which compiles scRNAseq data from multiple sources." \
	--annotation dc:title "VFB scRNAseq Ontology for dataset $*" \
	--link-annotation owl:imports "http://purl.obolibrary.org/obo/VFB_scRNAseq/imports/$*_import.owl" \
	--link-annotation owl:imports "http://purl.obolibrary.org/obo/VFB_scRNAseq/expression_data/dataset_$*.owl" \
	convert --format owl \
	-o $@ &&\
	rm -f $(METADATADIR)/$*_*.tsv $(METADATADIR)/$*_*.ofn

.PHONY: make_exp_ofns
# check whether ofn exists for each cluster tsv, delete tsv if true, make ofn then delete tsv if false.
make_exp_ofns: install_linkml
	apt-get update
	apt-get -y install parallel
	find $(EXPDIR) -name "*.tsv" | parallel -j 5 ' \
		if [ -e {.}.ofn ]; then \
			rm {}; \
		else \
			$(LINKML) {} -o {.}.ofn && rm {}; \
		fi'

# gene expression owl files for datasets that have 'cluster' expression data tsvs or ofns (names are dataset_FBlcxxxxxxx-cluster_FBlcxxxxxxx)
DATASET_EXP_FILES = $(sort $(filter-out cluster_%,$(subst -,.owl ,$(wildcard $(EXPDIR)/*.tsv))) $(filter-out cluster_%,$(subst -,.owl ,$(wildcard $(EXPDIR)/*.ofn))))

# for troubleshooting (check that expected dataset files are in list)
check_ds:
	echo $(DATASET_EXP_FILES)

.PHONY: update_expression_files
# tsvs must already be in place before makefile is read to generate ofns
update_expression_files: $(DATASET_EXP_FILES)
	echo  "Expression ontologies updated"

# merge and annotate cluster ofns for each dataset
# need to reformat expression annotations as these don't get the right types from linkml
$(EXPDIR)/dataset_%.owl: make_exp_ofns
	$(ROBOT) merge --inputs "$(EXPDIR)/dataset_$*-cluster_*.ofn" \
	annotate --ontology-iri "http://purl.obolibrary.org/obo/VFB_scRNAseq/$@" \
	convert --format ofn -o $(TMPDIR)/$*-exp-tmp.ofn &&\
	cat $(TMPDIR)/$*-exp-tmp.ofn | sed -e 's/(neo_custom:expression_\([a-z]\+\) "\([0-9]\+\.[0-9]\+\)")/(neo_custom:expression_\1 "\2"^^xsd:float)/g' -e 's/(neo_custom:hide_in_terminfo "\([a-z]\+\)")/(neo_custom:hide_in_terminfo "\1"^^xsd:boolean)/g' > $@ &&\
	$(ROBOT) convert -i $@ --format owl -o $@ &&\
	$(ROBOT) convert -i $@ --format owl -o $@.gz &&\
	rm -f $(EXPDIR)/dataset_$*-cluster_*.ofn $(TMPDIR)/$*-exp-tmp.ofn

.PHONY: update_ontology_files
update_ontology_files: update_metadata_files update_expression_files
	echo  "All ontology files updated"


########## release steps - imports, merged and compressed release files, reports

# variables - need ontologies to be made already
# dataset IDs from ontologies in ontology_files
RELEASE_DATASETS = $(patsubst $(ONTOLOGYDIR)/VFB_scRNAseq_%.owl,%,$(wildcard $(ONTOLOGYDIR)/*.owl))
ONTOLOGY_IMPORT_FILES = $(patsubst %,$(IMPORTDIR)/%_import.owl,$(RELEASE_DATASETS))
IMPORT_SEED_FILES = $(patsubst %,$(IMPORTDIR)/%_terms.txt,$(RELEASE_DATASETS))
RELEASE_ONTOLOGY_FILES = $(patsubst %,$(RELEASEDIR)/VFB_scRNAseq_%.owl,$(RELEASE_DATASETS))

.PHONY: all_imports
all_imports: create_import_stubs $(ONTOLOGY_IMPORT_FILES) # merged import is default prerequisite
	rm -f $(IMPORTDIR)/*terms.txt $(IMPORTDIR)/*terms_combined.txt

.PHONY: create_import_stubs
# make an empty ontology for imports to stop robot complaining
create_import_stubs:
	for FILE in $(ONTOLOGY_IMPORT_FILES); do \
		if ! test -f $$FILE; then \
			cp $(IMPORTDIR)/empty_import.txt $$FILE &&\
			$(ROBOT) annotate -i $$FILE \
			--ontology-iri "http://purl.obolibrary.org/obo/VFB_scRNAseq/imports/$$FILE" \
			-o $$FILE; fi; \
		done

# import seeds for each ontology
# need to add RO_0002292 (expresses), which is only in the expression imports
$(IMPORTDIR)/%_terms.txt: create_import_stubs | $(ONTOLOGYDIR) $(TMPDIR)
ifeq ($(IMP),true)
	$(ROBOT_O) query --input $(ONTOLOGYDIR)/VFB_scRNAseq_$*.owl --query ../sparql/external_terms.sparql $@ &&\
	echo "http://purl.obolibrary.org/obo/RO_0002292" >> $@
else
	touch $@
endif

$(IMPORTDIR)/merged_terms_combined.txt: $(IMPORT_SEED_FILES) | $(TMPDIR)
ifeq ($(IMP),true)
	cat $(IMPORT_SEED_FILES) | sort | uniq > $@
else
	touch $@
endif

.PHONY: release_ontology_files
release_ontology_files: $(RELEASE_ONTOLOGY_FILES)
	echo $@

.PHONY: update_catalog_files
update_catalog_files:
	python3 -m pip install beautifulsoup4
	python3 -m pip install lxml
	python3 $(SCRIPTSDIR)/update_catalogs.py

# create merged release files (no need to reason etc)
# remove expression import (loaded separately into VFB)
$(RELEASEDIR)/VFB_scRNAseq_%.owl: | $(RELEASEDIR)
	cat $(ONTOLOGYDIR)/VFB_scRNAseq_$*.owl | grep -v "http://purl.obolibrary.org/obo/VFB_scRNAseq/expression_data/dataset_$*.owl" > $(ONTOLOGYDIR)/VFB_scRNAseq_$*-tmp.owl
	$(ROBOT_O) merge -i $(ONTOLOGYDIR)/VFB_scRNAseq_$*-tmp.owl \
	convert --format owl \
	-o $@
	rm -f $(ONTOLOGYDIR)/VFB_scRNAseq_$*-tmp.owl

# this is needed for gene annotations in vfb-scRNAseq-gene-annotations repo
$(REPORTDIR)/FBgn_list.txt: $(TMPDIR)/existing_FBgns.txt | $(REPORTDIR)
	cp $< $@ &&\
	rm -f $(EXPDIR)/*.fbgns.tmp

# make a $(SRC) file that imports all the owl files in ontology_files
$(SRC):
	python3 $(SCRIPTSDIR)/create_src.py

# remove any existing docs and generate fresh
.PHONY: gen_docs
gen_docs: install_linkml
	rm -fr ../../docs
	gen-doc ./VFB_scRNAseq_schema.yaml --directory ../../docs


######## UPDATE OBSOLETE GENES
# generating seed file (to extract FBgns from there) needs too much memory (so using grep)
$(TMPDIR)/existing_FBgns.txt: unzip_exp_files
	for FILE in $(EXPDIR)/*.owl; \
	do cat $$FILE | grep --only-matching -E "FBgn[0-9]+" | sort | uniq > $$FILE.fbgns.tmp; done &&\
	cat $(EXPDIR)/*.fbgns.tmp | sort | uniq > $@

.PHONY: get_gene_id_map
get_gene_id_map: install_postgresql
	# this won't work until https://flybase.github.io/docs/chado/functions#update_ids is fixed
	python3 $(SCRIPTSDIR)/print_id_query.py &&\
	psql -h chado.flybase.org -U flybase flybase -f ../sql/id_update_query.sql \
	 > $(TMPDIR)/id_validation_table.tsv

replace_gene_ids_in_files:
	# need to get 'tmp/id_validation_table.txt' file from manual use of id validator
	python3 $(SCRIPTSDIR)/update_FBgns_in_files.py &&\
	for DS in $(RELEASE_DATASETS); \
	do if [ -f $(EXPDIR)/processed_dataset_$$DS.owl ]; \
	then mv $(EXPDIR)/processed_dataset_$$DS.owl $(EXPDIR)/dataset_$$DS.owl; fi &&\
	$(ROBOT) convert -i $(EXPDIR)/dataset_$$DS.owl --format owl -o $(EXPDIR)/dataset_$$DS.owl.gz &&\
	rm $(EXPDIR)/dataset_$$DS.owl.fbgns.tmp; done

######## overwrite some ODK goals to prevent unnecessary processing

$(EDIT_PREPROCESSED): $(SRC)
	cp $< $@

$(SRCMERGED): $(EDIT_PREPROCESSED) $(OTHER_SRC)
	cp $< $@

$(PRESEED):
	touch $@

$(ALL_TERMS_COMBINED):
	touch $@

.PHONY: update_repo
# don't keep adding extra imports
update_repo:
	sh $(SCRIPTSDIR)/update_repo.sh
	rm -f $(foreach n,$(IMPORTS), $(IMPORTDIR)/$(n)_import.owl) $(foreach n,$(IMPORTS), $(IMPORTDIR)/$(n)_terms.txt)
