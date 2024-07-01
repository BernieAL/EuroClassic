import os
from simple_chalk import chalk
from dotenv import load_dotenv,find_dotenv

if os.getenv('RUNNING_IN_DOCKER') == '1':
	load_dotenv(find_dotenv('.env.docker'))   
	print(chalk.green(f"CONFIG - USING - .env.docker"))
else:
	load_dotenv(find_dotenv('.env.local'))   
	print(chalk.green(f"CONFIG - USING - .env.local"))
	

APPLICATION_SECRET_KEY = os.getenv('APPLICATION_SECRET_KEY')
DB_URI = os.getenv('DB_URI')
PROXY_HTTPS = os.getenv('PROXY_HTTPS')
PROXY_HTTP = os.getenv('PROXY_HTTP')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
BACKEND_DIR = os.getenv('BACKEND_DIR')
PROJECT_PATHS= os.getenv('PROJECT_PATHS')
GOOGLE_APP_PW = os.getenv('GOOGLE_APP_PW')
GOOGLE_SENDER_EMAIL = os.getenv('GOOGLE_SENDER_EMAIL')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
API_HOST = os.getenv('API_HOST')
API_PORT = os.getenv('API_PORT')

# Ensure API_HOST and API_PORT are set
if not API_HOST or not API_PORT:
    raise ValueError("API_HOST and API_PORT must be set in the environment variables")


nginx_template = """
server {{
    listen 80;
    listen [::]:80;
    server_name localhost;

    # Redirect http to https
    # return 302 https://$host$request_uri;
}}

server {{
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name localhost;
    ssl_certificate /etc/nginx/ssl/fullchain.pem; 
    ssl_certificate_key /etc/nginx/ssl/server.key;
    include /etc/nginx/ssl/ssl-params.conf;

    root /usr/share/nginx/html;
    index index.html;
    error_page 500 502 503 504 /50x.html;

    location / {{
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache";
    }}

    location /api {{
        proxy_pass http://{api_host}:{api_port}/api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # CORS headers
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS, PUT, DELETE';
        add_header Access-Control-Allow-Headers 'Content-Type, Authorization';
        add_header Access-Control-Allow-Credentials true;

        # Increase timeouts
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
        proxy_send_timeout 60s;
        send_timeout 60s;
    }}
}}
"""


# Fill the template with actual values
nginx_conf = nginx_template.format(api_host=API_HOST, api_port=API_PORT)

# Write the filled template to nginx.conf
with open('backend_copy/nginx.custom-gen.conf', 'w') as f:
    f.write(nginx_conf)


print(chalk.green("(config.py) Nginx configuration file generated"))
#test
#print(f"DB_URI: {DB_URI}")