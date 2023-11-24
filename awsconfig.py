import boto3
session = boto3.Session(
    aws_access_key_id="ASIAZOIVOVX5R222AWVE",
    aws_secret_access_key="mDCZq6PQUKTc49z62jmQKWbw3TZFPCyVS9oHxWWq",
    aws_session_token="FwoGZXIvYXdzEAsaDKZ54arOZqrjWgeikyLQAcdXy0V6EPJOh2f7W7PL4b8uiR63pVNbstATOYHiDmcOfAfxIi/VDB5MlZ6y7sEXGu0/hFJ/QyqMomTmgYnS/p3sPRPI1oZXag8H9PuLA9MEKfb1Jj8xD/4qCktu3DDJOl/k6QZnWR68XDvDzyICddwMunpf7bJfZg8Qq3wOwMwGpEx5P6MLWY8Www9PQMFIqGXn3hfzqesWT9QyfEJMWt72pyYd9yLOtbxDyJhjd/f/0anI7Q9CNUYDpb0ChxW8Oh9Nprlg85wxBvxch3EhBT4ot4eAqwYyLVswIifH+T+0mOZOMNcN4m1bfbHre2uj9CpLTK2J1ggK8bWJ0EQ+8gw2P9KYqQ=="
)

s3_client = session.client('s3')
dynamo_client = session.resource('dynamodb')