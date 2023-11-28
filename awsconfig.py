import boto3
session = boto3.Session(
    region_name='us-east-1',
    aws_access_key_id="ASIAZOIVOVX5UGLMJUOG",
    aws_secret_access_key="ClMv8P0MjXJeg5h476+YpqiiSS+4AdBDpMZVY2d8",
    aws_session_token="FwoGZXIvYXdzEGsaDAUuFDxuG0lrIWyjpSLQAVQm+WrpfMV8wI8LrWCEimXLb4QNc/4Ueo1I+lAa5vp6vEG9oZwNQIxL4vHtP+5NI4a4CSCQHqWjnRNu6M9A0/O6hsDvFqEUXbXsndzDUn9QRVh3USaLArpIPEiOuUhT/0PpHu4MNJMLDGCZpqzYURLi5DZgC84cQcRmkGWVXPcWhglKwpMmX3iu0Je6BBUNziE5CaI44chsYv03SOx3Q4OnW7LHEA1yDVpP9Ue08kqSu0G4NRlVGUk6chR1Kh+DUhX4/H3wA6Pgvd+QHLDI1ooonYeVqwYyLdAEzqZQnzDf9xg3PVimcDBG01ilA25uFGe689KOVWl7brV/qhrReNWmx7HUPw=="
)

s3_client = session.client('s3')
dynamo_table = session.resource('dynamodb').Table("sesiones-alumnos")
sns_topic =  session.resource('sns').Topic("arn:aws:sns:us-east-1:649121934843:AlumnosInfo")