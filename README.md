# website_google_app_engine

To run locally: 
dev_appserver.py .

To deploy: 
- using appcfg: appcfg.py -A __PROJECT_NAME___ -V v1 update .
- using gcloud: gcloud app deploy --project __PROJECT_NAME___ -v v1

Code to edit in: 
templates/onepage.html
