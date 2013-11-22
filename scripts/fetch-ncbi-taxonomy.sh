#!/bin/bash

base=taxdump
mkdir taxonomy/
cd taxonomy/
mkdir ncbi/
cd ncbi/
wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/$base.tar.gz
tar xvfz $base.tar.gz
rm $base.tar.gz
