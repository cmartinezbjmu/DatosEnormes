#!/bin/bash

echo "The number of arguments is: $#"
#python read_news.py "$1" "$2"

for i in "${@:2}"
do
    python read_news.py "$1" "$i"
done
