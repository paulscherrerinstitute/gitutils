#!/bin/bash
LC_CTYPE=en_US.utf8
# decript the token file
echo "Please, type the password to decrypt the token file: "
openssl aes-256-cbc -d -a -in /root/token.enc -out /root/.gitutils_token
source activate
conda env create -f environment_droplet.yml -n gitutils
source activate gitutils
cd ${RUN_DIR}
# run unit test
echo "Run gitutils tests..."
cd ./gitutils
echo "Unit tests..."
python -m unittest gitutils.tests.gitutils_unittest
if [ $? = 0 ]; then
    echo "Unit tests... Success!"
else
    echo "PROBLEM WITH UNIT TESTS"
fi
echo "Commands tests..."
python -m unittest gitutils.tests.gitutils_cmds
if [ $? = 0 ]; then
    echo "Commands tests... Success!"
else
    echo "PROBLEM WITH COMMAND TESTS..."
fi
echo "Done."