# Giải thích về package

## ks-support
ks-support bao gồm các hàm dùng chung hỗ trợ cho các dự án của team kanshi.

## Cách cài đặt
Cài đặt bằng pip
```
pip install git+https://github.com/bui-nhu-phu/kanshi-batch-support.git@${tagname}
```
${tagname}: tagname là tên versionn, ví dụ: 0.0.1

### 1. logger
logger được thiết kế để xuất log trong quá trình chương trình được thực thi, tuân theo các log level chính info, error, warning,...

Ví dụ:
```
from logger import logger

logger.info('Input logger message here...')
```

### 2. push_to_firehose
push_to_firehose là hàm thực hiện việc đẩy dữ liệu lên server thông qua aws firehose.

Các tham số đầu vào:
- push_data: list danh sáchh các bản ghi sẽ được đẩy thông qua firehose
- delivery_stream_name: tên của firehose sẽ đẩy dữ liệu
- firehose_client: kết nối firehose client
- record_quantity: số lượng bản ghi của mỗi lần đẩy dữ liệu

Ví dụ:
```
push_data = [
    {
        'key1': 'value1',
        'key2': 'value2',
    },
    {
        'key3': 'value3',
        'key4': 'value4',
    }
]

delivery_stream_name = 'put-data-sample'
firehose_client = boto3.client('firehose')

#Bắt đầu put data bằng push_to_firehose
push_to_firehose(push_data, delivery_stream_name, firehose_client, 500)
```
