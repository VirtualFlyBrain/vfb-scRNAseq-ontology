

# Slot: name


_Short systematic label for the entity._



URI: [rdfs:label](http://www.w3.org/2000/01/rdf-schema#label)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Assay](Assay.md) |  |  no  |
| [Cluster](Cluster.md) |  |  no  |
| [Clustering](Clustering.md) |  |  no  |
| [Sample](Sample.md) |  |  no  |
| [Dataset](Dataset.md) |  |  no  |
| [Class](Class.md) |  |  no  |







## Properties

* Range: [String](String.md)

* Recommended: True





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl | AnnotationAssertion |



### Schema Source


* from schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq




## LinkML Source

<details>
```yaml
name: name
annotations:
  owl:
    tag: owl
    value: AnnotationAssertion
description: Short systematic label for the entity.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
slot_uri: rdfs:label
alias: name
domain_of:
- Class
range: string
recommended: true

```
</details>