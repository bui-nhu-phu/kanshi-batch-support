# Giải thích về package

## kanshi-lib
kanshi-lib bao gồm các hàm dùng chung hỗ trợ cho các dự án của team kanshi.

## Cách cài đặt
Cài đặt bằng pip
```
pip install git+https://github.com/afterfit/kanshi-lib.git@

# hoặc download theo version
pip install git+https://github.com/afterfit/kanshi-lib.git@${tagname}
```
${tagname}: tagname là tên versionn, ví dụ: 0.0.1

## Chi tiết các hàm
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
- push_data: dữ liệu kiểu list, list danh sáchh các bản ghi sẽ được đẩy thông qua firehose
- delivery_stream_name: dữ liệu kiểu str, tên của firehose sẽ đẩy dữ liệu
- firehose_client: kết nối firehose client
- record_quantity: dữ liệu kiểuu int, số lượng bản ghi của mỗi lần đẩy dữ liệu. Default: 500

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

### 3. format_event_time
format_event_time là hàm thực hiện việc convert event time của sự kiện lambda trigger thành định dạng datetime mà database lưu trữ

Các tham số đầu vào:
- event_time: dữ liệu kiểu str, là datetime của sư kiện lambda trigger
- timestamp_suf: dữ liệu kiểu str, là định dạng timezone. Default: '+09:00'

Ví dụ:
```
event_time = '2023-08-09T09:20:26.251Z'
received_time = format_event_time(event_time)

print(received_time)
#2023-08-09T09:20:26+09:00
```

### 4. list_folders
list_folders là hàm thực hiện việc get danh sách tất cả các folder con của một folder s3

Các tham số đầu vào:
- bucket_name: dữ liệu kiểu str, là tên của s3 bucket
- sub_folder: dữ liệu kiểu str, là đường dẫn đầy đủ của s3 folder cha
- s3_client: s3 client hỗ trợ việc kết nối tới aws s3

Ví dụ:
```
import boto3
s3_client = boto3.client('s3',
                         aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID',
                         aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY'
                         )

sample_folder_list = list_folders('your_bucket_name', 'your_sub_folder', s3_client)

```

### 5. list_files
list_files là hàm thực hiện việc get danh sách tất cả các file nằm trong thư mục s3

Các tham số đầu vào:
- bucket_name: dữ liệu kiểu str, là tên của s3 bucket
- sub_folder: dữ liệu kiểu str, là đường dẫn đầy đủ của s3 folder cha
- s3_client: s3 client hỗ trợ việc kết nối tới aws s3

Ví dụ:
```
import boto3
s3_client = boto3.client('s3',
                         aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID',
                         aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY'
                         )

sample_file_list = list_files('your_bucket_name', 'your_sub_folder', s3_client)

```

### 6. get_json_data_from_s3
get_json_data_from_s3 là hàm thực hiện việc get dữ liệu json từ file json trên s3

Các tham số đầu vào:
- bucket_name: dữ liệu kiểu str, là tên của s3 bucket
- key: dữ liệu kiểu str, là đường dẫn đầy đủ của s3 file
- s3_resource: s3 resource hỗ trợ việc kết nối tới aws s3
- encoding: dữ liệu kiểu str, là kiểu encode dữ liệu. Default: 'utf-8'

Ví dụ:
```
import boto3
s3_resource = boto3.resource('s3',
                         aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID',
                         aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY'
                         )

sample_json_data = get_json_data_from_s3('your_bucket_name', 'your_json_key', s3_resource)

```
### 7. get_csv_data_from_s3
get_csv_data_from_s3 là hàm thực hiện việc get dữ liệu csv từ file csv trên s3

Các tham số đầu vào:
- bucket_name: dữ liệu kiểu str, là tên của s3 bucket
- key: dữ liệu kiểu str, là đường dẫn đầy đủ của s3 file
- s3_resource: s3 resource hỗ trợ việc kết nối tới aws s3
- encoding: dữ liệu kiểu str, là kiểu encode dữ liệu. Default: 'cp932'

Ví dụ:
```
import boto3
s3_resource = boto3.resource('s3',
                         aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID',
                         aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY'
                         )

sample_json_data = get_json_data_from_s3('your_bucket_name', 'your_csv_key', s3_resource)

```

### 8. get_last_modified_datetime
get_last_modified_datetime là hàm thực hiện việc tạo ra một danh sách các object chứa thông tin về thời điểm cuối cùng nhận file dữ liệu

Các tham số đầu vào:
- plant_id: dữ liệu kiểu str, id của trạm điện
- data_type: kiểu dữ liệu sẽ check là gì
- received_at: dữ liệu kiểu str, là dữ liệu thời gian của lần cuối cùng nhận được file

Ví dụ: 
```
last_modified_datetime = get_last_modified_datetime('your_plant_id', 'your_data_type', '2023-08-09T09:20:26+09:00')

print(last_modified_datetime)
#[
#   {
#       "plant_id": "your_plant_id",
#       "data_type": "your_data_type",
#       "received_at": "2023-08-09T09:20:26+09:00"
#   }    
#]
```

### 9. get_plant_master_data
get_plant_master_data laf hàm thực hiện việc lấy ra thông tin chi tiết của một trạm điện, bao gồm cả thông tin chi tiết của các thiết bị trong trạm điện đó

Các tham số đầu vào:
- device_type: mã kiểu loại thiết bị
- serial_number: serial number của thiết bị
- api_access_key: api access key để access api
- api_url: url của api. Default os.getenv('API_BASE_URL')

Ví dụ:
```
device_type = 1 # thiết bị pcs
serial_nnumber = 'your_serial_nnumber'
api_access_key = 'your_access_key'
api_url= 'your_api_url'

plant_info = get_plant_master_data(device_type, serial_number, api_access_key, api_url=API_BASE_URL)
    
```
