

# Slot: total_gene_count


_Total number of distinct genes associated with the entity before filtering by extent._



URI: [neo_custom:total_gene_count](http://n2o.neo/custom/total_gene_count)



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
| self | neo_custom:total_gene_count |
| native | http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq/:total_gene_count |




## LinkML Source

<details>
```yaml
name: total_gene_count
annotations:
  owl:
    tag: owl
    value: AnnotationProperty
description: Total number of distinct genes associated with the entity before filtering
  by extent.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: neo_custom:total_gene_count
alias: total_gene_count
domain_of:
- Dataset
- Cluster
range: integer

```
</details>