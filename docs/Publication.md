

# Slot: publication


_Publication associated with the Dataset._





URI: [dc:references](http://purl.org/dc/terms/references)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Dataset](Dataset.md) |  |  no  |







## Properties

* Range: [Publication](Publication.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | AnnotationAssertion( dc:references {id} {V} ) |



### Schema Source


* from schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dc:references |
| native | http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq/:publication |




## LinkML Source

<details>
```yaml
name: publication
annotations:
  owl.fstring:
    tag: owl.fstring
    value: AnnotationAssertion( dc:references {id} {V} )
description: Publication associated with the Dataset.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: dc:references
alias: publication
owner: Dataset
domain_of:
- Dataset
range: Publication

```
</details>