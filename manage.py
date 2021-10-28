#!/usr/bin/env python3
import os

from flask_migrate import Migrate, Manager, MigrateCommand

from apos.extensions import app, db

MIGRATION_DIR = os.path.join('apos', 'migrations')

migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    import pytest
    pytest.cmdline.main([])


@manager.command
def test_ci():
    import pytest
    pytest.cmdline.main(['-q'])


@manager.command
def test_data(clear=False):
    from tests import data
    import sqlalchemy
    if clear:
        db.drop_all()
        db.create_all()
    try:
        data.import_data(db.session)
    except sqlalchemy.exc.IntegrityError:
        print("Could not import test data. This usually happens because your database already contains data.")
        print("Use --clear to clear any existing data before the import.")


if __name__ == '__main__':
    manager.run()
