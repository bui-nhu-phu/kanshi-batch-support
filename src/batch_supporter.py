__author__='buinhuphu'
__author_email__='bn.phu@afterfit.co.jp'

import json
import time
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

        logger.info(f'pushed records: {count_of_push_data}')

        return count_of_push_data
    except Exception as e:
        logger.warning(e)

def get_last_modified_datetime(plant_id, last_modified_time):
    """
    get_last_modified_datetime does get the last modified datetime of file in folder
    """
    logger.info(f'Start get last modified datetime')
    logger.info('This is version 0.0.2')
    logger.info(f'Completed get last modified datetime')
    return [
        {
            "plant_id": plant_id,
            "last_modified_time": last_modified_time,
        }
    ]
