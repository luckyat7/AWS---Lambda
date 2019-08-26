import boto3
def lambda_handler(event, context):
	filename=event['Records'][0]['s3']['object']['key']
	s3client=boto3.client('sns')
	s3client.publish(Message='FileName is {}'.format(filename) , TopicArn="arn:aws:sns:us-east-1:001082169132:test")
	return event