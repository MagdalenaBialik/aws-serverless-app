import json
import boto3
import time

db_client = boto3.client('dynamodb')
ses_client = boto3.client('ses')
s3_client = boto3.client("s3")


def lambda_pet_statistics(event, context):
    pets = ['Brutus', 'Borys', 'Majkus', 'Milusia']
    pet_statistics_dict = {}
    for pet in pets:
        response = db_client.query(
            TableName='pet_statistics',
            Select='COUNT',
            KeyConditionExpression='PK = :PK',
            ExpressionAttributeValues={
                ':PK': {'S': pet}}
        )
        pet_statistics_dict[pet] = response['Count']

    print(pet_statistics_dict)

    message = lambda_prepare_message(pet_statistics_dict)
    lambda_sent_pet(message)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def get_object_from_s3(pet_statistics_dict):
    max_pet_statistics_dict = max(pet_statistics_dict, key=pet_statistics_dict.get)
    s3_bucket_name = "my-pets-statistics-bucket"

    object_key = f"{max_pet_statistics_dict}.jpg"

    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': s3_bucket_name, 'Key': object_key},
        ExpiresIn=3600)

    return url


def lambda_prepare_message(pet_statistics_dict):
    max_pet_statistics_dict = max(pet_statistics_dict, key=pet_statistics_dict.get)

    message = "Overall Pet Statistics: \n"
    for nazwa_zwierzatka, wynik in pet_statistics_dict.items():
        message += f"{nazwa_zwierzatka}:{wynik}\n"

    message += get_object_from_s3(pet_statistics_dict)
    return message


def lambda_sent_pet(message):
    ses_response = ses_client.send_email(
        Source='alek.fidelus@gmail.com',
        Destination={
            'ToAddresses': ['magdalena.bialik@gmail.com', 'alek.fidelus@gmail.com']
        },
        Message={
            'Subject': {
                'Data': 'Całościowe statystyki zwierzatek dnia'
            },

            'Body': {
                'Text': {
                    'Data': message
                }
            }
        }
    )
    return ses_response
