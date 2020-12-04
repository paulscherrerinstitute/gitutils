#!/bin/bash
LC_CTYPE=en_US.utf8
# decript the token file
echo "Please, type the password to decrypt the token file: "
gpg --output /root/.gitutils_token --decrypt /root/token.enc 
source activate
conda env create -f environment_droplet.yml -n gitutils
source activate gitutils
cd ${RUN_DIR}/gitutils
# run unit test
echo "Run gitutils tests..."
echo "Unit tests..."
python -m unittest gitutils.tests.gitutils_unittest -b
if [ $? = 0 ]; then
    echo "Unit tests... Success!"
else
    echo "PROBLEM WITH UNIT TESTS"
fi
echo "Commands tests..."
python -m unittest gitutils.tests.gitutils_cmds -b
if [ $? = 0 ]; then
    echo "Commands tests... Success!"
else
    echo "PROBLEM WITH COMMAND TESTS..."
fi
echo "Done."