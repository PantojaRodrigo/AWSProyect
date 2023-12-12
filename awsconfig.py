import boto3
session = boto3.Session(
    region_name='us-east-1',
    aws_access_key_id="ASIAZOIVOVX55DZBFLXS",
    aws_secret_access_key="9KVx2+a9g4iaQ7g1MtXHuBIuBa63hvFXfUwCQR9z",
    aws_session_token="FwoGZXIvYXdzENH//////////wEaDGvzQ7CJqksiq4/PViLQASR3T4ppODVSeGUUTu9+HX94BVACWqNsMbnIQgx4Goim2aIHKx2jLKEIFMuV5YwYmR0NalcYg0VKBMwaqj8JdwbrMz0vrSNE5wG6/pxO2nypHF81b1jabbebtIE9hJsebqW69CEAOPZ1sM6Bx8VbXoR4bNMUMxhSrEaju64mMEVIDM5GR1UQVhtmpAi8qBnIYGFwlMwcYrbZ/jsW3Aev0f0lddlqX3OXay7XMqSRP77PUoKRFl96FOGr04/pe6BfYyxurLgjrT4UFEXcHW7XZhEo2NrjqwYyLXM6STAoHXBoxV6qi52snZfCCjG86BaHJaeeh6Gbiy9IjbdnSCEXdEBM2wObhA=="
)

s3_client = session.client('s3')
dynamo_table = session.resource('dynamodb').Table("sesiones-alumnos")
sns_topic =  session.resource('sns').Topic("arn:aws:sns:us-east-1:649121934843:AlumnosInfo")