with open("tmp/existing_FBgns.txt", 'r') as file:
    id_list = [line.rstrip() for line in file]

#This method is not going to work until https://flybase.github.io/docs/chado/functions#update_ids is fixed
query_file = '../sql/id_update_query.sql'

query = ("COPY (SELECT DISTINCT * FROM "
         "flybase.update_ids(ARRAY[\"%s\"])) "
         "TO STDOUT WITH DELIMITER E'\\t' CSV HEADER;"
         % '\",\"'.join(id_list))

with open(query_file, 'w') as file:
    file.write(query)