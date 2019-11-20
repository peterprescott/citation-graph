RMDIR /Q/S _build
python convertMD.py
sphinx-apidoc -f -o . ..
sphinx-build -c . -b html . _build
.\_build\index.html
