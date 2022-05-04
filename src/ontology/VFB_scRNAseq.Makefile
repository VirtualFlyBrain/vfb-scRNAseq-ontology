## Customize Makefile settings for VFB_scRNAseq
##
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

# additionally remove _terms_combined files
.PHONY: prepare_release
prepare_release: all
	rsync -R $(RELEASE_ASSETS) $(RELEASEDIR) &&\
  rm -f $(CLEANFILES) &&\
	rm -f $(IMPORTDIR)/*_terms_combined.txt &&\
  echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on your git hosting site such as GitHub or GitLab"

EXPDIR = expression_data
LINKML = linkml-data2owl -s VFB_scRNAseq_schema.yaml
EXPRESSION_TSVS = $(wildcard $(EXPDIR)/*.tsv)
EXPRESSION_OFNS = $(EXPRESSION_TSVS:.tsv=.ofn)


.PHONY: get_FB_data
get_FB_data: $(EXPDIR)
	# clear any existing cluster expression files
	rm -f $(EXPDIR)/*.tsv $(EXPDIR)/*.ofn
	# get scRNAseq data from public chado
	apt-get -y install postgresql-client
	psql -h chado.flybase.org -U flybase flybase -f ../sql/dataset_query.sql \
	| sed '1 s/type/@type/' > $(TMPDIR)/dataset_data.tsv
	psql -h chado.flybase.org -U flybase flybase -f ../sql/sample_query.sql \
	| sed '1 s/type/@type/' > $(TMPDIR)/sample_data.tsv
	psql -h chado.flybase.org -U flybase flybase -f ../sql/cluster_query.sql \
	| sed '1 s/type/@type/' > $(TMPDIR)/cluster_data.tsv
	psql -h chado.flybase.org -U flybase flybase -f ../sql/expression_query.sql \
	| sed '1 s/type/@type/' > $(TMPDIR)/expression_data.tsv
	# split expression data into tsvs for each cluster and filter by extent
	python3 $(SCRIPTSDIR)/expression_by_cluster.py

.DEFAULT:
	echo $@
	# Empty recipe for anything that doesn't have a recipe
	# Stops make complaining that no recipe exists for tsvs

.PHONY: install_linkml
install_linkml:
	python3 -m pip install linkml-owl

$(EXPDIR):
	mkdir -p $@

$(EXPDIR)/%.ofn: $(EXPDIR)/%.tsv | $(EXPDIR) install_linkml
	$(LINKML) $< -o $@

.PHONY: update_ontology
update_ontology: get_FB_data $(EXPRESSION_OFNS) install_linkml $(COMPONENTSDIR)
	$(LINKML) $(TMPDIR)/dataset_data.tsv -o $(TMPDIR)/dataset_data.ofn &&\
	$(LINKML) $(TMPDIR)/sample_data.tsv -o $(TMPDIR)/sample_data.ofn &&\
	$(LINKML) $(TMPDIR)/cluster_data.tsv -o $(TMPDIR)/cluster_data.ofn &&\
	$(ROBOT) merge \
	--input VFB_scRNAseq-annotations.ofn \
	--input $(TMPDIR)/dataset_data.ofn \
	--input $(TMPDIR)/sample_data.ofn \
	--input $(TMPDIR)/cluster_data.ofn \
	--include-annotations true --collapse-import-closure false \
	convert --format ofn \
	-o VFB_scRNAseq-edit.owl \
	# Make expression import
	$(ROBOT) merge --inputs "$(EXPDIR)/*.ofn" \
	annotate --ontology-iri "http://purl.obolibrary.org/obo/VFB_scRNAseq/components/expression_data.owl" \
	convert --format ofn -o $(COMPONENTSDIR)/expression_data.owl &&\
	echo "\nOntology source file updated!\n"

# add VFB iri
$(ONT).owl: $(ONT)-full.owl
	grep -v owl:versionIRI $< > $@.tmp.owl
	$(ROBOT) annotate -i $@.tmp.owl --ontology-iri http://virtualflybrain.org/data/VFB/OWL/vfb_scRNAseq.owl \
		convert -o $@.tmp.owl && mv $@.tmp.owl $@
