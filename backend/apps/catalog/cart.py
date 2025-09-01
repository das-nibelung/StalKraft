from decimal import Decimal
from .models import Product

CART_SESSION_KEY = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product_id: int, qty: int = 1, replace: bool = False):
        pid = str(product_id)
        if pid not in self.cart:
            self.cart[pid] = {"qty": 0}
        self.cart[pid]["qty"] = qty if replace else self.cart[pid]["qty"] + qty
        self.save()

    def remove(self, product_id: int):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def __len__(self):
        return sum(item["qty"] for item in self.cart.values())

    def items(self):
        pids = self.cart.keys()
        products = Product.objects.filter(id__in=pids)
        for p in products:
            qty = self.cart[str(p.id)]["qty"]
            yield {
                "product": p,
                "qty": qty,
                "subtotal": (p.price or Decimal("0")) * qty,
            }

    def save(self):
        self.session.modified = True
