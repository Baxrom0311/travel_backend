# 🏛️ Visit Khorezm — Backend API

Xorazm viloyati turizm portali uchun to'liq RESTful API. Django + DRF asosida qurilgan.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![DRF](https://img.shields.io/badge/DRF-3.17-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🏨 **Hotels** — Mehmonxonalar (narx, reyting, qulayliklar, rasmlar)
- 🕌 **Attractions** — Diqqatga sazovor joylar (gallery, video, tarix)
- 🍽️ **Restaurants** — Restoranlar (oshxona turlari, narx diapazoni)
- 🎫 **Tours** — Turlar va ekskursiyalar (itinerary, narxlar)
- 🎉 **Events** — Tadbirlar va festivallar
- 📰 **News** — Yangiliklar va maqolalar
- 🚕 **Transport** — Aeroport transport yo'nalishlari
- ⭐ **Reviews** — Generic reviews (barcha modellar uchun)
- 📧 **Newsletter** — Email obuna
- 📬 **Contact** — Aloqa formasi (throttle bilan)
- 🔍 **Global Search** — Barcha kontent turlari bo'yicha qidiruv
- 🌐 **i18n** — 3 til: O'zbek, English, Русский

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/visit-khorezm-backend.git
cd visit-khorezm-backend

# 2. Virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Environment
cp .env.example .env
# .env fayldagi qiymatlarni o'zgartiring

# 5. Database setup
python manage.py migrate
python manage.py loaddata initial_data.json

# 6. Import images & demo data
python manage.py import_hotel_photos
python manage.py seed_attraction_images
python manage.py seed_demo_data
python manage.py seed_extras

# 7. Create admin user
python manage.py createsuperuser

# 8. Run server
python manage.py runserver
```

Server: `http://127.0.0.1:8000`

## 📡 API Endpoints

### Core
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/` | API overview |
| GET | `/api/home/` | Bosh sahifa aggregated data |
| GET | `/api/search/?q=...` | Global qidiruv |
| GET | `/health/` | Health check |

### Hotels
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/hotels/` | Mehmonxonalar ro'yxati |
| GET | `/api/hotels/{id}/` | Bitta mehmonxona |
| GET | `/api/hotels/{id}/related/` | O'xshash mehmonxonalar |
| GET | `/api/hotels/stats/` | Statistika |
| GET | `/api/hotels/options/` | Filter options |
| GET | `/api/amenities/` | Qulayliklar |

**Filters:** `city`, `featured`, `stars`, `search`, `amenity`, `min_price`, `max_price`, `ordering`

### Attractions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/attractions/` | Joylar ro'yxati |
| GET | `/api/attractions/{id}/` | Bitta joy (gallery bilan) |
| GET | `/api/attractions/{id}/related/` | O'xshash joylar |
| GET | `/api/attractions/options/` | Options |

### Restaurants
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/restaurants/` | Restoranlar |
| GET | `/api/restaurants/{id}/` | Bitta restoran |
| GET | `/api/restaurants/cuisines/` | Oshxona turlari |
| GET | `/api/restaurants/options/` | Filter options |

### Tours
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tours/` | Turlar |
| GET | `/api/tours/{slug}/` | Bitta tur (detail) |

### Events & News
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/events/` | Tadbirlar |
| GET | `/api/events/{id}/` | Tadbir tafsiloti |
| GET | `/api/news/` | Yangiliklar |
| GET | `/api/news/{slug}/` | Yangilik tafsiloti |

### Transport
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/transport/` | Yo'nalishlar |
| GET | `/api/transport/{id}/` | Bitta yo'nalish |

### Reviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/reviews/` | Sharh qoldirish |
| GET | `/api/reviews/{type}/{id}/` | Sharhlar ro'yxati |

### Newsletter
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/newsletter/subscribe/` | Obuna |
| POST | `/api/newsletter/unsubscribe/` | Bekor qilish |

### Contact
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/contact/` | Xabar yuborish (5/hour throttle) |

## 🌐 Language Support

Har bir endpoint `?lang=uz|en|ru` parametrini qabul qiladi:

```bash
GET /api/hotels/?lang=en
GET /api/home/?lang=ru
```

## 🏗️ Architecture

```
backend/
├── config/           # Django sozlamalari
├── core/             # Home, search, API overview
├── hotels/           # Mehmonxonalar + amenities + contact
├── attractions/      # Diqqatga sazovor joylar
├── restaurants/      # Restoranlar
├── tours/            # Turlar
├── events/           # Tadbirlar
├── news/             # Yangiliklar
├── transport/        # Transport yo'nalishlari
├── reviews/          # Generic reviews
├── newsletter/       # Email obuna
├── contact/          # Contact form
├── utils/            # Helpers (lang, pagination, etc.)
├── media/            # Uploaded images
├── manage.py
└── requirements.txt
```

## 🔧 Environment Variables

`.env` faylida sozlang:

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost

# CORS
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourfrontend.com

# Pagination
API_PAGE_SIZE=20
API_MAX_PAGE_SIZE=100

# Throttle
CONTACT_THROTTLE_RATE=5/hour
```

## 📚 API Documentation

Interactive Swagger UI:
```
http://127.0.0.1:8000/api/docs/
```

Schema JSON:
```
http://127.0.0.1:8000/api/schema/
```

## 🛠️ Management Commands

```bash
# Hotel rasmlari import
python manage.py import_hotel_photos
python manage.py import_hotel_photos --clear

# Attraction rasmlari
python manage.py seed_attraction_images

# Events va News demo
python manage.py seed_demo_data

# Restaurants va Tours demo
python manage.py seed_extras
```

## 🔐 Admin Panel

```
http://127.0.0.1:8000/admin/
```

Admin'da boshqarish mumkin:
- Barcha modellar (CRUD)
- Rasm preview va inline edit
- Reviews moderatsiya
- Newsletter obunachilar
- Contact xabarlar

## 🧪 Testing

```bash
python manage.py test
```

## 📦 Deployment

### Production Checklist
- [ ] `DEBUG=False`
- [ ] `SECRET_KEY` env'dan
- [ ] `ALLOWED_HOSTS` sozlangan
- [ ] `CORS_ALLOWED_ORIGINS` sozlangan
- [ ] PostgreSQL database
- [ ] Static files: `collectstatic`
- [ ] Media files: S3 yoki local
- [ ] Gunicorn + Nginx
- [ ] HTTPS (Let's Encrypt)

### Docker (kelajakda)
```bash
docker-compose up -d
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | Django 6.0 |
| API | Django REST Framework 3.17 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| CORS | django-cors-headers |
| Images | Pillow |
| Documentation | drf-spectacular (OpenAPI) |
| Config | python-decouple |

## 📄 License

MIT License

## 👥 Contributing

Pull requests welcome! Major changes - avval issue oching.

## 📞 Contact

Email: info@visitkhorezm.uz
Website: https://visitkhorezm.uz
