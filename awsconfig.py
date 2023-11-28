import boto3
session = boto3.Session(
    region_name='us-east-1',
    aws_access_key_id="ASIAZOIVOVX55PF4BZIS",
    aws_secret_access_key="exs1FckwAe5jxMaGZ7ZmM7Ge+S31QE1CLErhOjZo",
    aws_session_token="FwoGZXIvYXdzEG8aDITukhyOjMgksNYILiLQAQEkCbTifnAQ28fewxHmrnDEDRQGIGcb/zFFYvGEHJa8l5gBTI809t33WPb+3yA7Mq9wsGCgXHKHDaWesPtP/aXITVqZqbVe7xEq3F64NIzi3kPiMc1Gr78OqAhzhfBccKke7ZH/HP4ZzB+EHmFVD9uVaYLJnallB6AA73A+yr1kf340OFaPnTFZan2o0uGZqf89blXMetF3W93jrcr24WfOcZ6SDBHuIpSP55hTF5EeLSAcn4b4cWMMxtnXUa0LP04NjWcmUcYJF1Vc6VTPw7AoxvqVqwYyLfabL9Ri9tfBytZ4G/guwboYGnJN29e+O/W2kZG2vt/bBC/IgaVHWgOFMbZlrQ=="
)

s3_client = session.client('s3')
dynamo_table = session.resource('dynamodb').Table("sesiones-alumnos")
sns_topic =  session.resource('sns').Topic("arn:aws:sns:us-east-1:649121934843:AlumnosInfo")