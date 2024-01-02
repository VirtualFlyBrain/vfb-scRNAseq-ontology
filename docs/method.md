# Slot: method


_Method used for the assay - currently getting any direct subclass of FBcv:0009005 'single-cell library sequencing' for scRNAseq data._



URI: [BAO:0000212](http://www.bioassayontology.org/bao#BAO_0000212)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[Assay](Assay.md) |  |  no  |







## Properties

* Range: [Thing](Thing.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | ClassAssertion( ObjectSomeValuesFrom( BAO:0000212 {V} ) {id} ) |



### Schema Source


* from schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq




## LinkML Source

<details>
```yaml
name: method
annotations:
  owl.fstring:
    tag: owl.fstring
    value: ClassAssertion( ObjectSomeValuesFrom( BAO:0000212 {V} ) {id} )
description: Method used for the assay - currently getting any direct subclass of
  FBcv:0009005 'single-cell library sequencing' for scRNAseq data.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: BAO:0000212
multivalued: false
alias: method
owner: Assay
domain_of:
- Assay
range: Thing

```
</details>