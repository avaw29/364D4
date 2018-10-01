from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required

import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.debug=True

class WeatherForm(FlaskForm):
    zip = StringField('Enter your zipcode:', validators=[Required()])
    submit = SubmitField('Submit')

    def validate_zip(self, field):
        if len(field.data) != 5:
            raise ValidationError("Your zipcode must be 5 characters.")


@app.route('/zipcode', methods = ['GET', "POST"])
def zip_form():
    form = WeatherForm()
    if request.method == "POST" and form.validate_on_submit():
        zip = form.zip.data
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        params_d = {}
        params_d['zip'] = zip
        params_d['APPID'] = "0d9812cdf147283843e5761877f1f57b"
        req = requests.get(base_url, params=params_d)
        res = json.loads(req.text)
        name = res['name']
        des = res['weather'][0]['description']
        temp = res['main']['temp']
        converted_temp = str(((int(temp)) * (9/5)) - 459.67).split('.')[0]
        return render_template('weather_results.html', name=name, des=des, temp=converted_temp)
    flash(form.errors)
    return render_template('zipform.html', form=form)


if __name__ == "__main__":
    app.run(use_reloader=True,debug=True)
