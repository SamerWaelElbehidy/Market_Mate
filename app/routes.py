from app.controllers.device_controller import device_controller
from app.controllers.image_controller import image_controller
from app.controllers.feedback_controller import feedback_controller
from app.controllers.admin.admin_auth_controller import admin_auth_controller
from app.controllers.admin.admin_dashboard_controller import admin_dashboard_controller
from app.controllers.admin.admin_controller import admin_controller
from app.controllers.admin.admin_device_controller import admin_device_controller
from app.controllers.admin.admin_image_controller import admin_image_controller
from app.controllers.admin.admin_analysis_controller import admin_analysis_controller
from app.controllers.admin.admin_feedback_controller import admin_feedback_controller
from app.controllers.admin.admin_insights_controller import admin_insights_controller

def register_routes(app):
    app.register_blueprint(device_controller, url_prefix='/api')
    app.register_blueprint(image_controller, url_prefix='/api')
    app.register_blueprint(feedback_controller, url_prefix='/api')
    app.register_blueprint(admin_device_controller)
    app.register_blueprint(admin_image_controller)
    app.register_blueprint(admin_analysis_controller)
    app.register_blueprint(admin_feedback_controller)
    app.register_blueprint(admin_auth_controller)
    app.register_blueprint(admin_dashboard_controller)
    app.register_blueprint(admin_controller)
    app.register_blueprint(admin_insights_controller)