# Slot: sample_tissue


_Tissue(s) (FBbt IDs) in the sample. Multiple IDs should be separated with '|' or in different rows. Maps as an overlaps relationship rather than part_of due to imprecision of dissection._



URI: [RO:0002131](http://purl.obolibrary.org/obo/RO_0002131)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[Sample](Sample.md) |  |  no  |







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
name: sample_tissue
annotations:
  owl:
    tag: owl
    value: ClassAssertion, ObjectSomeValuesFrom
description: Tissue(s) (FBbt IDs) in the sample. Multiple IDs should be separated
  with '|' or in different rows. Maps as an overlaps relationship rather than part_of
  due to imprecision of dissection.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: RO:0002131
multivalued: true
alias: sample_tissue
owner: Sample
domain_of:
- Sample
range: Thing

```
</details>