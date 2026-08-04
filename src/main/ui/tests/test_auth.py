from dbm.sqlite3 import error

import pytest
from playwright.sync_api import expect
from ui.pages.login_page import LoginPage
from ui.pages.catalog_page import CatalogPage
from ui.steps.login_steps import LoginSteps

def test_auth(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")

    # Проверяем, что мы на странице каталога после успешного логина
    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0, "Ожидаем товары на странице каталога"

def test_login_locked_out_user(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")

    # Получаем текст ошибки и assert в тесте
    error_text = steps.login_page.get_error_text()
    assert "locked out" in error_text, "Ожидаем сообщение о заблокированном пользователе"

def test_logout(page):
    login = LoginSteps(page)
    catalog = CatalogPage(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    assert catalog.get_products_count() > 0, "Ожидаем что в каталоге есть товары"

    catalog.logout()
    assert page.url == "https://www.saucedemo.com", "Ожидаем возврат на страницу логина"

def test_logout_visual_user(page):
    login = LoginSteps(page)
    catalog = CatalogPage(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    assert catalog.get_products_count() > 0, "Ожидаем что в каталоге есть товары"

    catalog.logout()
    assert page.url == login.LOGIN_URL, "Ожидаем возврат на страницу логина"
