--Query for scRNA-seq expression values.
--Max value of "spread" (aka extent) is 1.0 (i.e., all cells express the gene).
COPY (SELECT DISTINCT
    'FlyBase:'||l.uniquename as library_id,
    'FlyBase:'||f.uniquename as gene,
    expression_level.value as expression_level,
    expression_extent.value as expression_extent
FROM library l
JOIN library_cvterm lcvt ON lcvt.library_id = l.library_id
JOIN cvterm cvtt ON (cvtt.cvterm_id = lcvt.cvterm_id AND cvtt.name = 'transcriptional cell cluster')
JOIN library_feature lf ON lf.library_id = l.library_id
JOIN feature f ON f.feature_id = lf.feature_id
JOIN library_featureprop expression_level ON (expression_level.library_feature_id = lf.library_feature_id AND expression_level.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'mean_expr'))
JOIN library_featureprop expression_extent ON (expression_extent.library_feature_id = lf.library_feature_id AND expression_extent.type_id = (SELECT cvterm_id FROM cvterm WHERE name = 'spread'))
WHERE l.is_obsolete is false
  AND f.is_obsolete is false
  AND f.uniquename ~ '^FBgn[0-9]{7}$'
) TO STDOUT WITH DELIMITER E'\t' CSV HEADER;
