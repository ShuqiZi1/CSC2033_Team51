from flask import Blueprint, render_template, request
from contact.forms import ContactForm
import csv
from pathlib import Path

contact_blueprint = Blueprint('contact', __name__, template_folder='templates')

# Allows user to create a contact form with name email and message, then they're returned to the home page


@contact_blueprint.route('/contact', methods=['GET', 'POST'])
def contact():
    # create contact form object
    form = ContactForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        # contact message file store path
        CONTACT_DIR = Path(__file__).resolve().parent.parent.joinpath('contact.csv')
        f = open(CONTACT_DIR, "a", newline='')
        writer = csv.writer(f)
        contact_massage = list()
        contact_massage.append(form.name.data)
        contact_massage.append(form.email.data)
        contact_massage.append(form.message.data)
        writer.writerow(contact_massage)
        f.close()
        return render_template('index.html')
    return render_template('contact_us.html',form=form)
    # Loads contact us page so the user can create a form

