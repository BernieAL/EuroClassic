import os
from dotenv import load_dotenv

for env_file in ('.env','.flaskenv'):
	env = os.path.join(os.getcwd(),env_file)
	if os.path.exists(env):
		load_dotenv(env)

workers = int(os.environ.get('GUNICORN_PROCESSES','2'))
threads = int(os.environ.get('GUNICORN_THREADS','4'))

#timeout = int(os.environ.get('GUNICORN_TIMEOUT','120'))

bind = os.environ.get('GUNICORN_BIND','0.0.0.0:7777')

forwarded_allow_ips = '*'

secure_scheme_headers = {'X-Forwarded-Proto':'https'}
