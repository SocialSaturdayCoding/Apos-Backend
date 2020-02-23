from flask_migrate import Migrate, Manager, MigrateCommand

from app import app, db

app.config.from_object('config.Config')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
