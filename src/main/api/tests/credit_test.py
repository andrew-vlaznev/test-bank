from src.main.api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.specs.response_specs import ResponseSpecs


class TestCreditAccount:
    def test_credit_account_valid(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest):
        create_account_response = api_manager.user_steps.create_account(create_credit_user_request)

        amount = 5000

        term_months = 12

        credit_request = CreditRequest(
            accountId=create_account_response.id,
            amount=amount,
            termMonths=term_months
        )

        credit_response = api_manager.user_steps.credit(
            create_credit_user_request,
            credit_request
        )

        old_balance = create_account_response.balance
        expected_balance = old_balance + amount

        assert credit_response.id == credit_request.accountId
        assert credit_response.amount == amount
        assert credit_response.termMonths == credit_request.termMonths
        assert credit_response.balance == expected_balance
        assert credit_response.creditId is not None

        account_from_db = Account.get_account_by_id(
            db_session,
            create_account_response.id
        )

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.balance == expected_balance


    def test_credit_account_invalid(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest):
        create_account_response = api_manager.user_steps.create_account(create_credit_user_request)

        amount = 5000

        term_months = 12

        credit_request = CreditRequest(
            accountId=create_account_response.id,
            amount=amount,
            termMonths=term_months
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

        assert "Only one active credit allowed per user" in credit_response_2.json()["error"]
        assert credit_response_1.balance == amount

        account_from_db = Account.get_account_by_id(
            db_session,
            create_account_response.id
        )

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.balance == amount




