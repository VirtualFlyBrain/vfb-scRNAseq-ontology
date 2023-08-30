## Customize Makefile settings for VFB_scRNAseq
##
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

.PHONY: prepare_release
prepare_release: $(SRC) all_components $(IMPORT_FILES) $(MAIN_FILES) $(REPORTDIR)/FBgn_list.txt
	rsync -R $(MAIN_FILES) $(RELEASEDIR) &&\
  rm -f $(CLEANFILES) &&\
  echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on your git hosting site such as GitHub or GitLab"

# flags to bypass recreation of existing gene expression and experiment metadata
# NB setting either of these (especially for expression data) to TRUE will greatly increase processing time (many hours, possibly days)
UPDATE_FROM_FB = TRUE
REFRESH_EXP = FALSE
REFRESH_META = FALSE

# files and commands
EXPDIR = expression_data
LINKML = linkml-data2owl -s VFB_scRNAseq_schema.yaml
NEW_EXPRESSION_TSVS = $(wildcard $(EXPDIR)/*.tsv)
NEW_EXPRESSION_OFNS = $(NEW_EXPRESSION_TSVS:.tsv=.ofn)
CLEANFILES := $(CLEANFILES) $(patsubst %, $(IMPORTDIR)/%_terms_combined.txt, $(IMPORTS))


.PHONY: get_FB_data
get_FB_data: $(EXPDIR)
ifeq ($(UPDATE_FROM_FB),TRUE)
	apt-get update
	apt-get -y install postgresql-client
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

.PHONY: process_FB_metadata
process_FB_metadata: $(TMPDIR)/existing_entities.txt get_FB_data $(TMPDIR)/excluded_datasets_and_assays.tsv
	# filter FB data to remove metadata for excluded datasets and, if REFRESH_META is TRUE, remove existing metadata
ifeq ($(REFRESH_META),TRUE)
	python3 $(SCRIPTSDIR)/process_metadata.py -r
else
	python3 $(SCRIPTSDIR)/process_metadata.py
endif
	python3 $(SCRIPTSDIR)/process_site_data.py
	
.PHONY: process_FB_expdata
process_FB_expdata: $(TMPDIR)/existing_entities.txt get_FB_data $(TMPDIR)/excluded_datasets_and_assays.tsv process_FB_metadata | $(EXPDIR)
	# filter FB data to remove clusters for excluded datasets and, if REFRESH_EXP is FALSE, remove existing clusters
	# also split into tsvs for each cluster and filter by extent
ifeq ($(REFRESH_EXP),TRUE)
	python3 $(SCRIPTSDIR)/process_expression_data.py -r
else
	python3 $(SCRIPTSDIR)/process_expression_data.py
endif

.DEFAULT:
	echo $@
	# Default recipe for anything that doesn't have a recipe
	# Stops make complaining that no recipe exists for tsvs

.PHONY: install_linkml
install_linkml:
	python3 -m pip install linkml-owl==v0.2.2

$(EXPDIR):
	mkdir -p $@

$(TMPDIR)/existing_entities.txt:
	$(ROBOT) query --input $(SRC) \
  --query ../sparql/existing_entities.sparql $(TMPDIR)/existing_entities.csv &&\
	grep -oE 'FBlc[0-9]+' $(TMPDIR)/existing_entities.csv > $@ &&\
	rm $(TMPDIR)/existing_entities.csv

$(TMPDIR)/excluded_datasets_and_assays.tsv: get_FB_data
	python3 -m pip install vfb-connect
	python3 $(SCRIPTSDIR)/excluded_datasets_and_assays.py

$(EXPDIR)/%.ofn: $(EXPDIR)/%.tsv | $(EXPDIR) install_linkml
	$(LINKML) $< -o $@ && rm $<

$(SRC): install_linkml process_FB_metadata
	mv $(SRC) $(TMPDIR)/old-$(SRC)
	$(LINKML) -C Dataset $(TMPDIR)/dataset_data.tsv -o $(TMPDIR)/dataset_data.ofn &&\
	$(LINKML) -C Sample $(TMPDIR)/sample_data.tsv -o $(TMPDIR)/sample_data.ofn &&\
	$(LINKML) -C Assay $(TMPDIR)/assay_data.tsv -o $(TMPDIR)/assay_data.ofn &&\
	$(LINKML) -C Cluster $(TMPDIR)/cluster_data.tsv -o $(TMPDIR)/cluster_data.ofn &&\
	$(LINKML) -C Clustering $(TMPDIR)/clustering_data.tsv -o $(TMPDIR)/clustering_data.ofn &&\
	$(LINKML) -C Publication $(TMPDIR)/publication_data.tsv -o $(TMPDIR)/publication_data.ofn &&\
	$(ROBOT) merge \
	--input VFB_scRNAseq-annotations.ofn \
	--input $(TMPDIR)/dataset_data.ofn \
	--input $(TMPDIR)/sample_data.ofn \
	--input $(TMPDIR)/assay_data.ofn \
	--input $(TMPDIR)/cluster_data.ofn \
	--input $(TMPDIR)/clustering_data.ofn \
	--input $(TMPDIR)/publication_data.ofn \
	--include-annotations true --collapse-import-closure false \
	-o $(TMPDIR)/merged-meta.owl
ifeq ($(REFRESH_META),TRUE)
	$(ROBOT) convert -i $(TMPDIR)/merged-meta.owl --format ofn \
	-o $@
else
	$(ROBOT) remove --input $(TMPDIR)/old-$(SRC) \
	--select "ontology" \
	merge --input $(TMPDIR)/merged-meta.owl \
	--include-annotations true --collapse-import-closure false \
	convert --format ofn \
	-o $@
endif
	echo "\nOntology source file updated!\n"

$(COMPONENTSDIR)/expression_data.owl: process_FB_expdata $(NEW_EXPRESSION_OFNS) | $(COMPONENTSDIR)
ifeq ($(REFRESH_EXP),TRUE)
	$(ROBOT) merge --inputs "$(EXPDIR)/*.ofn" \
	-o $(TMPDIR)/expression_data.owl
else
	$(ROBOT) merge --input $@ --inputs "$(EXPDIR)/*.ofn" \
	-o $(TMPDIR)/expression_data.owl
endif
	$(ROBOT) annotate --input $(TMPDIR)/expression_data.owl \
	--ontology-iri "http://purl.obolibrary.org/obo/VFB_scRNAseq/components/expression_data.owl" \
	convert --format ofn -o $@.tmp &&\
	cat $@.tmp | sed -e 's/(custom:expression_\([a-z]\+\) "\([0-9]\+\.[0-9]\+\)")/(custom:expression_\1 "\2"^^xsd:float)/g' -e 's/(custom:hide_in_terminfo "\([a-z]\+\)")/(custom:hide_in_terminfo "\1"^^xsd:boolean)/g' > $@ &&\
	gzip -c $@ > $@.gz &&\
	rm -f $(EXPDIR)/*.ofn $@.tmp &&\
	echo "\nGene expression file updated!\n"

# add VFB iri
$(ONT).owl: $(ONT)-full.owl
	grep -v owl:versionIRI $< > $@.tmp.owl
	$(ROBOT) annotate -i $@.tmp.owl --ontology-iri http://virtualflybrain.org/data/VFB/OWL/VFB_scRNAseq.owl \
		convert -o $@.tmp.owl && mv $@.tmp.owl $@

$(REPORTDIR)/FBgn_list.txt: $(TMPDIR)/ontologyterms.txt
	grep -oE "FBgn[0-9]+" $< | sort | uniq > $@