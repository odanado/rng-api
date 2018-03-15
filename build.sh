#/bin/bash

mkdir -p .temp

cp -r src .temp
cp -r venv/lib64/python3.?/site-packages/ .temp/vendor

cd .temp

zip -q -r ../lambda.zip . 

cd ..

rm -r .temp
