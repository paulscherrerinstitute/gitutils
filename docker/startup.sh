#!/bin/bash
#activates env
source activate
conda env create -f environment_droplet.yml

conda activate gitutils 
cd ${RUN_DIR}
# decript the token file
echo "Please, type the password to decrypt the token file: "
openssl aes-256-cbc -d -a -in /root/token.enc -out /root/.gitutils_token
# run unit test
echo "Run gitutils tests..."
cd ./gitutils && python -m unittest gitutils.tests.gitutils_unittest
# python -m unittest gitutils.tests.gitutils_cmds
echo "Done."