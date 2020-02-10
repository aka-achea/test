#!/usr/bin/python3
#coding:utf-8


from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
# import logging
from configparser import ConfigParser
from pprint import pprint

from conf import qconf,bucket,target,dest

# logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def cos_client(qconf=qconf):
    '''Create QCloud CosObj Storage Client Object'''
    confile = qconf 
    key = ConfigParser()
    key.read(confile)
    secret_id = key['coskey']['secret_id']  
    secret_key = key['coskey']['secret_key']
    region = 'ap-shanghai'     # 替换为用户的 Region
    token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
    scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    config = CosConfig(Region=region,SecretId=secret_id,SecretKey=secret_key,Token=token,Scheme=scheme)
    return CosS3Client(config)


def upload_to_cos(source,bucket,dest):
    '''Upload file to QCloud CosObj Storage'''
    client = cos_client()
    with open(source,'rb') as fp:
        try:
            response = client.put_object(
                Bucket=bucket,
                Body=fp,
                Key=dest,
                StorageClass='STANDARD',
                ACL='public-read',  # 请慎用此参数,否则会达到1000条 ACL 上限
                Expires='0',
                CacheControl='no-store,no-cache,must-revalidate,proxy-revalidate',
                ContentType='text/html',
            )
        except:
            raise
    return response['ETag']


def download_cos(bucket,objfolder):
    '''Download file to QCloud CosObj Storage'''
    client = cos_client()
    try:
        response = client.list_objects(
            Bucket=bucket,
            Prefix=objfolder
        )
        filelist = response['Contents']
        filelist = [ f['Key'] for f in filelist ]
        # pprint(filelist)
        for f in filelist:
            response = client.get_object(
                Bucket=bucket,
                Key=f,
            )
            body = response['Body']
            fname = f.split('/')[-1]
            body.get_stream_to_file(fname)
    except:
        raise
    return filelist



if __name__ == "__main__":   
    result = upload_to_cos(target,bucket,dest)
    print(result)