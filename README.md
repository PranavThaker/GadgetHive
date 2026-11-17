# GadgetHive

A full-stack electronics e-commerce website built with Django 5.1. It supports browsing products by category, searching, a session/user-aware shopping cart, checkout into orders, and basic account management.

## Features

- **Product catalog** — categories and products with images, pricing, stock, and active/inactive status.
- **Browsing & search** — home page listing active products, per-category pages, and keyword search across product name/description.
- **Shopping cart** — works for both logged-in users and anonymous visitors (tracked via session key); add, remove, and clear items.
- **Checkout & orders** — authenticated checkout converts the current cart into an `Order` with line-item `OrderItem`s and a computed total; users can view their order history and order details.
- **User accounts** — registration (Django's built-in `UserCreationForm`), login/logout, and a profile page backed by an extended `UserProfile` (phone, address, city, state, pincode).
- **Demo data seeding** — a management command generates sample categories/products (Mobiles, Laptops, Accessories) with placeholder SVG images, for quick local demos.
- **Django admin** — all models are registered for management via `/admin/`.

## Tech Stack

- **Backend:** Django 5.1
- **Database:** SQLite (default, via `db.sqlite3`)
- **Frontend:** Django templates + a single `static/styles.css`
- **Images:** Django `ImageField` (requires Pillow)

## Project Structure

```
GadgetHive/
├── GadgetHive/          # Project settings, root URLconf, WSGI/ASGI entrypoints
├── store/               # Categories, products, home/category/product/search views
│   └── management/commands/seed_demo_data.py   # Demo data seeder
├── cart/                # Session- and user-aware shopping cart
├── orders/              # Checkout flow, order history and details
├── users/               # Registration, login/logout, profile
├── templates/           # Base template + shared partials
├── static/styles.css    # Site-wide styles
└── manage.py
```

### Apps at a glance

| App | Models | Key URLs |
|---|---|---|
| `store` | `Category`, `Product` | `/`, `/category/<slug>/`, `/product/<slug>/`, `/search/` |
| `cart` | `CartItem` | `/cart/`, `/cart/add/<product_id>/`, `/cart/remove/<item_id>/`, `/cart/clear/` |
| `orders` | `Order`, `OrderItem` | `/orders/`, `/orders/checkout/`, `/orders/<pk>/`, `/orders/success/<pk>/` |
| `users` | `UserProfile` | `/users/register/`, `/users/login/`, `/users/logout/`, `/users/profile/` |

## Requirements

- Python 3.10+
- Django 5.1.x
- Pillow (for product image uploads)

> Note: this project doesn't ship a `requirements.txt`. Install the two packages above directly, or generate one with `pip freeze > requirements.txt` after installing them.

## Setup

1. **Clone the repository and set up a virtual environment:**

   ```bash
   git clone https://github.com/PranavThaker/GadgetHive
   cd GadgetHive-main/GadgetHive
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install django pillow
   ```

3. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

4. **Create an admin user (optional, for `/admin/`):**

   ```bash
   python manage.py createsuperuser
   ```

5. **Seed demo products (optional):**

   ```bash
   python manage.py seed_demo_data
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000/` in your browser.
