# TrailView

### Tutorial of py2app
https://py2app.readthedocs.io/en/latest/tutorial.html#create-a-setup-py-file

### Install py2app
```
pip install py2app
```

### Create a setup.py file
```
$ py2applet --make-setup MyApplication.py
Wrote setup.py
```

### Clean up your build directories
```
$ rm -rf build dist
```

### Build the application
```
python setup.py py2app
```