

# Slot: publication


_Publication associated with the Dataset._



URI: [dcterms:references](http://purl.org/dc/terms/references)



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
| owl.fstring | AnnotationAssertion( dcterms:references {id} {V} ) |



### Schema Source


* from schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dcterms:references |
| native | http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq/:publication |




## LinkML Source

<details>
```yaml
name: publication
annotations:
  owl.fstring:
    tag: owl.fstring
    value: AnnotationAssertion( dcterms:references {id} {V} )
description: Publication associated with the Dataset.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: dcterms:references
alias: publication
owner: Dataset
domain_of:
- Dataset
range: Publication

```
</details>