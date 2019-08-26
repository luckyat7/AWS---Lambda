import json
import logging
import boto3


cors_headers = {
    "Access-Control-Allow-Origin": "*"
}


def send_response(response, status_code):
    return {
        "statusCode": status_code,
        "headers": cors_headers,
        "isBase64Encoded": False,
        "body": json.dumps(response)
    }


def getResultOfOperation(StackSetName, OperationId):
    client = boto3.client('cloudformation')
    response = client.list_stack_set_operation_results(
        StackSetName='testStackset',
        OperationId=OperationId,
    )
    logging.info("RESPONSE {}".format(response))
    print response
    #Sometimes the operation results has an empty summary so we'll run it again
    if response['Summaries'][0]['Status'] is None:
        getResultOfOperation(StackSetName, OperationId)
    else:    
        return response['Summaries'][0]['Status']


def lambda_handler(event, context):
    client = boto3.client('cloudformation')
    logging.info("Event {}".format(event))
    print event
    accountID = event['pathParameters']['accountid']
    if accountID:
        try:
            response = client.create_stack_instances(
                StackSetName='testStackset',
                Accounts=[accountID,],
                Regions = [
                          'us-east-1',
                      ],
            )


            operationID = response['OperationId']

            print operationID
            
            while (getResultOfOperation('testStackset', operationID) == 'PENDING' or getResultOfOperation(
                    'testStackset', operationID ) == 'RUNNING'):
                pass

                statusOfOperation = getResultOfOperation('testStackset', 'ff93c711-f8d5-4e8e-a901-4c0ee4817dfd')
                print statusOfOperation
            
                if statusOfOperation == 'SUCCESS':
                    send_response('Successfully Added Accounts to StackSet', 200)
                else:
                    send_response('Failed to Add Accounts to StackSet', 500)
        except Exception as e:
            print "An Exception Occured {}".format(e.message)
            send_response(e.message, 500)
    else:
        send_response('Account Id Missing', 500)
