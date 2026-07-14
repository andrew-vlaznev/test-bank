from src.main.api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.specs.response_specs import ResponseSpecs


class TestDepositAccount:
    def test_deposit_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        create_account_response = api_manager.user_steps.create_account(create_user_request)

        amount = 1000.5

        deposit_request = DepositRequest(
            accountId=create_account_response.id,
            amount=amount
        )

        deposit_response = api_manager.user_steps.deposit(
            create_user_request,
            deposit_request
        )

        old_balance = create_account_response.balance
        expected_balance = old_balance + amount

        assert deposit_response.id == deposit_request.accountId
        assert deposit_response.balance == expected_balance

        account_from_db = Account.get_account_by_id(
            db_session,
            create_account_response.id
        )

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.balance == expected_balance


    def test_deposit_other_user_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        user1_request = create_user_request
        user2_request = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(user2_request)

        user1_account_response = api_manager.user_steps.create_account(user1_request)

        deposit_request = DepositRequest(
            accountId=user1_account_response.id,
            amount=1000
        )

        response = api_manager.user_steps.deposit(
            user2_request,
            deposit_request,
            ResponseSpecs.request_not_found()
        )

        assert "does not belong" in response.json()["error"]

        account_from_db = Account.get_account_by_id(
            db_session,
            user1_account_response.id
        )

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.balance == 0




