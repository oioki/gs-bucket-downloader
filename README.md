# gs-bucket-downloader

```
usage: gs_bucket_downloader.py [-h] -u URL [-o OUTPUT]

Download contents of Google Cloud Storage bucket via XML API

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     HTTP(s) endpoint of public bucket
  -o OUTPUT, --output OUTPUT
                        Local directory to dump bucket contents
```

## Example

```
$ ./gs_bucket_downloader.py -u http://storage.googleapis.com/kubernetes-release -o kubernetes-release
Google Storage bucket: kubernetes-release

http://storage.googleapis.com/kubernetes-release
 ... addons/crinit/v0.0.0-test.1/crinit
 ... addons/test/crinit/2017-11-17/crinit
 ... anago-gcs-write.183918
     [SNIP]
```
