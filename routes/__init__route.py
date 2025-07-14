from flask import Flask

def register_routes(app: Flask):
    from models.drivers import drivers_bp
    from models.team import teams_bp
    from models.race import races_bp
    from models.User import users_bp
    from models.predictions import predictions_bp
    from models.results import results_bp
    from models.shedule import shedule_bp

    app.register_blueprint(drivers_bp, url_prefix="/drivers")
    app.register_blueprint(teams_bp, url_prefix="/teams")
    app.register_blueprint(races_bp, url_prefix="/races")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(predictions_bp, url_prefix="/predictions")
    app.register_blueprint(results_bp, url_prefix="/results")
    app.register_blueprint(shedule_bp, url_prefix="/shedule")
