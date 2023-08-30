--Query for "Dataset" (aka "project")
--Pulls projects derived associations with scRNA-seq assay terms.
COPY (
SELECT
--  project.type, 
  project.id,
  project.name,
  project.title,
  project.publication,
  project.assay_type,
  xrefs.accession AS accession,
  xrefs.name AS site_label,
  source.value AS source_linkout
FROM (
  SELECT DISTINCT
--    'Dataset' as type,
    'FlyBase:'||l.uniquename as id,
    l.name as name,
    s.name as title,
    'FlyBase:'||p.uniquename as publication,
    db.name||':'||dbx.accession as assay_type,
    l.library_id,
    lr.object_id
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
  LEFT JOIN library_relationship lr ON l.library_id=lr.subject_id
  WHERE l.is_obsolete is false) AS project
LEFT JOIN (
  SELECT 
    l.uniquename,
    l.library_id
  FROM library l) AS superproject
ON project.object_id=superproject.library_id
LEFT JOIN (
  SELECT 
    ld.library_id, 
    dx.accession, 
    db.name
  FROM library_dbxref ld
  JOIN dbxref dx
  ON ld.dbxref_id=dx.dbxref_id
  JOIN db
  ON dx.db_id=db.db_id
  WHERE db.name!='FlyBase') AS xrefs
ON (xrefs.library_id=project.library_id OR xrefs.library_id=superproject.library_id)
LEFT JOIN (
  SELECT
    lp.library_id,
    lp.value
  FROM libraryprop lp
  JOIN cvterm cv
  ON lp.type_id=cv.cvterm_id
  WHERE cv.name='owner'
) AS source
ON (project.library_id=source.library_id OR superproject.library_id=source.library_id)
) TO STDOUT WITH DELIMITER E'\t' CSV HEADER;
