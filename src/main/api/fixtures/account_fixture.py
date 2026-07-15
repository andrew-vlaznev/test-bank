import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest


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