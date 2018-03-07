# deploy
```bash
export VENDOR_PATH=$PWD/vendor
pip install Cython==0.27 -t ./vendor
pip install -r requirements.txt -t ./vendor
```

``bash
zip -r lambda.zip src vendor
```
