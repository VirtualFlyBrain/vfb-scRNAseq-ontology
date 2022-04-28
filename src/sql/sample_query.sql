--Query for "Sample" (aka "biosample")
--Note - If many tissues or stages are associated with a sample, this query returns one line for each distinct tissue/sex/stage term combination.
--Note - Should still return a sample if tissue, sex or stage are missing (with NULL value for that field).
COPY (SELECT DISTINCT
    'Sample' as type,
    'FlyBase:'||l.uniquename as library_id,
    l.name as library_name,
    s.name as library_title,
    tissue.name as tissue,
    db_tissue.name||':'||dbx_tissue.accession as sample_tissue_id,
    sex.name as sex,
    stage.name as stage,
    db_stage.name||':'||dbx_stage.accession as sample_stage_id,
    'FlyBase:'||p.uniquename as associated_dataset
FROM library l
JOIN cvterm t ON (t.cvterm_id = l.type_id AND t.name = 'biosample')
JOIN library_relationship lr ON lr.subject_id = l.library_id
JOIN library p ON p.library_id = lr.object_id AND p.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'project')
JOIN cvterm lrt ON (lrt.cvterm_id = lr.type_id AND lrt.name = 'belongs_to')
JOIN library_cvterm lcvt ON lcvt.library_id = p.library_id
JOIN cvterm cvta ON (cvta.cvterm_id = lcvt.cvterm_id AND cvta.name in ('single-cell RNA-Seq', 'single-nucleus RNA-Seq'))
JOIN library_synonym ls ON (ls.library_id = l.library_id AND ls.is_current is true)
JOIN synonym s ON s.synonym_id = ls.synonym_id
JOIN cvterm cvts ON (cvts.cvterm_id = s.type_id AND cvts.name = 'fullname')
JOIN library_expression le ON le.library_id = l.library_id
LEFT OUTER JOIN expression_cvterm ecvt_tissue ON (ecvt_tissue.expression_id = le.expression_id AND ecvt_tissue.cvterm_type_id = (SELECT cvterm_id FROM cvterm WHERE cv_id = (SELECT cv_id FROM cv WHERE name = 'expression slots') AND name = 'anatomy'))
LEFT OUTER JOIN cvterm tissue ON tissue.cvterm_id = ecvt_tissue.cvterm_id
LEFT OUTER JOIN dbxref dbx_tissue ON dbx_tissue.dbxref_id = tissue.dbxref_id
LEFT OUTER JOIN db db_tissue ON db_tissue.db_id = dbx_tissue.db_id
LEFT OUTER JOIN expression_cvterm ecvt_stage ON (ecvt_stage.expression_id = le.expression_id AND ecvt_stage.cvterm_type_id = (SELECT cvterm_id FROM cvterm WHERE cv_id = (SELECT cv_id FROM cv WHERE name = 'expression slots') AND name = 'stage') AND NOT ecvt_stage.cvterm_id in (SELECT DISTINCT cvterm_id FROM cvterm WHERE cv_id = (SELECT cv_id FROM cv WHERE name = 'FlyBase miscellaneous CV') AND name LIKE '%male'))
LEFT OUTER JOIN cvterm stage ON stage.cvterm_id = ecvt_stage.cvterm_id
LEFT OUTER JOIN dbxref dbx_stage ON dbx_stage.dbxref_id = stage.dbxref_id
LEFT OUTER JOIN db db_stage ON db_stage.db_id = dbx_stage.db_id
LEFT OUTER JOIN expression_cvterm ecvt_sex ON (ecvt_sex.expression_id = le.expression_id AND ecvt_sex.cvterm_type_id = (SELECT cvterm_id FROM cvterm WHERE cv_id = (SELECT cv_id FROM cv WHERE name = 'expression slots') AND name = 'stage') AND ecvt_sex.cvterm_id in (SELECT DISTINCT cvterm_id FROM cvterm WHERE cv_id = (SELECT cv_id FROM cv WHERE name = 'FlyBase miscellaneous CV') AND name LIKE '%male'))
LEFT OUTER JOIN cvterm sex ON sex.cvterm_id = ecvt_sex.cvterm_id
WHERE l.is_obsolete is false
  AND p.is_obsolete is false
) TO STDOUT WITH DELIMITER E'\t' CSV HEADER;
