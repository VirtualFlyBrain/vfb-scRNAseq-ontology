# get data from FlyBase
sh run.sh make get_FB_data -B

# update edit file
sh run.sh make update_ontology -B

# run release
sh run.sh make prepare_release -B
