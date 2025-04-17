from behave import given, when, then
from pages.register_page import Register_Page

@given('I am on the registration page')
def step_impl(context):
    registration_url = f"{context.base_url}customer/account/create/"
    if not hasattr(context, "page") or context.page is None:
        raise RuntimeError("context.page is not initialized")
    context.register_page = Register_Page(context.page)
    context.register_page.goto(registration_url)


@when('I fill in the registration form with valid data')
def step_fill_registration_form(context):
    for row in context.table:
        first_name = row['first_name']
        last_name = row['last_name']
        email = row['email']
        password = row['password']

        context.register_page.register(first_name, last_name, email, password)


@when('I submit the form')
def step_submit_form(context):
    context.register_page.submit_form()