import os
import sys
from flask import Flask, jsonify

# Add the parent directory to the path so we can import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the Flask app
from app import app as flask_app

# Define a handler function for AWS Lambda
def handler(event, context):
    """AWS Lambda handler function for the Flask app."""
    # Get the HTTP method and path from the event
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    
    # Get the query parameters and headers
    query_params = event.get('queryStringParameters', {}) or {}
    headers = event.get('headers', {}) or {}
    
    # Get the body
    body = event.get('body', '')
    
    # Create a WSGI environment
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': '&'.join([f"{k}={v}" for k, v in query_params.items()]),
        'CONTENT_LENGTH': str(len(body) if body else 0),
        'SERVER_NAME': 'netlify',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': body,
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    # Add the headers
    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = f'HTTP_{key}'
        environ[key] = value
    
    # Create a response object
    response_status = None
    response_headers = []
    response_body = []
    
    def start_response(status, headers):
        nonlocal response_status, response_headers
        response_status = status
        response_headers = headers
    
    # Call the Flask app
    response = flask_app(environ, start_response)
    
    # Get the response body
    for chunk in response:
        response_body.append(chunk)
    
    # Convert the response body to a string
    response_body = b''.join(response_body).decode('utf-8')
    
    # Get the status code
    status_code = int(response_status.split(' ')[0])
    
    # Convert the headers to a dictionary
    headers_dict = {key: value for key, value in response_headers}
    
    # Return the response
    return {
        'statusCode': status_code,
        'headers': headers_dict,
        'body': response_body,
    }
