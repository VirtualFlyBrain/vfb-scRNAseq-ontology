# Slot: associated_dataset


_Dataset (FBlc ID) that the Sample or Cluster belongs to._



URI: [dcterms:source](http://purl.org/dc/terms/source)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[Sample](Sample.md) |  |  no  |
[Assay](Assay.md) |  |  no  |
[Clustering](Clustering.md) |  |  no  |
[Cluster](Cluster.md) |  |  no  |







## Properties

* Range: [Dataset](Dataset.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl | AnnotationProperty |



### Schema Source


* from schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq




## LinkML Source

<details>
```yaml
name: associated_dataset
annotations:
  owl:
    tag: owl
    value: AnnotationProperty
description: Dataset (FBlc ID) that the Sample or Cluster belongs to.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: dcterms:source
alias: associated_dataset
domain_of:
- Sample
- Assay
- Clustering
- Cluster
range: Dataset

```
</details>