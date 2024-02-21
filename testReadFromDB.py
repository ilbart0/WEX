import unittest
from unittest.mock import MagicMock
from lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):
    def setUp(self):
        self.event = {
            'queryStringParameters': {
                'transactionId': 'c026461e-aee9-4359-be55-d94a208ebde2',
                'targetCurrency': 'EUR'
            }
        }

    def test_lambda_handler_success(self):
        mock_response = {
            'Item': {
                'description': 'Order n. 1234567',
                'date': '2024-02-08',
                'amount': '199.99'
            }
        }
        mock_table = MagicMock()
        mock_table.get_item.return_value = mock_response
        lambda_handler.table = mock_table

        response = lambda_handler(self.event, {})
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('transactionId', response['body'])
        self.assertIn('description', response['body'])
        self.assertIn('date', response['body'])
        self.assertIn('targetCurrency', response['body'])
        self.assertIn('amount', response['body'])
        self.assertIn('converted_amount', response['body'])
        self.assertIn('message', response['body'])

    def test_lambda_handler_transaction_not_found(self):
        mock_response = {}
        mock_table = MagicMock()
        mock_table.get_item.return_value = mock_response
        lambda_handler.table = mock_table

        response = lambda_handler(self.event, {})
        self.assertEqual(response['statusCode'], 404)
        self.assertIn('error_message', response['body'])

if __name__ == '__main__':
    unittest.main()
