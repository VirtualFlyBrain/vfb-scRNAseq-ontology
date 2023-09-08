# Slot: gene


_A gene (FBgn ID) expressed by the Cluster. Max one gene per tsv row alongside its expression_extent and expression_level._



URI: [RO:0002292](http://purl.obolibrary.org/obo/RO_0002292)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[Cluster](Cluster.md) |  |  no  |







## Properties

* Range: [Thing](Thing.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl | ClassAssertion, ObjectSomeValuesFrom || owl.fstring | ClassAssertion ( Annotation ( neo_custom:hide_in_terminfo {hide_in_terminfo} ) Annotation ( neo_custom:expression_level {expression_level} ) Annotation ( neo_custom:expression_extent {expression_extent} ) ObjectSomeValuesFrom ( RO:0002292 {V}) {id}) |



### Schema Source


* from schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq




## LinkML Source

<details>
```yaml
name: gene
annotations:
  owl:
    tag: owl
    value: ClassAssertion, ObjectSomeValuesFrom
  owl.fstring:
    tag: owl.fstring
    value: ClassAssertion ( Annotation ( neo_custom:hide_in_terminfo {hide_in_terminfo}
      ) Annotation ( neo_custom:expression_level {expression_level} ) Annotation (
      neo_custom:expression_extent {expression_extent} ) ObjectSomeValuesFrom ( RO:0002292
      {V}) {id})
description: A gene (FBgn ID) expressed by the Cluster. Max one gene per tsv row alongside
  its expression_extent and expression_level.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: RO:0002292
alias: gene
owner: Cluster
domain_of:
- Cluster
range: Thing

```
</details>