import json
import random as rand
import boto3
import time

db_client = boto3.client("dynamodb")


def add_to_table(pet_of_the_day):
    response = db_client.put_item(
        TableName="pet_statistics",
        Item={"PK": {"S": pet_of_the_day}, "SK": {"N": str(int(time.time()))}},
    )


def lambda_handler(event, context):
    pets = ["Brutus", "Borys", "Majkus", "Milusia"]
    pet_of_the_day = rand.choice(pets)

    add_to_table(pet_of_the_day)

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
