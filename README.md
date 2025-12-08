# todo-list-toliq

# Todo List API (Django REST Framework)

Oddiy, tez va zamonaviy Todo ilovasi. Foydalanuvchilar roʻyxatdan oʻtib, oʻz vazifalarini boshqarishi mumkin.

## Texnologiyalar
- Python 3.9+
- Django 4.x / 5.x
- Django REST Framework
- SQLite (development) / PostgreSQL (production tavsiya etiladi)
- Simple TokenAudentification (token autentifikatsiya)

## Xususiyatlar
- Foydalanuvchi registratsiyasi va login
- TokenAudentification bilan himoyalangan API
- Todo yaratish, oʻqish, yangilash, oʻchirish (CRUD)
- Todo holati: bajarildi / bajarilmadi
- Qidiruv va filterlash
- Admin panel

---

## API Endpointlar

### Auth (Autentifikatsiya)

| Method | Endpoint                          | Tavsif                          | Kerakli ruxsat         |
|--------|------------------------------------|----------------------------------|-------------------------|
| POST   | `/api/auth/register/`              | Yangi foydalanuvchi yaratish    | Hammaga ochiq           |
| POST   | `/api/auth/login/`                 | Login → access va refresh token | Hammaga ochiq           |
| POST   | `/api/auth/logout/`         | chiqish       | tokenni ochirish           |

### Todo (Vazifalar)

| Method | Endpoint                          | Tavsif                                    | Kerakli ruxsat          |
|--------|------------------------------------|-------------------------------------------|--------------------------|
| GET    | `/api/todos/`                      | Barcha todolarni olish (oʻziniki)         | Authenticated           |
| GET    | `/api/todos/?search=matn`          | Qidiruv (title yoki description boʻyicha) | Authenticated           |
| GET    | `/api/todos/?completed=true`       | Faqat bajarilganlar                       | Authenticated           |
| GET    | `/api/todos/?completed=false`      | Faqat bajarilmaganlar                     | Authenticated           |
| POST   | `/api/todos/`                      | Yangi todo yaratish                       | Authenticated           |
| GET    | `/api/todos/<id>/`                 | Bitta todoni koʻrish                      | Owner yoki Admin        |
| PUT    | `/api/todos/<id>/`                 | Toʻliq yangilash                          | Owner yoki Admin        |
| PATCH  | `/api/todos/<id>/`                 | Qisman yangilash (masalan, faqat status)  | Owner yoki Admin        |
| DELETE | `/api/todos/<id>/`                 | Todoni oʻchirish                          | Owner yoki Admin        |

---

## Misol soʻrovlar (cURL)

### 1. Roʻyxatdan oʻtish
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ali",
    "password": "12345678",
    "password2": "12345678",
    "email": "ali@example.com"
  }'
