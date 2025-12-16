# Sports Competition Management System

## Project Overview

This is a Django-based sports competition management system for managing sports competitions, participant registration, and user permission control.

## Tech Stack

- Django
- Python
- SQLite (Development Environment)

## Project Route Description

### Main Route Configuration (`sports_competition/urls.py`)

The main route configuration file of the project, containing the following routes:

| Route Path | Description | View/Function |
|------------|-------------|---------------|
| `/admin/` | Django Admin Panel | `admin.site.urls` |
| `/` | Root path, includes all routes from competitions app | `include('competitions.urls')` |
| `/accounts/login/` | User Login Page | Django built-in `LoginView` |
| `/accounts/logout/` | User Logout | Django built-in `LogoutView` |

---

### Competitions App Routes (`competitions/urls.py`)

All routes related to competition management:

#### 1. Competition List Page
- **Path**: `/`
- **View Function**: `competition_list`
- **Route Name**: `competition_list`
- **Features**: 
  - Display all competition list
  - Support search functionality (by name, description, location)
  - Support filtering by sport type and status
  - Regular users can only view public competitions
  - Users with permissions can create new competitions
- **Permission Required**: None (Public access)

#### 2. User Login
- **Path**: `/login/`
- **View Function**: `custom_login`
- **Route Name**: `custom_login`
- **Features**: User login page
- **Permission Required**: None

#### 3. User Logout
- **Path**: `/logout/`
- **View Function**: `custom_logout`
- **Route Name**: `custom_logout`
- **Features**: User logout and redirect to competition list
- **Permission Required**: None

#### 4. Create New Competition
- **Path**: `/competition/new/`
- **View Function**: `competition_create`
- **Route Name**: `competition_create`
- **Features**: Create a new competition
- **Permission Required**: 
  - Login required
  - Requires `competitions.can_create_competition` permission

#### 5. Competition Detail Page
- **Path**: `/competition/<int:pk>/`
- **View Function**: `competition_detail`
- **Route Name**: `competition_detail`
- **Parameters**: `pk` - Competition primary key ID
- **Features**: 
  - Display competition detailed information
  - Show whether user is registered
  - Display edit/delete buttons based on permissions
  - Display register button (if user has permission and registration is open)
- **Permission Required**: 
  - Public competitions: None
  - Private competitions: Requires `competitions.can_view_all` permission

#### 6. Edit Competition
- **Path**: `/competition/<int:pk>/edit/`
- **View Function**: `competition_edit`
- **Route Name**: `competition_edit`
- **Parameters**: `pk` - Competition primary key ID
- **Features**: Edit existing competition information
- **Permission Required**: 
  - Login required
  - Requires `competitions.can_edit_competition` permission **OR** is the competition creator

#### 7. Delete Competition
- **Path**: `/competition/<int:pk>/delete/`
- **View Function**: `competition_delete`
- **Route Name**: `competition_delete`
- **Parameters**: `pk` - Competition primary key ID
- **Features**: Delete competition (requires confirmation)
- **Permission Required**: 
  - Login required
  - Requires `competitions.can_delete_competition` permission **OR** is the competition creator

#### 8. Register Participant
- **Path**: `/competition/<int:pk>/register/`
- **View Function**: `register_participant`
- **Route Name**: `register_participant`
- **Parameters**: `pk` - Competition primary key ID
- **Features**: 
  - Register current logged-in user as competition participant
  - Check if registration is open
  - Check if there are available slots
  - Prevent duplicate registration
- **Permission Required**: 
  - Login required
  - Requires `competitions.can_register_participant` permission

---

## Permission System

The project uses Django's permission system, main permissions include:

- `competitions.can_view_all` - View all competitions (including private ones)
- `competitions.can_create_competition` - Create competitions
- `competitions.can_edit_competition` - Edit competitions
- `competitions.can_delete_competition` - Delete competitions
- `competitions.can_register_participant` - Register participants

---

## Route Structure Diagram

```
/
├── admin/                          # Django Admin Panel
├── accounts/
│   ├── login/                      # User Login
│   └── logout/                     # User Logout
└── (competitions app routes)
    ├── /                           # Competition List (Homepage)
    ├── login/                      # Custom Login Page
    ├── logout/                     # Custom Logout
    └── competition/
        ├── new/                    # Create New Competition
        ├── <pk>/                   # Competition Detail
        ├── <pk>/edit/              # Edit Competition
        ├── <pk>/delete/            # Delete Competition
        └── <pk>/register/          # Register Participant
```

---

## Installation and Running

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Database Migration

```bash
python manage.py migrate
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to view the application.

---

## Notes

1. **Web Environment Limitations**: Sensor features (such as accelerometer) are only available on mobile devices (iOS/Android), not supported in web browsers.
2. **Permission Control**: Ensure proper user permission configuration, otherwise some features may not be accessible.
3. **Database**: The project uses SQLite as the development database. For production environments, it is recommended to use PostgreSQL or MySQL.

---

## Developers

Project maintained by the development team.
