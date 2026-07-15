from src.main.api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.generators.request_generator import RequestGenerator


class TestCreditAccount:
    def test_credit_account_valid(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, credit_account: CreateAccountResponse):

        credit_request = RequestGenerator.credit(
            credit_account.id
        )

        credit_response = api_manager.user_steps.credit(
            create_credit_user_request,
            credit_request
        )

        old_balance = credit_account.balance
        expected_balance = old_balance + credit_request.amount

        assert credit_response.id == credit_account.id, "Получен неверный accountId"
        assert credit_response.amount == credit_request.amount, "Получена неверная сумма кредита"
        assert credit_response.balance == expected_balance, "Баланс после выдачи кредита рассчитан неверно"

        assert credit_response.creditId is not None, "Не создан кредит"

        account_from_db = Account.get_account_by_id(
            db_session,
            credit_account.id
        )

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.balance == expected_balance, "Баланс в БД не соответствует ожидаемому"


    def test_credit_account_invalid(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, credit_account: CreateAccountResponse):

        credit_request = RequestGenerator.credit(
            credit_account.id
        )

        credit_response_1 = api_manager.user_steps.credit(
            create_credit_user_request,
            credit_request
        )

        credit_response_2 = api_manager.user_steps.credit(
            create_credit_user_request,
            credit_request,
            ResponseSpecs.request_not_found()
        )

        assert "Only one active credit allowed per user" in credit_response_2.json()["error"], "Получено неверное сообщение об ошибке"

        account_from_db = Account.get_account_by_id(
            db_session,
            credit_account.id
        )

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.balance == credit_response_1.balance, "Баланс изменился после повторной попытки взять кредит"




