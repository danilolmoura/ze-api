import os

from application import create_app

port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    app = create_app('dev')
    app.run(host='0.0.0.0', port=port)