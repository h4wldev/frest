# -*- coding: utf-8 -*-
import os

from app import app, db, routes, handler
from app.config import APP_DEFAULT_PORT, APP_SECRET_KEY, ENVIRONMENT
from app.modules.auth import basic, token


if __name__ == '__main__':
    port = int(os.environ.get('PORT', APP_DEFAULT_PORT))

    app.secret_key = APP_SECRET_KEY

    db.create_all()

    if ENVIRONMENT == 'production' or ENVIRONMENT == 'testing':
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        app.run(host='0.0.0.0', port=port, debug=True)
