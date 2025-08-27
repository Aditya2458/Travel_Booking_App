# Travel Booking Web App

A Django-based web application to browse, filter, and book travel options such as flights, trains, and buses. Users can register, log in, manage profiles, view bookings, and cancel them. Built with Bootstrap 5 for a modern, responsive design.

<img width="1467" height="743" alt="Screenshot 2025-08-28 at 1 53 15 AM" src="https://github.com/user-attachments/assets/e2727999-7f81-4fc2-9ff2-08c9cbfee5e8" />

<img width="1467" height="743" alt="Screenshot 2025-08-28 at 1 53 46 AM" src="https://github.com/user-attachments/assets/7f2fe8e8-3ac6-4c1c-8af3-3ef6116fae97" />
---

## Features

- User authentication (register, login, logout)  
- Browse travel options with filters (type, source, destination, date)  
- Book available travel options  
- View and cancel bookings  
- Profile update  
- Pagination for travel listings  
- Responsive UI with Bootstrap 5  

---

## Technologies Used

- Django  
- Python 3.x  
- Bootstrap 5  
- SQLite (default) / any other relational DB  
- HTML, CSS, JavaScript  

---

## Setup Instructions

1. **Clone the repository**  

```bash
git clone <your-repo-url>
cd <your-project-folder>
```
# Travel Booking Web App

A Django-based web application to browse, filter, and book travel options such as flights, trains, and buses. Users can register, log in, manage profiles, view bookings, and cancel them. Built with Bootstrap 5 for a modern, responsive design.

---

## Features

- User authentication (register, login, logout)  
- Browse travel options with filters (type, source, destination, date)  
- Book available travel options  
- View and cancel bookings  
- Profile update  
- Pagination for travel listings  
- Responsive UI with Bootstrap 5  

---

## Technologies Used

- Django  
- Python 3.x  
- Bootstrap 5  
- SQLite (default) / any other relational DB  
- HTML, CSS, JavaScript  

---

## Setup Instructions

1. **Clone the repository**  

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

Create a virtual environment
```
python -m venv venv
```
Activate the virtual environment
On Windows:
```
venv\Scripts\activate
```
On Mac/Linux:
```
source venv/bin/activate
```
Install dependencies
```
pip install -r requirements.txt
```
Apply migrations
```
python manage.py makemigrations
python manage.py migrate
```
Create a superuser (for admin access)
```
python manage.py createsuperuser
```
Run the development server
```
python manage.py runserver
```
Access the app
```
User interface: http://127.0.0.1:8000/
Admin panel: http://127.0.0.1:8000/admin/
```


Folder Structure
```
travel_booking/
│
├─ bookings/           # Django app
│  ├─ templates/       # HTML templates
│  ├─ static/          # CSS, JS, images
│  ├─ models.py        # Models
│  ├─ views.py         # Views
│  └─ forms.py         # Forms
├─ travel_booking/     # Project settings
│  ├─ settings.py
│  └─ urls.py
├─ manage.py
└─ requirements.txt
```
<img width="1467" height="743" alt="Screenshot 2025-08-28 at 1 54 02 AM" src="https://github.com/user-attachments/assets/222ac543-edcd-49da-9c45-1a9a05fe460d" />
<img width="1467" height="743" alt="Screenshot 2025-08-28 at 1 54 16 AM" src="https://github.com/user-attachments/assets/6151dcf8-d9b8-43d6-9739-d74fe9944032" />

<img width="1467" height="743" alt="Screenshot 2025-08-28 at 1 54 31 AM" src="https://github.com/user-attachments/assets/46f786f3-6909-4ff6-8943-1c96bd3a3e65" />





