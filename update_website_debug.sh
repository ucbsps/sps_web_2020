#!/bin/bash

# Copy static files to website
rsync -rc ~/sps_web_2020/static ~/public_html/sps/

# Rewrite css urls
cd ~/public_html/sps/static
for file in $(find . -name "*.css"); do
    cat $file | sed 's|"/static|"/~$(whoami)/sps/static|g' > tmp
    cat tmp | sed "s|'/static|'/~$(whoami)/sps/static|g" > $file
done

# Trigger update of website code
touch ~/public_html/sps/run.fcgi
