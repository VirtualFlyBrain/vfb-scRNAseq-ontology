# Slot: sex


_Sex for the entity. Should be 'male' or 'female'._



URI: [BFO:0000050](http://purl.obolibrary.org/obo/BFO_0000050)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[Sample](Sample.md) |  |  no  |
[Cluster](Cluster.md) |  |  no  |







## Properties

* Range: [SexOptions](SexOptions.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl | ClassAssertion, ObjectSomeValuesFrom |



### Schema Source


* from schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq




## LinkML Source

<details>
```yaml
name: sex
annotations:
  owl:
    tag: owl
    value: ClassAssertion, ObjectSomeValuesFrom
description: Sex for the entity. Should be 'male' or 'female'.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: BFO:0000050
alias: sex
domain_of:
- Sample
- Cluster
range: sex_options

```
</details>