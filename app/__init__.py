from flask import Flask 

app = Flask(__name__)
app.secret_key = 'my_unobvious_secret_key'






from app import view
from app import error_handlers

from app import etfe_arch
from app import uvalue

