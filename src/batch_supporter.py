__author__='buinhuphu'
__author_email__='bn.phu@afterfit.co.jp'

import botocore
import csv
import json
import time
from datetime import datetime
from logger import logger

def push_to_firehose_with_retry(records, stream_name, firehose_client, max_retry=10):
    """
    push_to_firehose_with_retry does push data to firehose if fail will retry push

    :param records: data list
    :param stream_name: name of firehose will put data to here
    :param firehose_client: connect to firehose
    :param max_retry: numbers of retry
    """
    if max_retry < 0:
        logger.error('Put data to firehose failed!!!')
        return
    try:
        response = firehose_client.put_record_batch(
            DeliveryStreamName=stream_name,
            Records=records
        )
        if ('FailedPutCount' in response.keys() and response['FailedPutCount'] > 0) or (
                'FailedPutCount' not in response.keys()):
            logger.warning(f"FailedPutCount: {response['FailedPutCount']}")
            time.sleep(2)
            max_retry -= 1
            push_to_firehose_with_retry(records, stream_name, firehose_client, max_retry)
        else:
            logger.info(f'Completed put {len(records)} records')
    except Exception as e:
        logger.warning(e)
        time.sleep(2)
        max_retry -= 1
        push_to_firehose_with_retry(records, stream_name, firehose_client, max_retry)

def push_to_firehose(push_data, delivery_stream_name, firehose_client, record_quantity=500):
    """
    push_to_firehose does push data to firehose

    :param push_data: data list
    :param delivery_stream_name: name of firehose will put data to here
    :param firehose_client: connect to firehose
    :param record_quantity: numbers of records per put
    """
    try:
        count_of_push_data = len(push_data)
        if count_of_push_data > 0:
            data_set = [push_data[i:i + record_quantity] for i in range(0, count_of_push_data, record_quantity)]
            for datas in data_set:
                records = [{'Data': json.dumps(r).encode('utf8')} for r in datas]
                push_to_firehose_with_retry(records, delivery_stream_name, firehose_client, 10)

        return count_of_push_data
    except Exception as e:
        logger.warning(e)

def get_last_modified_datetime(plant_id, data_type, received_at):
    """
    get_last_modified_datetime does get the last modified datetime of file in folder

    :param plant_id: id of power plant
    :data_type: type of file data
    :param received_at: last time the file was received

    return list object containing data about the last time the file was received
    """
    return [
        {
            "plant_id": plant_id,
            "data_type": data_type,
            "received_at": received_at,
        }
    ]

def format_event_time(event_time, timestamp_suf='+09:00'):
    """
    format_event_time does format event time of lambda trigger

    :param event_time: datetime when event lambda trigger start
    :param timestamp_suf: timestamp suf, default timestamp suf in japan

    return timestamp with format %Y-%m-%dT%H:%M:%S+timestamp_suf
    """
    try:
        date_time = datetime.strptime(event_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        try:
            date_time = datetime.strptime(event_time, '%y-%m-%dT%H:%M:%S.%fz')
        except Exception as e:
            logger.error(f'cannot format event time. error {e}')
            return None

    timestamp = datetime.strftime(date_time, f'%Y-%m-%dT%H:%M:%S') + timestamp_suf

    return timestamp

def list_folders(bucket_name, sub_folder, s3_client):
    """
    list_folders does get all subfolder in s3 folder

    :param bucket_name: s3 bucket name
    :param sub_folder: path of folder you want list subfolder
    :param s3_client: s3 client for connect to aws s3

    return list subfolder
    """
    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name, Prefix=sub_folder, Delimiter='/')
        folder_list = []
        if "CommonPrefixes" not in response:
            return folder_list
        for content in response.get('CommonPrefixes', []):
            folder_list.append(content.get('Prefix'))
        return folder_list
    except Exception as e:
        logger.error(f'cannot get list folder. error {e}')

def list_files(bucket_name, sub_folder, s3_client):
    """
    list_files does get all file in s3 folder

    :param bucket_name: s3 bucket name
    :param sub_folder: path of folder you want list file
    :param s3_client: s3 client for connect to aws s3

    return list file
    """
    try:
        all_objects = []
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name, Prefix=sub_folder):
            if 'Contents' in page:
                all_objects.extend(page['Contents'])

        file_list = []
        for obj in all_objects:
            file_list.append(obj['Key'])

        return file_list
    except Exception as e:
        logger.error(f'cannot get list file. error {e}')

def get_json_data_from_s3(bucket_name, key, s3_resource, encoding="utf-8"):
    """
    get_json_data_from_s3 does read and return json data from json file

    :param bucket_name: s3 bucket name
    :param key: path of json file
    :param s3_resource: s3 resource for connect to aws s3
    :param encoding: encoding type

    return json data
    """
    try:
        content_object = s3_resource.Object(bucket_name, key)
        file_content = content_object.get()["Body"].read().decode(encoding)

        return json.loads(file_content)
    except Exception as e:
        logger.error(f'cannot get json data from s3. error {e}')

def get_csv_data_from_s3(bucket_name, key, s3_resource, encoding="cp932"):
    """
    get_csv_data_from_s3 does read and return csv data from csv file

    :param bucket_name: s3 bucket name
    :param key: path of json file
    :param s3_resource: s3 resource for connect to aws s3
    :param encoding: encoding type

    return json data
    """
    rows = None

    try:
        obj = s3_resource.Object(bucket_name, key)
        lines = obj.get()['Body'].read().decode(encoding).splitlines(True)
        reader = csv.reader(lines, delimiter=';')
        rows = [row for row in reader]

    except botocore.exceptions.ClientError:
        return None

    except UnicodeDecodeError:
        lines = obj.get()['Body'].read().decode("ISO-8859-1").splitlines(True)
        reader = csv.reader(lines, delimiter=';')
        rows = [row for row in reader]

    except Exception:
        lines = obj.get()['Body'].read().decode(encoding).replace('\0','').splitlines(True)
        reader = csv.reader(lines, delimiter=';')
        rows = [row for row in reader]

    return rows
