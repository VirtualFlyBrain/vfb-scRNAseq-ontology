

# Slot: neo_label 


_neo4j node label to add to entity._





URI: [neo_property:nodeLabel](http://n2o.neo/property/nodeLabel)
Alias: neo_label

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Sample](Sample.md) |  |  no  |
| [Cluster](Cluster.md) |  |  no  |
| [Assay](Assay.md) |  |  no  |
| [Dataset](Dataset.md) |  |  no  |
| [Publication](Publication.md) |  |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [Dataset](Dataset.md), [Sample](Sample.md), [Assay](Assay.md), [Cluster](Cluster.md), [Publication](Publication.md) |
| Slot URI | [neo_property:nodeLabel](http://n2o.neo/property/nodeLabel) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information



### Annotations

| property | value |
| --- | --- |
| owl | AnnotationProperty |




### Schema Source


* from schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | neo_property:nodeLabel |
| native | http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq/neo_label |




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