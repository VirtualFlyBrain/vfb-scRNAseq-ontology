--Query for "Clustering" (aka "cell clustering analysis")
COPY (SELECT DISTINCT
--    'Clustering' as type,
    'FlyBase:'||l.uniquename as id,
    l.name as name,
    s.name as title,
    'FlyBase:'||p.uniquename as associated_dataset,
    'FlyBase:'||bs.uniquename as associated_sample
FROM library l
JOIN library_cvterm lcvt ON lcvt.library_id = l.library_id
JOIN cvterm cvt ON (cvt.cvterm_id = lcvt.cvterm_id AND cvt.name = 'cell clustering analysis')
JOIN library_synonym ls ON (ls.library_id = l.library_id AND ls.is_current is true)
JOIN synonym s ON s.synonym_id = ls.synonym_id
JOIN cvterm cvts ON (cvts.cvterm_id = s.type_id AND cvts.name = 'fullname')
JOIN library_relationship lr ON (lr.subject_id = l.library_id AND lr.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'belongs_to'))
JOIN library p ON (p.library_id = lr.object_id AND p.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'project'))
JOIN library_relationship lr2 ON (lr2.subject_id = l.library_id AND lr2.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'derived_analysis_of'))
JOIN library bs ON (bs.library_id = lr2.object_id AND bs.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'biosample'))
WHERE l.is_obsolete is false
) TO STDOUT WITH DELIMITER E'\t' CSV HEADER;
