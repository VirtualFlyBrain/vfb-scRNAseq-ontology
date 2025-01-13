

# Slot: stage


_Developmental stage (FBdv ID) of the Sample or Cluster._





URI: [RO:0002490](http://purl.obolibrary.org/obo/RO_0002490)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Cluster](Cluster.md) |  |  no  |
| [Sample](Sample.md) |  |  no  |







## Properties

* Range: [Thing](Thing.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | ClassAssertion( ObjectSomeValuesFrom( RO:0002490 {V} ) {id} ) |



### Schema Source


* from schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | RO:0002490 |
| native | http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq/:stage |




## LinkML Source

<details>
```yaml
name: stage
annotations:
  owl.fstring:
    tag: owl.fstring
    value: ClassAssertion( ObjectSomeValuesFrom( RO:0002490 {V} ) {id} )
description: Developmental stage (FBdv ID) of the Sample or Cluster.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: RO:0002490
alias: stage
domain_of:
- Sample
- Cluster
range: Thing

```
</details>