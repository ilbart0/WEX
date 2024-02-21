import unittest
from unittest.mock import MagicMock
from lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):
    def setUp(self):
        self.event = {
            'description': 'Test transaction',
            'date': '2024-02-21',
            'amount': '10.50'
        }

    def test_lambda_handler_success(self):
        mock_table = MagicMock()
        mock_table.put_item.return_value = {}
        lambda_handler.table = mock_table

        response = lambda_handler(self.event, {})
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('message', response['body'])
        self.assertIn('Transaction ID', response['body'])

    def test_lambda_handler_invalid_description(self):
        self.event['description'] = 'A description longer than fifty characters A description longer than fifty characters A description longer than fifty characters'
        response = lambda_handler(self.event, {})
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('error_message', response['body'])

    def test_lambda_handler_invalid_date_format(self):
        self.event['date'] = '02-21-2024'
        response = lambda_handler(self.event, {})
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('error_message', response['body'])

    def test_lambda_handler_invalid_amount(self):
        self.event['amount'] = 'invalid_amount'
        response = lambda_handler(self.event, {})
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('error_message', response['body'])

if __name__ == '__main__':
    unittest.main()
