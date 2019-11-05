import boto3
import sys, os

ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
BUCKET_NAME = ''
REMOTE_PATH = ''

DOWNLOAD_LOCATION_PATH = os.path.expanduser("~") + "/s3-backup/"
if not os.path.exists(DOWNLOAD_LOCATION_PATH):
	print ("Making download directory")
	os.mkdir(DOWNLOAD_LOCATION_PATH)

def downloadTotalList(bucketName, remoteDirectoryName, callback):
    
    s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY
    )
    bucket = s3.Bucket(bucketName)
    bucketlist = bucket.objects.filter(Prefix = remoteDirectoryName)
    bucketlist = list(bucketlist)
    totalcount = len(bucketlist)
    currentIndex = 0
    for object in bucketlist:
        if not os.path.exists(os.path.dirname(object.key)):
            os.makedirs(os.path.dirname(object.key))

        if not os.path.isfile(object.key):
            s3.meta.client.download_file(bucketName, object.key, object.key, Callback=callback(object.key, currentIndex, totalcount))

        currentIndex += 1

def downloadTest(filename, current, total):
    print("downloading: " + str(current) + "/" + str(total))

downloadTotalList(BUCKET_NAME, REMOTE_PATH, downloadTest)
