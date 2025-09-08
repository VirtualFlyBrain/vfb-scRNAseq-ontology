

# Slot: filtered_gene_count 


_Total number of distinct genes associated with the entity after filtering by extent._





URI: [neo_custom:filtered_gene_count](http://n2o.neo/custom/filtered_gene_count)
Alias: filtered_gene_count

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Dataset](Dataset.md) |  |  no  |
| [Cluster](Cluster.md) |  |  no  |







## Properties

* Range: [Integer](Integer.md)





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
| self | neo_custom:filtered_gene_count |
| native | http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq/filtered_gene_count |




## LinkML Source

<details>
```yaml
name: filtered_gene_count
annotations:
  owl:
    tag: owl
    value: AnnotationProperty
description: Total number of distinct genes associated with the entity after filtering
  by extent.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: neo_custom:filtered_gene_count
alias: filtered_gene_count
domain_of:
- Dataset
- Cluster
range: integer

```
</details>