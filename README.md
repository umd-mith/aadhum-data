Configure the softwre:

```
apt-get install python3-pip
pip3 install pipenv
git clone https://github.com/umd-mith/aadhum-data.git
cd aadhum-data
pipenv install --three
```

Configure AWS keys:

```
aws configure
```

Get the data:

```
aws s3 sync s3://aadhum data
```

This should get the AADHUM digitized content on Amazon S3. The data is organized by collection, folder number and then item.

```
data
├── labor
│   ├── 060383
│   │   ├── 0001.jpg
│   │   ├── 0002.jpg
│   │   ├── 0003.jpg
│   │   └── 0004.jpg
│   ├── 060384
│   │   ├── 0001.jpg
│   │   ├── 0002.jpg
│   │   ├── 0003.jpg
│   │   ├── 0004.jpg
│   │   └── 0005.jpg
└── mdu
    ├── 060883
    │   ├── 0001.jpg
    │   ├── 0002.jpg
    │   ├── 0003.jpg
    │   ├── 0004.jpg
    │   ├── 0005.jpg
    │   ├── 0006.jpg
    │   ├── 0007.jpg
    │   ├── 0008.jpg
    │   ├── 0009.jpg
    │   ├── 0010.jpg
    │   ├── 0011.jpg
    │   ├── 0012.jpg
    │   ├── 0013.jpg
...
```

Now generate the IIIF manifests:

```
./generate.py
```
