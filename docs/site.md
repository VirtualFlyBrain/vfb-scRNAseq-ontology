# Slot: site


_VFB site node curie. The site must be created in VFB and added to the dictionary in ../scripts/process_site_data.py to successfully map from FB data._



URI: [oboInOwl:hasDbXref](http://www.geneontology.org/formats/oboInOwl#hasDbXref)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[Dataset](Dataset.md) |  |  no  |







## Properties

* Range: [Thing](Thing.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl | AnnotationProperty || owl.axiom_annotation.slots | accession |



### Schema Source


* from schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq




## LinkML Source

<details>
```yaml
name: site
annotations:
  owl:
    tag: owl
    value: AnnotationProperty
  owl.axiom_annotation.slots:
    tag: owl.axiom_annotation.slots
    value: accession
description: VFB site node curie. The site must be created in VFB and added to the
  dictionary in ../scripts/process_site_data.py to successfully map from FB data.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: oboInOwl:hasDbXref
alias: site
owner: Dataset
domain_of:
- Dataset
range: Thing

```
</details>