import json
import math
import boto3
from time import gmtime, strftime
import uuid  # Import UUID library for generating unique IDs
from datetime import datetime
from decimal import Decimal  # Import Decimal for precise numeric representation

# Create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# Use the DynamoDB object to select our table
table = dynamodb.Table('transactions')

def lambda_handler(event, context):
    try:
        # Extract the inputs from the Lambda service's event object
        description = event['description']
        date = event['date']
        amount = event['amount']

        # Validate description length
        if len(description) > 50:
            return {
                'statusCode': 400,
                'body': json.dumps({'error_message': 'Description must not exceed 50 characters.'})
            }

        # Validate transaction date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error_message': 'Invalid transaction date format. Please use YYYY-MM-DD.'})
            }

        # Validate purchase amount
        try:
            amount = Decimal(amount)  # Convert amount to Decimal
            if amount <= 0:
                raise ValueError
            # Round the purchase amount to the nearest cent
            amount = round(amount, 2)
        except ValueError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error_message': 'Purchase amount must be a valid positive number. Please ensure you input a valid number.'})
            }

        # Generate a unique ID for the transaction
        transaction_id = str(uuid.uuid4())

        # Write to the DynamoDB table using the object instantiated
        response = table.put_item(
            Item={
                'ID': transaction_id,
                'description': description,
                'date': date,
                'amount': amount
            }
        )

        # Construct the success response
        success_response = {
            'message': 'Operation successful.',
            'Transaction ID': transaction_id
        }

        # Return the success response
        return {
            'statusCode': 200,
            'body': json.dumps(success_response)
        }
    except Exception as e:
        # Return a negative message if an error occurs
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': 'Operation failed: {}'.format(str(e))})
        }
