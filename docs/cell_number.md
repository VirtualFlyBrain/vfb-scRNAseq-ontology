

# Slot: cell_number


_The number of cells in the Cluster (as integer)._



URI: [neo_custom:cell_count](http://n2o.neo/custom/cell_count)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Cluster](Cluster.md) |  |  no  |







## Properties

* Range: [Integer](Integer.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | AnnotationAssertion( neo_custom:cell_count {id} {cell_number} ) |



### Schema Source


* from schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq




## LinkML Source

<details>
```yaml
name: cell_number
annotations:
  owl.fstring:
    tag: owl.fstring
    value: AnnotationAssertion( neo_custom:cell_count {id} {cell_number} )
description: The number of cells in the Cluster (as integer).
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: neo_custom:cell_count
alias: cell_number
owner: Cluster
domain_of:
- Cluster
range: integer

```
</details>