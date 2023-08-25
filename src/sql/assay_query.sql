--Query for "Assay"
COPY (SELECT DISTINCT
    'Assay' as type,
    'FlyBase:'||l.uniquename as id,
    l.name as name,
    s.name as title,
    'FlyBase:'||p.uniquename as associated_dataset,
    'FlyBase:'||ca.uniquename as control_assay,
    methods.name||':'||methods.accession as method
FROM library l
JOIN cvterm t ON (t.cvterm_id = l.type_id AND t.name = 'assay')
JOIN library_cvterm lc ON lc.library_id = l.library_id
JOIN (SELECT cv1.cvterm_id, db1.name, dbx1.accession from cvterm_relationship cvr
  JOIN (SELECT ct.cvterm_id, ct.name from cvterm ct
    JOIN dbxref dbx ON dbx.dbxref_id = ct.dbxref_id
    JOIN db db ON db.db_id = dbx.db_id
    WHERE db.name = 'FBcv'
    AND dbx.accession in ('0009005')) FBcv_xrefs -- get cvterm_id for FBcv:0009005 ('single-cell library sequencing')
  ON cvr.object_id = FBcv_xrefs.cvterm_id
  JOIN cvterm cv1 ON cv1.cvterm_id = cvr.subject_id
  JOIN dbxref dbx1 ON dbx1.dbxref_id = cv1.dbxref_id
  JOIN db db1 ON db1.db_id = dbx1.db_id) methods -- subjects of direct relationships to FBcv:0009005 ('single-cell library sequencing')
ON methods.cvterm_id = lc.cvterm_id
JOIN library_relationship lr ON lr.subject_id = l.library_id
JOIN library p ON p.library_id = lr.object_id AND p.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'project')
JOIN cvterm lrt ON (lrt.cvterm_id = lr.type_id AND lrt.name = 'belongs_to')
JOIN library_cvterm lcvt ON lcvt.library_id = p.library_id
JOIN cvterm cvta ON (cvta.cvterm_id = lcvt.cvterm_id AND cvta.name in ('single-cell RNA-Seq', 'single-nucleus RNA-Seq'))
JOIN library_synonym ls ON (ls.library_id = l.library_id AND ls.is_current is true)
JOIN synonym s ON s.synonym_id = ls.synonym_id
JOIN cvterm cvts ON (cvts.cvterm_id = s.type_id AND cvts.name = 'fullname')
LEFT OUTER JOIN library_relationship lra ON (lra.subject_id = l.library_id AND lra.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'biological_reference_is'))
LEFT OUTER JOIN library ca ON lra.object_id=ca.library_id
WHERE l.is_obsolete is false
  AND p.is_obsolete is false
) TO STDOUT WITH DELIMITER E'\t' CSV HEADER;
