#!/usr/bin/env python3
import os

from flask_migrate import Migrate, Manager, MigrateCommand

from apos.app import app
from apos.extensions import db

app.config.from_object('apos.config.Config')
MIGRATION_DIR = os.path.join('apos', 'migrations')

migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
