#!/usr/bin/env python3
import os

import pytest
from flask_migrate import Migrate, Manager, MigrateCommand

from apos.extensions import app, db

app.config.from_object('apos.config.Config')
MIGRATION_DIR = os.path.join('apos', 'migrations')

migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    pytest.cmdline.main([])


@manager.command
def test_ci():
    pytest.cmdline.main(['-q'])


if __name__ == '__main__':
    manager.run()
