import json
import boto3

ses_client = boto3.client("ses")


def lambda_sent_pet(pet_of_the_day):
    ses_response = ses_client.send_email(
        Source="alek.fidelus@gmail.com",
        Destination={
            "ToAddresses": ["magdalena.bialik@gmail.com", "alek.fidelus@gmail.com"]
        },
        Message={
            "Subject": {"Data": "Pet of the day"},
            "Body": {"Text": {"Data": pet_of_the_day}},
        },
    )
    return ses_response


def lambda_handler(event, context):
    image = event["Records"][0]["dynamodb"]["NewImage"]
    imie = image["PK"]["S"]
    ses_response = lambda_sent_pet(imie)

    return {"statusCode": 200, "body": json.dumps(ses_response)}
