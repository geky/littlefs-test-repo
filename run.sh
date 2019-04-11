#!/bin/bash

set -e
rm -f v1.results
rm -f v2.results

for i in {0..12}
do
for j in {2..12}
do
    COUNT=$((2**i))
    SIZE=$((2**j))
    (
        cd v1
        touch main.c
        make "CFLAGS+=\
                -DLFS_FILE_COUNT=$COUNT\
                -DLFS_FILE_SIZE=$SIZE\
                -DLFS_BLOCK_COUNT=$((2**17))\
                -DLFS_READ_SIZE=$(($1>64?$1:64))\
                -DLFS_PROG_SIZE=$(($2>64?$2:64))\
                -DLFS_BLOCK_SIZE=$3"
        ./lfs >> ../v1.results
    ) &
    (
        cd v2
        touch main.c
        make "CFLAGS+=\
                -DLFS_FILE_COUNT=$COUNT\
                -DLFS_FILE_SIZE=$SIZE\
                -DLFS_BLOCK_COUNT=$((2**17))\
                -DLFS_READ_SIZE=$1\
                -DLFS_PROG_SIZE=$2\
                -DLFS_BLOCK_SIZE=$3\
                -DLFS_CACHE_SIZE=$(($2>64?$2:64))"
        ./lfs >> ../v2.results
    ) &
    wait
done
done
