Telegram bot app on AWS Lambdas.
Developed by Rinat Akhmedziiev

To run locally:

1. Creare "/Users/advaer/dev/pet/advaerbot/chalicelib/conf/secret.py" and put all settings from secret.py.default
2. Install requirements-dev.txt
2. From root directory run "chalice local"

To deploy:
1. Add AWS IAM keys
2. Unzip "vendor/SQLAlchemy-1.1.13-cp36-cp36m-linux_x86_64.whl" into vendor dir.
3. From root directory run "chalice deploy"