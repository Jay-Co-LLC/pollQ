import json
import boto3

sqs = boto3.resource('sqs')
q = sqs.get_queue_by_name(QueueName='LambdaResultsQueue')

def lambda_handler(event, context):
    
    msgs = q.receive_messages()
    
    if (len(msgs) > 0):
        res = msgs[0].body
        if (res == "SUCCESS"):
            for m in msgs:
                m.delete()
                
            return {
                'statusCode' : 200,
                'headers' : {
                    'Access-Control-Allow-Origin' : '*'
                },
                'body' : json.dumps('Lambda Completed Successfully')
            }
        elif (res == "FAILURE"):
            for m in msgs:
                m.delete()
                
            return {
                'statusCode' : 400,
                'headers' : {
                    'Access-Control-Allow-Origin' : '*'
                },
                'body' : json.dumps('Lambda Failed')
            }
        else:
            for m in msgs:
                m.delete()
                
            return {
                'statusCode' : 404,
                'headers' : {
                    'Access-Control-Allow-Origin' : '*'
                },
                'body' : json.dumps('Unknown message in queue')
            }
    else:
        return {
            'statusCode' : 202,
            'headers' : {
                    'Access-Control-Allow-Origin' : '*'
                },
            'body' : json.dumps('No message in queue')
        }
