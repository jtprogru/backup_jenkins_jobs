
SERVER = os.environ.get("JENKINS_SERVER")
API_TOKEN = os.environ.get("JENKINS_API_KEY")
USER = os.environ.get("JENKINS_USER")
JOBS_DIR = 'jenkins_jobs/'
JOB_FILTER = 'test'
BASE_URL = f'https://{SERVER}/api/json?pretty=true'
