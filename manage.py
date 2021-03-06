import os

from coverage import coverage
import unittest


from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from bucketlist import app, db, models

COV = coverage(
    branch=True,
    include='bucketlist/*',
    omit=[
        'tests/*',
        'bucketlist/config.py',
        'bucketlist/models.py',
        'bucketlist/*/__init__.py'
    ]
)
COV.start()


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report(show_missing=True)
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
