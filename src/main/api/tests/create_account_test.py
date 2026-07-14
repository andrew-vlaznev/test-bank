import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from sqlalchemy.orm import Session
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.user_steps.create_account(
            create_user_request
        )

        assert response.id is not None

        assert response.balance == 0

        account_from_db = Account.get_account_by_id(
            db_session,
            response.id
        )

        assert account_from_db is not None, "Аккаунт не создан в БД"
        assert account_from_db.id == response.id
        assert account_from_db.balance == 0