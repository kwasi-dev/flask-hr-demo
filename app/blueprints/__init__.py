import functools
from flask import g, redirect, url_for

# This function is responsible for initialising the blueprints throughout the system 
def init_blueprints(app):
    from . import auth
    from . import dashboard 
    from . import employee 
    from . import supporting_data_entry 
    from . import appraisal 
    from . import leave 
    from . import disciplinary_action 
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(employee.bp)
    app.register_blueprint(supporting_data_entry.bp)
    app.register_blueprint(appraisal.bp)
    app.register_blueprint(disciplinary_action.bp)
    app.register_blueprint(leave.bp)
