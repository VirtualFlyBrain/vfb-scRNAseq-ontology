# Slot: cell_type


_Anatomy (FBbt IDs) for the Cluster. Multiple IDs should be separated with '|'._



URI: [RO:0002473](http://purl.obolibrary.org/obo/RO_0002473)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[Cluster](Cluster.md) |  |  no  |







## Properties

* Range: [Thing](Thing.md)

* Multivalued: True





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
name: cell_type
annotations:
  owl:
    tag: owl
    value: ClassAssertion, ObjectSomeValuesFrom
description: Anatomy (FBbt IDs) for the Cluster. Multiple IDs should be separated
  with '|'.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: RO:0002473
multivalued: true
alias: cell_type
owner: Cluster
domain_of:
- Cluster
range: Thing

```
</details>