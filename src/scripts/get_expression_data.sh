#!/usr/bin/env bash
# Runs expression_query.sql in batches of clusters, as chado's proxy kills queries after 2 min.
# Usage: get_expression_data.sh <cluster_tsv> <output_tsv> [batch_size]
# Cluster ids are taken from the first column of cluster_tsv (output of cluster_query.sql).
set -euo pipefail

CLUSTER_FILE=$1
OUTPUT_FILE=$2
BATCH_SIZE=${3:-200}
SQL_FILE="$(dirname "$0")/../sql/expression_query.sql"
FB_PSQL="psql -v ON_ERROR_STOP=1 -h chado.flybase.org -U flybase flybase"

BATCH_DIR=$(mktemp -d)
trap 'rm -rf "$BATCH_DIR"' EXIT

# one quoted, comma-separated id list per line
tail -n +2 "$CLUSTER_FILE" | cut -f1 | sed 's/^FlyBase://' | sort -u \
 | awk -v n="$BATCH_SIZE" '{printf "%s'\''%s'\''", ((NR-1)%n ? "," : ""), $0} NR%n==0 {print ""} END {if (NR%n) print ""}' \
 > "$BATCH_DIR/batches.txt"

N_BATCHES=$(wc -l < "$BATCH_DIR/batches.txt" | tr -d " ")
i=0
while read -r IDS; do
	i=$((i+1))
	echo "Expression query batch $i/$N_BATCHES"
	$FB_PSQL -v cluster_ids="$IDS" -f "$SQL_FILE" > "$BATCH_DIR/batch_$i.tsv"
done < "$BATCH_DIR/batches.txt"

# keep header from first batch only
head -1 "$BATCH_DIR/batch_1.tsv" > "$OUTPUT_FILE"
for j in $(seq "$N_BATCHES"); do
	tail -n +2 "$BATCH_DIR/batch_$j.tsv" >> "$OUTPUT_FILE"
done
