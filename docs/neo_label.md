# Slot: neo_label


_neo4j node label to add to entity._



URI: [neo_property:nodeLabel](http://n2o.neo/property/nodeLabel)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[Dataset](Dataset.md) |  |  no  |
[Sample](Sample.md) |  |  no  |
[Assay](Assay.md) |  |  no  |
[Cluster](Cluster.md) |  |  no  |
[Publication](Publication.md) |  |  no  |







## Properties

* Range: [String](String.md)





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
name: neo_label
annotations:
  owl:
    tag: owl
    value: AnnotationProperty
description: neo4j node label to add to entity.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: neo_property:nodeLabel
alias: neo_label
domain_of:
- Dataset
- Sample
- Assay
- Cluster
- Publication
range: string

```
</details>