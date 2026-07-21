from src.main.api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.generators.request_generator import RequestGenerator

class TestDepositAccount:
    def test_deposit_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, account: CreateAccountResponse):

        deposit_request = RequestGenerator.deposit(
            account.id,
            amount=1000.5
        )

        deposit_response = api_manager.user_steps.deposit(
            create_user_request,
            deposit_request
        )

        old_balance = account.balance
        expected_balance = old_balance + deposit_request.amount

        assert deposit_response.id == account.id, "Неверный id счета"
        assert deposit_response.balance == expected_balance, "Баланс после пополнения неверный"

        account_from_db = Account.get_account_by_id(
            db_session,
            account.id
        )

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.balance == expected_balance, "Баланс в БД не совпадает"


    def test_deposit_other_user_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, account: CreateAccountResponse):
        user2_request = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(user2_request)

        deposit_request = RequestGenerator.deposit(
            account.id
        )

        response = api_manager.user_steps.deposit(
            user2_request,
            deposit_request,
            ResponseSpecs.request_not_found()
        )

        assert "does not belong" in response.json()["error"], "Получено неверное сообщение об ошибке"

        account_from_db = Account.get_account_by_id(
            db_session,
            account.id
        )

        old_balance = account.balance

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.balance == old_balance, "Баланс изменился после попытки пополнить чужой счет"




