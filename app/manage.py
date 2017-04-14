import os, sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# from flask.ext.script import Manager, Server
from flask_script import Manager, Server

# from blog import create_app
# app = create_app(os.getenv('config') or 'default')

from blog import app


manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0',
    port = 8080)
)

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    manager.run()
