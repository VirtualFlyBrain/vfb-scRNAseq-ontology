## Customize Makefile settings for VFB_scRNAseq
##
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

.PHONY: prepare_release
prepare_release: all $(REPORTDIR)/FBgn_list.txt
	rsync -R $(RELEASE_ASSETS) $(RELEASEDIR) &&\
  rm -f $(CLEANFILES) &&\
	rm -f $(IMPORTDIR)/*_terms_combined.txt &&\
  echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on your git hosting site such as GitHub or GitLab"

EXPDIR = expression_data
LINKML = linkml-data2owl -s VFB_scRNAseq_schema.yaml
NEW_EXPRESSION_TSVS = $(wildcard $(EXPDIR)/*.tsv)
NEW_EXPRESSION_OFNS = $(NEW_EXPRESSION_TSVS:.tsv=.ofn)


.PHONY: get_FB_data
get_FB_data: $(EXPDIR) $(TMPDIR)/existing_clusters.txt
	apt-get update
	apt-get -y install postgresql-client
	psql -h chado.flybase.org -U flybase flybase -f ../sql/dataset_query.sql \
	| sed '1 s/type/@type/' > $(TMPDIR)/raw_dataset_data.tsv
	psql -h chado.flybase.org -U flybase flybase -f ../sql/sample_query.sql \
	| sed '1 s/type/@type/' > $(TMPDIR)/raw_sample_data.tsv
	psql -h chado.flybase.org -U flybase flybase -f ../sql/cluster_query.sql \
	| sed '1 s/type/@type/' > $(TMPDIR)/raw_cluster_data.tsv
	psql -h chado.flybase.org -U flybase flybase -f ../sql/expression_query.sql \
	| sed '1 s/type/@type/' > $(TMPDIR)/raw_expression_data.tsv

.PHONY: process_FB_data
process_FB_data: get_FB_data
	# split expression data into tsvs for new clusters and filter by extent
	python3 $(SCRIPTSDIR)/process_expression_data.py
	python3 $(SCRIPTSDIR)/process_site_data.py

.DEFAULT:
	echo $@
	# Default recipe for anything that doesn't have a recipe
	# Stops make complaining that no recipe exists for tsvs

.PHONY: install_linkml
install_linkml:
	python3 -m pip install linkml-owl

$(EXPDIR):
	mkdir -p $@

$(TMPDIR)/existing_clusters.txt:
	$(ROBOT) query --input $(SRC) \
  --query ../sparql/existing_clusters.sparql $(TMPDIR)/existing_clusters.csv &&\
	grep -oE 'FBlc[0-9]+' $(TMPDIR)/existing_clusters.csv > $@ &&\
	rm $(TMPDIR)/existing_clusters.csv

$(EXPDIR)/%.ofn: $(EXPDIR)/%.tsv | $(EXPDIR) install_linkml
	$(LINKML) $< -o $@ && rm $<

.PHONY: update_ontology
update_ontology: install_linkml process_FB_data $(NEW_EXPRESSION_OFNS) $(COMPONENTSDIR)
	$(LINKML) $(TMPDIR)/dataset_data.tsv -o $(TMPDIR)/dataset_data.ofn &&\
	$(LINKML) $(TMPDIR)/sample_data.tsv -o $(TMPDIR)/sample_data.ofn &&\
	$(LINKML) $(TMPDIR)/new_cluster_data.tsv -o $(TMPDIR)/new_cluster_data.ofn &&\
	$(ROBOT) merge \
	--input cluster_data.ofn \
	--input $(TMPDIR)/new_cluster_data.ofn \
	convert --format ofn \
	-o cluster_data.ofn &&\
	$(ROBOT) merge \
	--input VFB_scRNAseq-annotations.ofn \
	--input $(TMPDIR)/dataset_data.ofn \
	--input $(TMPDIR)/sample_data.ofn \
	--input cluster_data.ofn \
	--include-annotations true --collapse-import-closure false \
	convert --format ofn \
	-o $(SRC)
	# Make expression import
	$(ROBOT) merge --input $(COMPONENTSDIR)/expression_data.owl --inputs "$(EXPDIR)/*.ofn" \
	annotate --ontology-iri "http://purl.obolibrary.org/obo/VFB_scRNAseq/components/expression_data.owl" \
	convert --format ofn -o $(COMPONENTSDIR)/expression_data.owl &&\
	gzip -c $(COMPONENTSDIR)/expression_data.owl > $(COMPONENTSDIR)/expression_data.owl.gz &&\
	echo "\nOntology source file updated!\n"

# add VFB iri
$(ONT).owl: $(ONT)-full.owl
	grep -v owl:versionIRI $< > $@.tmp.owl
	$(ROBOT) annotate -i $@.tmp.owl --ontology-iri http://virtualflybrain.org/data/VFB/OWL/vfb_scRNAseq.owl \
		convert -o $@.tmp.owl && mv $@.tmp.owl $@

$(REPORTDIR)/FBgn_list.txt: $(TMPDIR)/ontologyterms.txt
	grep -oE "FBgn[0-9]+" $< | sort | uniq > $@