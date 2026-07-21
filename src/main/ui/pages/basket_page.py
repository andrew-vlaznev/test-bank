from playwright.sync_api import Page, expect

class BasketPage:
    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.locator(".shopping_cart_link")
        self.item_cards = page.locator(".cart_item")
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.error_message = page.locator('[data-test="error"]')

    def open_cart(self):
        """Переход в корзину через иконку"""
        self.cart_link.click()

    def checkout(self):
        """Нажать Checkout и перейти на страницу checkout"""
        self.checkout_button.click()

    def remove_item(self, product_name: str):
        """Удаляем товар по имени"""
        card = self.item_cards.filter(has_text=product_name)
        expect(card).to_be_visible()

    def expect_item_not_in_cart(self, product_name: str):
        """Проверяемб что товар отсутствует в корзине"""
        card = self.item_cards.filter(has_text=product_name)
        expect(card).to_be_visible()

    def get_item_names(self) -> list[str]:
        """Возвращает список названий товаров в корзине"""
        return self.item_cards.locator(".inventory_item_name").all_text_contents()

    def get_items_total_price(self) -> float:
        prices_text = self.item_cards.locator(".inventory_item_total_price").all_text_contents()
        return sum(float(p.replace("$", "")) for p in prices_text)