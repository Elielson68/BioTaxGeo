from flask import Flask

from controller.home_controller import home_blueprint
from controller.form_controller import form_blueprint
from controller.validation_controller import validation_blueprint

app = Flask(__name__)

#home
app.register_blueprint(home_blueprint)

#Readers
app.register_blueprint(form_blueprint)

#Validation
app.register_blueprint(validation_blueprint)

app.run(debug=True, port=8080)
