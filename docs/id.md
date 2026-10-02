

# Slot: id 


_Identifier for the entity. FlyBase identifiers should be prefixed with 'FlyBase:'._





URI: [http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq/id](http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq/id)
Alias: id

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Cluster](Cluster.md) |  |  no  |
| [Assay](Assay.md) |  |  no  |
| [Dataset](Dataset.md) |  |  no  |
| [Clustering](Clustering.md) |  |  no  |
| [Publication](Publication.md) |  |  no  |
| [Sample](Sample.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [Thing](Thing.md) |  |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Uriorcurie](Uriorcurie.md) |
| Domain Of | [Thing](Thing.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Identifier | Yes |












## Identifier and Mapping Information





### Schema Source


* from schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq/id |
| native | http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq/id |




## LinkML Source

<details>
```yaml
name: id
description: Identifier for the entity. FlyBase identifiers should be prefixed with
  'FlyBase:'.
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
rank: 1000
identifier: true
alias: id
domain_of:
- Thing
range: uriorcurie
required: true

```
</details>