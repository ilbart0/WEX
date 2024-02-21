import json
import boto3
from decimal import Decimal

# Create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# Use the DynamoDB object to select our table
table = dynamodb.Table('transactions')

def lambda_handler(event, context):
    # 1. Parse out query string params
    transactionId = event['queryStringParameters']['transactionId']
    targetCurrency = event['queryStringParameters']['targetCurrency']

    # Retrieve transaction data from the database
    response = table.get_item(
        Key={
            'ID': transactionId
        }
    )
    transaction_item = response.get('Item')
    
    if not transaction_item:
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': 'Transaction not found.'})
        }

    # Extract transaction details
    description = transaction_item['description']
    date = transaction_item['date']
    amount = Decimal(transaction_item['amount'])  # Convert amount to Decimal
    
    # Convert purchase amount to the target currency using a fixed exchange rate of 1.5
    converted_amount = amount * Decimal('1.5')  # Convert to Decimal before multiplication


    # 2. Construct the body of the response object
    transactionResponse = {}
    transactionResponse['transactionId'] = transactionId
    transactionResponse['description'] = description
    transactionResponse['date'] = date
    transactionResponse['targetCurrency'] = targetCurrency
    transactionResponse['amount'] = str(amount)  # Convert Decimal to string
    transactionResponse['converted_amount'] = str(converted_amount)  # Convert Decimal to string
    transactionResponse['message'] = 'Operation succesful'

    print('converted_amount=' + str(converted_amount))

    # 3. Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)

    # 4. Return the response object
    return responseObject