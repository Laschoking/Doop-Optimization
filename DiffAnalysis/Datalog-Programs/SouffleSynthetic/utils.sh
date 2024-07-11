#!/bin/sh

# a function to generate random fact files
gen_fact_file() {
    mkdir -p $OUT_DIR
    src_dir=`dirname $BASH_SOURCE[0]`
    ruby /home/kotname/Documents/Diplom/Code/doop/DiffAnalysis/Datalog-Programs/SouffleSynthetic/random_fact_generator.rb $@ > $OUT_DIR/$1.tsv
}

# set default benchmark size to small
TMP_SIZE=$1
OUT_DIR=$2
SIZE=${TMP_SIZE:=$SIZE}
SIZE=${SIZE:=small}

echo "Generating facts of size: $SIZE"

