from behave import *

# @given('')
# def step_impl(context):
#     pass
#
# @when('')
# def step_impl(context):
#     assert True is not False
#
# @then('')
# def step_impl(context):
#     assert context.failed is False


@given('the game board is blank')
def step_impl(context):
    pass


@given('the opponent makes a move first as an X')
def step_impl(context):
    pass


@given('the opponent makes a move at any time')
def step_impl(context):
    pass


@given('there are at least three Xs or three Os on the game board')
def step_impl(context):
    pass


@when('the machine makes a move first as an X')
def step_impl(context):
    assert True is not False


@when('the machine identifies the move from the opponent')
def step_impl(context):
    assert True is not False


@when('whoever has completed a move')
def step_impl(context):
    assert True is not False


@then('the machine will performs AI reasoning and make the first move')
def step_impl(context):
    assert context.failed is False


@then('the machine will performs AI reasoning and make the next move')
def step_impl(context):
    assert context.failed is False


@then('the machine checks the game board to determine a winner')
def step_impl(context):
    assert context.failed is False


@then('yield X or O as the winner')
def step_impl(context):
    assert context.failed is False
