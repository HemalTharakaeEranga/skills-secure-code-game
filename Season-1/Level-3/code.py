import os
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    TaxPayer('foo', 'bar').get_tax_form_attachment(request.args["input"])
    TaxPayer('foo', 'bar').get_prof_picture(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

class TaxPayer:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.prof_picture = None
        self.tax_form_attachment = None

    def get_prof_picture(self, path=None):
        if not path:
            return None

        # Defend against path traversal attacks
        if path.startswith('/') or '..' in path:
            return None

        base_dir = os.path.dirname(os.path.abspath(__file__))
        prof_picture_path = os.path.normpath(os.path.join(base_dir, path))

        # Ensure the path is within the allowed directory
        if not prof_picture_path.startswith(base_dir):
            return None

        try:
            with open(prof_picture_path, 'rb') as pic:
                picture = bytearray(pic.read())
            return prof_picture_path
        except Exception as e:
            return None

    def get_tax_form_attachment(self, path=None):
        if not path:
            raise Exception("Error: Tax form is required for all users")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        tax_form_path = os.path.normpath(os.path.join(base_dir, path))

        # Ensure the path is within the allowed directory
        if not tax_form_path.startswith(base_dir):
            return None

        try:
            with open(tax_form_path, 'rb') as form:
                tax_data = bytearray(form.read())
            return tax_form_path
        except Exception as e:
            return None