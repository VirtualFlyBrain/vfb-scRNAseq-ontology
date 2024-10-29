import glob
ontology_lines = []
ontology_file = 'VFB_scRNAseq-edit.ofn'

ontology_lines.extend([
'Prefix(:=<http://virtualflybrain.org/data/VFB/OWL/VFB_scRNAseq.owl#>)',
'Prefix(owl:=<http://www.w3.org/2002/07/owl#>)',
'Prefix(rdf:=<http://www.w3.org/1999/02/22-rdf-syntax-ns#>)',
'Prefix(xml:=<http://www.w3.org/XML/1998/namespace>)',
'Prefix(xsd:=<http://www.w3.org/2001/XMLSchema#>)',
'Prefix(rdfs:=<http://www.w3.org/2000/01/rdf-schema#>)',
'',
'',
'Ontology(<http://virtualflybrain.org/data/VFB/OWL/VFB_scRNAseq.owl>',
'Import(<http://purl.obolibrary.org/obo/VFB_scRNAseq/imports/merged_import.owl>)',
])

import_files = glob.glob('ontology_files/*.owl')
import_statements = ['Import(<http://virtualflybrain.org/data/VFB/OWL/%s>)' % o.replace('ontology_files/', '') for o in import_files]

ontology_lines.extend(import_statements)

ontology_lines.extend([
'Annotation(<http://purl.org/dc/terms/description> "An ontology of Drosophila melanogaster scRNAseq data. This information is taken from FlyBase, which sources it from the EMBL-EBI Single Cell Expression Atlas, which compiles scRNAseq data from multiple sources."^^xsd:string)',
'Annotation(<http://purl.org/dc/terms/title> "VFB scRNAseq Ontology"^^xsd:string)',
'Annotation(<http://purl.org/dc/terms/license> <https://creativecommons.org/licenses/by/4.0/>)',
'',
'Declaration(AnnotationProperty(<http://purl.org/dc/terms/description>))',
'Declaration(AnnotationProperty(<http://purl.org/dc/terms/title>))',
'Declaration(AnnotationProperty(<http://purl.org/dc/terms/license>))',
')'
])

with open(ontology_file, 'w') as file:
    file.write('\n'.join(ontology_lines) + '\n')
