# Class: Assay



URI: [FBcv:0003025](http://purl.obolibrary.org/obo/FBcv_0003025)




```mermaid
 classDiagram
    class Assay
      Class <|-- Assay
      
      Assay : associated_dataset
        
          Assay --|> Dataset : associated_dataset
        
      Assay : associated_sample_for_assay
        
          Assay --|> Sample : associated_sample_for_assay
        
      Assay : id
        
      Assay : method
        
          Assay --|> Thing : method
        
      Assay : name
        
      Assay : neo_label
        
      Assay : title
        
      
```





## Inheritance
* [Thing](Thing.md)
    * [Class](Class.md)
        * **Assay**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [associated_dataset](associated_dataset.md) | 0..1 <br/> [Dataset](Dataset.md) | Dataset (FBlc ID) that the Sample or Cluster belongs to | direct |
| [neo_label](neo_label.md) | 0..1 <br/> [String](String.md) | neo4j node label to add to entity | direct |
| [method](method.md) | 0..1 <br/> [Thing](Thing.md) | Method used for the assay - currently getting any direct subclass of FBcv:000... | direct |
| [associated_sample_for_assay](associated_sample_for_assay.md) | 0..* <br/> [Sample](Sample.md) | Input sample(s) for the scRNAseq assay | direct |
| [name](name.md) | 0..1 _recommended_ <br/> [String](String.md) | Short systematic label for the entity | [Class](Class.md) |
| [title](title.md) | 0..1 _recommended_ <br/> [String](String.md) | Short description of the entity | [Class](Class.md) |
| [id](id.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) | Identifier for the entity | [Thing](Thing.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Sample](Sample.md) | [associated_assay](associated_assay.md) | range | [Assay](Assay.md) |






## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl | NamedIndividual || owl.fstring | ClassAssertion( FBcv:0003025 {id} ) |



### Schema Source


* from schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | FBcv:0003025 |
| native | http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq/:Assay |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Assay
annotations:
  owl:
    tag: owl
    value: NamedIndividual
  owl.fstring:
    tag: owl.fstring
    value: ClassAssertion( FBcv:0003025 {id} )
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
is_a: Class
slots:
- associated_dataset
- neo_label
attributes:
  method:
    name: method
    annotations:
      owl:
        tag: owl
        value: ClassAssertion, ObjectSomeValuesFrom
    description: Method used for the assay - currently getting any direct subclass
      of FBcv:0009005 'single-cell library sequencing' for scRNAseq data.
    from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
    rank: 1000
    slot_uri: BAO:0000212
    multivalued: false
    range: Thing
  associated_sample_for_assay:
    name: associated_sample_for_assay
    annotations:
      owl:
        tag: owl
        value: ObjectPropertyAssertion
    description: Input sample(s) for the scRNAseq assay. Multiple IDs should be separated
      with '|' or in different rows.
    from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
    rank: 1000
    slot_uri: RO:0002233
    multivalued: true
    range: Sample
class_uri: FBcv:0003025

```
</details>

### Induced

<details>
```yaml
name: Assay
annotations:
  owl:
    tag: owl
    value: NamedIndividual
  owl.fstring:
    tag: owl.fstring
    value: ClassAssertion( FBcv:0003025 {id} )
from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
is_a: Class
attributes:
  method:
    name: method
    annotations:
      owl:
        tag: owl
        value: ClassAssertion, ObjectSomeValuesFrom
    description: Method used for the assay - currently getting any direct subclass
      of FBcv:0009005 'single-cell library sequencing' for scRNAseq data.
    from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
    rank: 1000
    slot_uri: BAO:0000212
    multivalued: false
    alias: method
    owner: Assay
    domain_of:
    - Assay
    range: Thing
  associated_sample_for_assay:
    name: associated_sample_for_assay
    annotations:
      owl:
        tag: owl
        value: ObjectPropertyAssertion
    description: Input sample(s) for the scRNAseq assay. Multiple IDs should be separated
      with '|' or in different rows.
    from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
    rank: 1000
    slot_uri: RO:0002233
    multivalued: true
    alias: associated_sample_for_assay
    owner: Assay
    domain_of:
    - Assay
    range: Sample
  associated_dataset:
    name: associated_dataset
    annotations:
      owl:
        tag: owl
        value: AnnotationProperty
    description: Dataset (FBlc ID) that the Sample or Cluster belongs to.
    from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
    rank: 1000
    slot_uri: dcterms:source
    alias: associated_dataset
    owner: Assay
    domain_of:
    - Sample
    - Assay
    - Clustering
    - Cluster
    range: Dataset
  neo_label:
    name: neo_label
    annotations:
      owl:
        tag: owl
        value: AnnotationProperty
    description: neo4j node label to add to entity.
    from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
    rank: 1000
    slot_uri: neo_property:nodeLabel
    alias: neo_label
    owner: Assay
    domain_of:
    - Dataset
    - Sample
    - Assay
    - Cluster
    - Publication
    range: string
  name:
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
    owner: Assay
    domain_of:
    - Class
    range: string
    recommended: true
  title:
    name: title
    annotations:
      owl:
        tag: owl
        value: AnnotationAssertion
    description: Short description of the entity.
    from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
    rank: 1000
    slot_uri: IAO:0000115
    alias: title
    owner: Assay
    domain_of:
    - Class
    range: string
    recommended: true
  id:
    name: id
    description: Identifier for the entity. FlyBase identifiers should be prefixed
      with 'FlyBase:'.
    from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
    rank: 1000
    identifier: true
    alias: id
    owner: Assay
    domain_of:
    - Thing
    range: uriorcurie
    required: true
class_uri: FBcv:0003025

```
</details>