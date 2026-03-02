# Mama's Mina - Restaurant Marocain

## 1. Project Overview

**Project Name:** Mama's Mina  
**Type:** Restaurant Management Web Application  
**Framework:** Django 4.x with Python 3.11  
**Core Functionality:** A complete restaurant solution with public menu browsing, cart/ordering system for clients, and staff management dashboard with real-time order tracking.

---

## 2. UI/UX Specification

### Color Palette
| Role | Color | Hex Code |
|------|-------|----------|
| Primary (Terracotta) | Rich Moroccan Red | #9C4221 |
| Secondary (Blue Majorelle) | Deep Blue | #5D8AA8 |
| Accent (Gold) | Warm Gold | #D4AF37 |
| Background | Cream White | #FAF8F5 |
| Text Primary | Dark Brown | #2C1810 |
| Text Secondary | Warm Gray | #6B5B4F |

### Typography
- **Headings:** "Playfair Display" (elegant serif)
- **Body:** "Nunito" (modern readable sans-serif)
- **Accent/Logo:** "Cinzel Decorative" (decorative)

### Visual Elements
- Zellige geometric patterns as subtle borders/backgrounds
- Warm, photo-focused card design for dishes
- Elegant Moroccan arches in section dividers
- Smooth animations on hover and transitions

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

---

## 3. Functionality Specification

### A. Public Interface (Client - No Login Required)

#### Menu Browsing
- Display categories: Méchoui, Tajines, Pastillas, Couscous, Entrées, Desserts, Boissons
- Each dish shows: photo, name, description, price
- Filter by category
- Search functionality

#### Shopping Cart
- Add/remove items
- Adjust quantities
- View total
- Persists in session (localStorage)

#### Order Simulation
- Enter table number
- Add special instructions
- Submit order → generates order ID
- Simulated payment flow

### B. Staff Interface (Login Required)

#### Authentication
- Google OAuth2 login (django-allauth)
- Staff-only access to dashboard

#### Menu Management (CRUD)
- Create/Read/Update/Delete dishes
- Create/Read/Update/Delete categories
- Image upload for dishes

#### Order Management
- Real-time dashboard view
- Order status: En préparation → Prêt → Servi → Payé
- Status updates with timestamps
- Kitchen view and Service view

---

## 4. Data Models

### Category
- name (CharField)
- description (TextField)
- display_order (IntegerField)
- is_active (BooleanField)

### Dish
- name (CharField)
- description (TextField)
- price (DecimalField)
- category (ForeignKey)
- image (ImageField)
- is_available (BooleanField)
- created_at (DateTimeField)

### Order
- order_id (CharField, unique)
- table_number (IntegerField)
- items (JSONField)
- total_amount (DecimalField)
- status (CharField: pending, preparing, ready, served, paid)
- special_instructions (TextField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

### OrderItem
- order (ForeignKey)
- dish (ForeignKey)
- quantity (IntegerField)
- unit_price (DecimalField)

---

## 5. Application Structure

```
restaurant-mina/
├── manage.py
├── requirements.txt
├── mama_mina/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── signals.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── menu.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_confirmed.html
│   ├── dashboard/
│   │   ├── base_dashboard.html
│   │   ├── orders.html
│   │   ├── menu_management.html
│   │   └── kitchen_view.html
│   └── includes/
│       ├── navbar.html
│       ├── footer.html
│       └── dish_card.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

---

## 6. Acceptance Criteria

### Public Side
- [ ] Menu displays with all categories and dishes
- [ ] Dishes show photos, names, descriptions, prices
- [ ] Cart functionality works (add, remove, update quantity)
- [ ] Order can be placed with table number
- [ ] Payment simulation completes successfully
- [ ] Order confirmation displayed with order ID

### Staff Side
- [ ] Google login works correctly
- [ ] Dashboard shows real-time orders
- [ ] Can create/edit/delete dishes
- [ ] Can create/edit/delete categories
- [ ] Order status can be updated
- [ ] Kitchen view shows pending orders

### Visual
- [ ] Moroccan color palette applied correctly
- [ ] Zellige patterns visible as accents
- [ ] Responsive on mobile and tablet
- [ ] Smooth animations and transitions
- [ ] Professional, elegant appearance
