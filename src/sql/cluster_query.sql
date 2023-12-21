--Query for "Cluster" (aka "transcriptional cell cluster")
COPY (SELECT DISTINCT
--    'Cluster' as type,
    'FlyBase:'||l.uniquename as id,
    l.name as name,
    s.name as title,
    db_stage.name||':'||dbx_stage.accession as stage,
    'FlyBase:'||p.uniquename as associated_dataset,
    'FlyBase:'||r.uniquename as associated_clustering,
    db_cell_type.name||':'||dbx_cell_type.accession as cell_type,
    lp.value as cell_number
FROM library l
JOIN library_cvterm lcvt ON lcvt.library_id = l.library_id
JOIN cvterm cvtt ON (cvtt.cvterm_id = lcvt.cvterm_id AND cvtt.name = 'transcriptional cell cluster')
JOIN library_synonym ls ON (ls.library_id = l.library_id AND ls.is_current is true)
JOIN synonym s ON s.synonym_id = ls.synonym_id
JOIN cvterm cvts ON (cvts.cvterm_id = s.type_id AND cvts.name = 'fullname')
-- clustering
JOIN library_relationship lr1 ON (lr1.subject_id = l.library_id AND lr1.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'belongs_to'))
JOIN library r ON (r.library_id = lr1.object_id AND r.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'result'))
-- project
JOIN library_relationship lr2 ON (lr2.subject_id = r.library_id AND lr2.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'belongs_to'))
JOIN library p ON (p.library_id = lr2.object_id AND p.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'project'))
-- stage
LEFT OUTER JOIN library_cvterm lcvt1 ON (lcvt1.library_id = l.library_id AND lcvt1.cvterm_id in (SELECT DISTINCT cvterm_id FROM cvterm WHERE cv_id = (SELECT cv_id FROM cv WHERE name = 'FlyBase development CV')))
LEFT OUTER JOIN cvterm stage ON stage.cvterm_id = lcvt1.cvterm_id
LEFT OUTER JOIN library_cvtermprop lcvtp1 ON (lcvtp1.library_cvterm_id = lcvt1.library_cvterm_id AND lcvtp1.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'derived_stage'))
LEFT OUTER JOIN dbxref dbx_stage ON dbx_stage.dbxref_id = stage.dbxref_id
LEFT OUTER JOIN db db_stage ON db_stage.db_id = dbx_stage.db_id
LEFT OUTER JOIN library_expression le ON le.library_id = l.library_id
LEFT OUTER JOIN expression_cvterm ecvt ON (ecvt.expression_id = le.expression_id AND ecvt.cvterm_type_id = (SELECT cvterm_id FROM cvterm WHERE cv_id = (SELECT cv_id FROM cv WHERE name = 'expression slots') AND name = 'anatomy'))
LEFT OUTER JOIN cvterm cell_type ON cell_type.cvterm_id = ecvt.cvterm_id
LEFT OUTER JOIN dbxref dbx_cell_type ON dbx_cell_type.dbxref_id = cell_type.dbxref_id
LEFT OUTER JOIN db db_cell_type ON db_cell_type.db_id = dbx_cell_type.db_id
LEFT OUTER JOIN libraryprop lp ON (lp.library_id = l.library_id AND lp.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'number_in_collection'))
WHERE l.is_obsolete is false
) TO STDOUT WITH DELIMITER E'\t' CSV HEADER;
