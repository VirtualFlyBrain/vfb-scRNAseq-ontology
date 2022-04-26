## Customize Makefile settings for VFB_scRNAseq
##
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

# additionally remove _terms_combined files
.PHONY: prepare_release
prepare_release: all
	rsync -R $(RELEASE_ASSETS) $(RELEASEDIR) &&\
  rm -f $(CLEANFILES) &&\
	rm -f imports/*_terms_combined.txt &&\
  echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on your git hosting site such as GitHub or GitLab"

.PHONY: update_ontology
update_ontology:
	python3 -m pip install linkml-owl &&\
	linkml-data2owl -s VFB_scRNAseq_schema.yaml tmp/scRNAseq_data.tsv -o tmp/scRNAseq_data.ofn  &&\
	$(ROBOT) convert --format ofn -i tmp/scRNAseq_data.ofn \
	-o VFB_scRNAseq-edit.owl &&\
	$(ROBOT) merge --input VFB_scRNAseq-annotations.ofn --input tmp/scRNAseq_data.ofn \
	--include-annotations true --collapse-import-closure false \
	convert --format ofn \
	-o VFB_scRNAseq-edit.owl &&\
	echo "\nOntology source file updated!\n"

# add VFB iri
$(ONT).owl: $(ONT)-full.owl
	grep -v owl:versionIRI $< > $@.tmp.owl
	$(ROBOT) annotate -i $@.tmp.owl --ontology-iri http://virtualflybrain.org/data/VFB/OWL/vfb_scRNAseq.owl \
		convert -o $@.tmp.owl && mv $@.tmp.owl $@
