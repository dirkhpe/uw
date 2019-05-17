"""
This script is called by Flask for launching the application.
"""

from gui import create_app

# Run Application
app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(app=app)
