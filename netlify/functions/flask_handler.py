#!/usr/bin/env python3
"""
Flask Handler for Netlify Functions
This script handles requests from Netlify Functions and processes them using Flask
"""

import argparse
import json
import os
import sys
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

# Add parent directory to path to import Flask app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

try:
    from app import app as flask_app
except ImportError:
    # If app.py cannot be imported, create a simple Flask app
    from flask import Flask
    flask_app = Flask(__name__)
    
    @flask_app.route('/')
    def index():
        return "Flask app could not be imported. This is a fallback response."

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Flask request handler for Netlify Functions')
    parser.add_argument('--method', default='GET', help='HTTP method')
    parser.add_argument('--path', default='/', help='Request path')
    parser.add_argument('--headers', default='{}', help='Request headers as JSON string')
    parser.add_argument('--query', default='{}', help='Query parameters as JSON string')
    parser.add_argument('--body', default='{}', help='Request body as JSON string')
    return parser.parse_args()

def create_wsgi_environment(args):
    """Create a WSGI environment from the arguments"""
    method = args.method
    path = args.path
    headers = json.loads(args.headers)
    query = json.loads(args.query)
    body = json.loads(args.body)
    
    # Convert query dict to string
    query_string = '&'.join([f"{k}={v}" for k, v in query.items()])
    
    # Create a basic WSGI environment
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'CONTENT_LENGTH': str(len(json.dumps(body)) if body else 0),
        'CONTENT_TYPE': headers.get('content-type', 'application/json'),
        'SERVER_NAME': 'netlify',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': StringIO(json.dumps(body)),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    # Add headers to environment
    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = f'HTTP_{key}'
        environ[key] = value
    
    return environ

def process_request(args):
    """Process the request using Flask app"""
    environ = create_wsgi_environment(args)
    
    # Capture response
    response_status = None
    response_headers = []
    response_body = []
    
    def start_response(status, headers):
        nonlocal response_status, response_headers
        response_status = status
        response_headers = headers
    
    # Capture stdout and stderr
    output = StringIO()
    error = StringIO()
    
    with redirect_stdout(output), redirect_stderr(error):
        # Call the Flask app
        response = flask_app(environ, start_response)
        
        # Get the response body
        for chunk in response:
            if isinstance(chunk, bytes):
                response_body.append(chunk.decode('utf-8'))
            else:
                response_body.append(chunk)
    
    # Get the status code
    status_code = int(response_status.split(' ')[0])
    
    # Convert the headers to a dictionary
    headers_dict = {key: value for key, value in response_headers}
    
    # Return the response
    return {
        'status': status_code,
        'headers': headers_dict,
        'body': ''.join(response_body),
        'stdout': output.getvalue(),
        'stderr': error.getvalue()
    }

def main():
    """Main function"""
    args = parse_args()
    
    try:
        response = process_request(args)
        print(json.dumps(response))
    except Exception as e:
        error_response = {
            'status': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': str(e),
                'traceback': str(sys.exc_info())
            })
        }
        print(json.dumps(error_response))

if __name__ == '__main__':
    main()
