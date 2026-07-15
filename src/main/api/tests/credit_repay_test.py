from src.main.api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.generators.request_generator import RequestGenerator


class TestCreditRepayAccount:
    def test_credit_account_valid(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, credit_account: CreateAccountResponse):

        credit_request = RequestGenerator.credit(
            credit_account.id
        )

        credit_response = api_manager.user_steps.credit(
            create_credit_user_request,
            credit_request
        )

        deposit_request = RequestGenerator.deposit(
            credit_account.id,
            amount=credit_request.amount
        )

        api_manager.user_steps.deposit(
            create_credit_user_request,
            deposit_request
        )

        credit_repay_request = RequestGenerator.repay(
            credit_account.id,
            credit_response.creditId,
            amount=credit_request.amount
        )

        credit_repay_response = api_manager.user_steps.credit_repay(
            create_credit_user_request,
            credit_repay_request
        )

        expected_balance = credit_account.balance + credit_request.amount

        assert credit_repay_response.creditId == credit_response.creditId, "Неверный идентификатор кредита"
        assert credit_repay_response.amountDeposited == credit_request.amount, "Неверная сумма погашения"

        account_from_db = Account.get_account_by_id(
            db_session,
            credit_account.id
        )

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.balance == expected_balance, "Баланс в БД не совпадает после погашения кредита"


    def test_credit_account_invalid(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, credit_account: CreateAccountResponse):

        credit_request = RequestGenerator.credit(
            credit_account.id
        )

        credit_response = api_manager.user_steps.credit(
            create_credit_user_request,
            credit_request
        )

        deposit_request = RequestGenerator.deposit(
            credit_account.id,
            amount=credit_request.amount
        )

        api_manager.user_steps.deposit(
            create_credit_user_request,
            deposit_request
        )

        credit_repay_request = RequestGenerator.repay(
            credit_account.id,
            credit_response.creditId,
            amount=credit_request.amount
        )

        credit_repay_response = api_manager.user_steps.credit_repay(
            create_credit_user_request,
            credit_repay_request
        )

        second_repay_response = api_manager.user_steps.credit_repay(
            create_credit_user_request,
            credit_repay_request,
            ResponseSpecs.request_conflict()
        )

        assert "The credit has already been repaid" in second_repay_response.json()["error"], "Получено неверное сообщение об ошибке"

        account_from_db = Account.get_account_by_id(
            db_session,
            credit_account.id
        )

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.balance == credit_request.amount, "Баланс изменился после повторного погашения кредита"


