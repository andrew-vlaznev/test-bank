import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.request_generator import RequestGenerator


@pytest.fixture
def account(api_manager: ApiManager, create_user_request: CreateUserRequest) -> CreateAccountResponse:
    return api_manager.user_steps.create_account(create_user_request)


@pytest.fixture
def credit_account(api_manager: ApiManager, create_credit_user_request: CreateUserRequest) -> CreateAccountResponse:
    return api_manager.user_steps.create_account(create_credit_user_request)

@pytest.fixture
def two_accounts(api_manager: ApiManager, create_user_request: CreateUserRequest):
    first_account = api_manager.user_steps.create_account(create_user_request)
    second_account = api_manager.user_steps.create_account(create_user_request)
    return first_account, second_account

@pytest.fixture
def two_accounts_with_balance(api_manager: ApiManager, create_user_request: CreateUserRequest, two_accounts):
    sender_account, receiver_account = two_accounts
    deposit_request = RequestGenerator.deposit(sender_account.id)
    api_manager.user_steps.deposit(create_user_request, deposit_request)
    return sender_account, receiver_account, deposit_request

@pytest.fixture
def account_with_balance(api_manager: ApiManager, create_user_request: CreateUserRequest, account: CreateAccountResponse):
    deposit_request = RequestGenerator.deposit(account.id)
    api_manager.user_steps.deposit(create_user_request, deposit_request)
    return account, deposit_request

@pytest.fixture
def credit_with_deposit(api_manager: ApiManager, create_credit_user_request: CreateUserRequest, credit_account: CreateAccountResponse):
    credit_request = RequestGenerator.credit(credit_account.id)
    credit_response = api_manager.user_steps.credit(create_credit_user_request, credit_request)
    deposit_request = RequestGenerator.deposit(credit_account.id, amount=credit_request.amount)
    api_manager.user_steps.deposit(create_credit_user_request, deposit_request)
    return credit_account, credit_request, credit_response

@pytest.fixture
def second_user_account(api_manager: ApiManager, second_user: CreateUserRequest) -> CreateAccountResponse:
    return api_manager.user_steps.create_account(second_user)