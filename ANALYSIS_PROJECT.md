# Project analysis: DjangoPro/eatero (delivery app)

## 1) What the project is
A small Django project (`DjangoPro/eatero`) with one main app: `delivery`.
It implements a basic “food delivery / restaurant + menu + cart” flow.

## 2) Key files
- `delivery/models.py`
- `delivery/views.py`
- `delivery/urls.py`
- `delivery/Templates/*.html`
- `eatero/settings.py`

## 3) Data model (ORM)
### `Customer`
Fields:
- `username`, `password`, `email`, `mobile`, `address` (all `CharField`)

### `Restaurant`
Fields:
- `name`
- `picture` (`URLField`, default to a URL)
- `cuisine`
- `rating` (`FloatField`)

### `Item`
Fields:
- `restaurant` FK → `Restaurant` (`related_name="items"`)
- `name`, `description`
- `price` (`FloatField`)
- `vegeterian` (`BooleanField`, default `False`)
- `picture` (`URLField`, default to a URL)

### `Cart`
Fields:
- `customer` FK → `Customer` (`related_name="cart"`)
- `items` M2M → `Item` (`related_name="carts"`)
- `total_price()` sums `item.price` for items in the cart

## 4) Request handling / views
Implemented as function-based views in `delivery/views.py`.

### Public pages
- `say_hello` → renders `index.html`
- `open_signup` → `signup.html`
- `open_signin` → `signin.html`

### Authentication (custom, not Django auth)
- `signup`:
  - POST fields create a `Customer`
  - attempts to prevent duplicate username via `try/except` around `Customer.objects.get(username=...)`
  - on duplicate returns `HttpResponse("Duplicate username!")`
- `signin`:
  - POST username/password
  - `Customer.objects.get(username=username, password=password)`
  - if username == `'admin'` → `admin_home.html`
  - else → `customer_home.html` with `restaurantList` and `username`
  - on `Customer.DoesNotExist` → `fail.html`

### Admin/restaurant management
- `open_add_restaurant` → `add_restaurant.html`
- `add_restaurant`:
  - POST creates `Restaurant` if no duplicate name
  - otherwise returns `HttpResponse("Duplicate restaurant!")`
- `open_show_restaurant` → `show_restaurants.html`
- `open_update_restaurant` / `update_restaurant`
- `delete_restaurant`

### Menu/item management
- `open_update_menu` / `update_menu`:
  - list items for a restaurant
  - POST creates new `Item` (duplicate-check by `Item.objects.get(name=name)`)
- `open_edit_item` / `edit_item`
- `delete_item_menu`

### Customer browsing & cart
- `view_menu(restaurant_id, username)` → `customer_menu.html`
- `add_to_cart(item_id, username)`:
  - fetches item + customer
  - `Cart.objects.get_or_create(customer=customer)`
  - adds item to cart
  - returns `show_cart`
- `show_cart(username)`:
  - fetches customer
  - fetches cart if present and computes total via `cart.total_price()`
  - renders `cart.html`
- `delete_item_cart(item_id, username)`:
  - fetches item + customer
  - removes item from that customer’s cart

## 5) URL routing
Defined in `delivery/urls.py` and included in `eatero/urls.py`.
It exposes endpoints for signup/signin, restaurant CRUD, item CRUD, and cart actions.

## 6) Templates (example)
- `Templates/cart.html` renders:
  - `itemList` with `item.picture`, `item.name`, `item.description`, `item.price`
  - delete link: `{% url 'delete_item_cart' item.id username %}`
  - total: `{{ total_price }}`

## 7) Main quality/security concerns
1. **Plaintext passwords**
   - `Customer.password` stored as plain text.
   - signin compares plaintext password directly.
2. **Admin privilege is unreliable**
   - admin access is determined by `username == 'admin'`.
   - any user choosing that username can get admin UI logic.
3. **Broad `except:` blocks**
   - duplicate checks use `except:` which can mask unrelated errors.
4. **Fragile signin variables**
   - if request isn’t POST, `username/password` may be undefined but are still used.
5. **No CSRF protection explicitly handled in templates**
   - CSRF middleware exists, so templates must use `{% csrf_token %}` on POST forms.
   - (Not verified here; should be checked in each HTML template.)
6. **Ownership checks missing for deletions**
   - deletion methods assume the item belongs to the user’s context.
   - e.g., cart item removal fetches item by id, then removes from cart without verifying membership.

## 8) Overall assessment
- **Architecture:** very straightforward CRUD + cart implemented directly in views.
- **Data modeling:** relationships (Restaurant→Item, Customer→Cart, Cart→Item M2M) are consistent.
- **Production-readiness:** limited due to custom auth, plaintext passwords, and missing guardrails.

