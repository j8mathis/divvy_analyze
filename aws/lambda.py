import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    print('event:', event)
    from_station_list = []
    for record in event['Records']:
        from_station_list.append(int(record['dynamodb']['Keys']['station_id'].get('N')))

    for i in from_station_list:
        fe = Key('from_station_id').eq(i)
        # pe = "from_station_id, from_station_name"

        dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
        tbl_trip_data = dynamodb.Table('TripDataSample')

        response = tbl_trip_data.query(
            KeyConditionExpression=fe,
            IndexName='from_station_id-index'
        )

        items = response['Items']

        while 'LastEvaluatedKey' in response:
            response = tbl_trip_data.query(
                KeyConditionExpression=fe,
                IndexName='from_station_id-index',
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items += response['Items']

        from_count_dict = {}
        from_count_dict['from_station_id'] = i
        from_count_dict['from_count'] = len(items)
        print(from_count_dict)

        tbl_from_count = dynamodb.Table('from_station_count')
        response = tbl_from_count.put_item(Item=from_count_dict)