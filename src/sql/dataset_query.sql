--Query for "Dataset" (aka "project")
--Pulls projects derived associations with scRNA-seq assay terms.
COPY (SELECT DISTINCT
    'Dataset' as type,
    'FlyBase:'||l.uniquename as id,
    l.name as name,
    s.name as title,
    'FlyBase:'||p.uniquename as publication,
    db.name||':'||dbx.accession as assay_type
FROM library l
JOIN cvterm t ON (t.cvterm_id = l.type_id AND t.name = 'project')
JOIN library_cvterm lcvt ON lcvt.library_id = l.library_id
JOIN cvterm cvta ON (cvta.cvterm_id = lcvt.cvterm_id AND cvta.name in ('single-cell RNA-Seq', 'single-nucleus RNA-Seq'))
JOIN dbxref dbx ON dbx.dbxref_id = cvta.dbxref_id
JOIN db ON db.db_id = dbx.db_id
JOIN library_synonym ls ON (ls.library_id = l.library_id AND ls.is_current is true)
JOIN synonym s ON s.synonym_id = ls.synonym_id
JOIN cvterm cvts ON (cvts.cvterm_id = s.type_id AND cvts.name = 'fullname')
JOIN library_pub lp ON lp.library_id = l.library_id
JOIN pub p ON p.pub_id = lp.pub_id
WHERE l.is_obsolete is false
) TO STDOUT WITH DELIMITER E'\t' CSV HEADER;
