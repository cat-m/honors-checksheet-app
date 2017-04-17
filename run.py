import os

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

#application = app # for Google Cloud

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)