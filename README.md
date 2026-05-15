# 🍔 Eatero - Modern Food Delivery Platform


**Eatero** is a premium, full-stack food delivery application built with Django. It features a stunning, modern user interface, robust administrative controls, and a seamless customer experience with integrated online payments.

---

## ✨ Key Features

### 🛒 Customer Experience
- **Premium UI**: Modern, responsive design using Glassmorphism and Poppins typography.
- **Restaurant Discovery**: Browse curated lists of restaurants with ratings and cuisine types.
- **Dynamic Cart**: Real-time cart management with price calculation.
- **Flexible Payments**: Choose between **Razorpay Online Payment** or **Cash on Delivery (COD)**.
- **Order Summary**: Detailed post-purchase breakdown with delivery tracking status.
- **Robust Validation**: Secure signup and sign-in with advanced form validation.

### 🛠️ Admin Dashboard
- **Restaurant Management**: Full CRUD operations for restaurant profiles.
- **Menu Control**: Easily add, edit, or delete menu items with vegetarian/non-vegetarian badges.
- **Analytics-ready**: Structured data models for restaurants, items, and customers.

---

## 🚀 Tech Stack

- **Backend**: Django 6.0.4 (Python)
- **Database**: SQLite 3 (Development)
- **Frontend**: Vanilla CSS3, HTML5, JavaScript (ES6+)
- **Payments**: Razorpay API Integration
- **Design Language**: Modern Premium (Custom CSS system)

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dhreetigithub3/Eatero.git
   cd Eatero
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install django razorpay
   ```

4. **Run Migrations**:
   ```bash
   python eatero/manage.py migrate
   ```

5. **Start the Server**:
   ```bash
   python eatero/manage.py runserver
   ```

---
6. **Live Demo**
- https://eatero.onrender.com/

## 🔒 Security Best Practices Implemented
- [x] Django CSRF Protection on all forms.
- [x] Robust server-side form validation for user inputs.
- [x] Dynamic pre-filling of payment data to prevent user error.
- [x] Forced evaluation of order items before cart clearing to ensure data persistence.

---

## 🗺️ Roadmap
- [ ] Migrate to Django Built-in User Auth.
- [ ] Implement Password Hashing.
- [ ] Environment variable support for API keys.
- [ ] Real-time order tracking with WebSockets.

---

Developed with ❤️ by [Dhreeti](https://github.com/dhreetigithub3)
