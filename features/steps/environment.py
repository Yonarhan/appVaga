# features/environment.py

from django.test.client import Client

def before_scenario(context):

    context.client = Client()
    context.form_data = {}