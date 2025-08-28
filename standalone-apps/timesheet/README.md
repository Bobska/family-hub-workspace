# Django Timesheet App

A comprehensive time tracking application built with Django 5.2+ that allows users to manage their work hours across multiple job locations.

## 🚀 Features

### Core Functionality
- **Job Management**: Create and manage multiple work locations
- **Time Entry Tracking**: Log daily work hours with start/end times
- **Break Time Support**: Account for break periods (0-120 minutes)
- **Overlap Prevention**: Automatic validation to prevent overlapping time entries
- **User Authentication**: Secure user accounts with data isolation

### User Interface
- **Dashboard**: Quick overview with today's entries and quick entry form
- **Daily Entry**: Detailed view for any date with full entry management
- **Weekly Summary**: Visual week view with daily breakdowns
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **AJAX Validation**: Real-time overlap checking and form validation

### Administrative Features
- **Django Admin Integration**: Full admin interface for data management
- **User Data Isolation**: Users only see their own jobs and entries
- **Comprehensive Filtering**: Admin filters by user, job, and date
- **Audit Trail**: Creation and modification timestamps

## 📋 Requirements

- Python 3.10+
- Django 5.1+
- python-decouple 3.8+
- Bootstrap 5 (CDN)
- Font Awesome 6 (CDN)

## 🛠 Installation & Setup

### 1. Clone and Navigate
```bash
cd standalone-apps/timesheet
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver 8001
```

### 6. Access Application
- **Main App**: http://127.0.0.1:8001/
- **Admin Interface**: http://127.0.0.1:8001/admin/

## 📱 Application Structure

### Models

#### Job Model
- **name**: Job/location name (required, max 200 chars)
- **address**: Optional full address for reference
- **user**: Foreign key to Django User model
- **created_at/updated_at**: Automatic timestamps

#### TimeEntry Model
- **user**: Foreign key to Django User model
- **job**: Foreign key to Job model
- **date**: Work date
- **start_time/end_time**: Work period times
- **break_duration**: Break time in minutes (0, 15, 30, 45, 60, 90, 120)
- **total_hours()**: Calculated method returning decimal hours

### Views & Templates

#### Dashboard (`/`)
- Today's time entries overview
- Quick entry form for current date
- Daily statistics and quick navigation
- **Template**: `timesheet/dashboard.html`

#### Daily Entry (`/daily/`)
- Date picker for any date
- Full time entry form
- Table view of day's entries
- Entry editing and deletion
- **Template**: `timesheet/daily_entry.html`

#### Weekly Summary (`/weekly/`)
- 7-day calendar view
- Daily totals and weekly summary
- Navigation between weeks
- Print-friendly styling
- **Template**: `timesheet/weekly_summary.html`

#### Job Management (`/jobs/`)
- List all user's jobs
- Job creation and editing
- Job statistics and recent entries
- **Templates**: `job_list.html`, `job_form.html`, `job_delete.html`

### Forms

#### TimeEntryForm
- Full time entry form with all fields
- User-filtered job choices
- Time validation and overlap checking
- Bootstrap 5 styling

#### QuickTimeEntryForm
- Simplified form for dashboard
- Pre-filled with current date
- Quick time entry workflow

#### JobForm
- Job creation and editing
- Name validation and address handling

### URL Patterns
```python
/                     # Dashboard
/daily/               # Daily entry view
/weekly/              # Weekly summary
/jobs/                # Job list
/jobs/add/           # Create job
/jobs/<id>/edit/     # Edit job
/jobs/<id>/delete/   # Delete job (with confirmation)
/entries/<id>/edit/  # Edit time entry
/entries/<id>/delete/ # Delete time entry (with confirmation)
/api/validate-overlap/ # AJAX overlap validation
```

## 🎨 UI/UX Features

### Design System
- **Color Scheme**: Purple gradient primary theme
- **Typography**: Bootstrap 5 system fonts
- **Icons**: Font Awesome 6 icons throughout
- **Responsive**: Mobile-first design approach

### Interactive Elements
- **Real-time Validation**: AJAX overlap checking
- **Auto-calculation**: Live hour calculation on forms
- **Confirmation Dialogs**: JavaScript confirmations for deletions
- **Date Navigation**: Previous/next day and week buttons
- **Print Support**: Print-optimized weekly summary

### User Experience
- **Intuitive Navigation**: Clear breadcrumbs and back buttons
- **Smart Defaults**: Auto-fill current time and date
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback for actions
- **Empty States**: Helpful guidance when no data exists

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

### Database Configuration
The app uses SQLite by default. For production, update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'timesheet_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Job creation with validation
- [ ] Time entry creation and validation
- [ ] Overlap prevention working
- [ ] Dashboard quick entry
- [ ] Daily view navigation
- [ ] Weekly summary display
- [ ] Entry editing and deletion
- [ ] Admin interface functionality

### Test Data Creation
```python
# Create test user
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.create_user('testuser', 'test@example.com', 'password')

# Create test job
from timesheet_app.models import Job
job = Job.objects.create(name='Test Office', address='123 Main St', user=user)

# Create test time entry
from timesheet_app.models import TimeEntry
from datetime import date, time
entry = TimeEntry.objects.create(
    user=user,
    job=job,
    date=date.today(),
    start_time=time(9, 0),
    end_time=time(17, 0),
    break_duration=60
)
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure ALLOWED_HOSTS
- [ ] Set secure SECRET_KEY
- [ ] Enable HTTPS
- [ ] Set up backup strategy
- [ ] Configure logging

### Static Files
```bash
python manage.py collectstatic
```

## 🤝 Integration with FamilyHub

This standalone app is designed for integration into the larger FamilyHub project:

1. **Copy App**: Move `timesheet_app` to `FamilyHub/apps/`
2. **Update Settings**: Add to `INSTALLED_APPS` as `'apps.timesheet'`
3. **Include URLs**: Add to main `urls.py`
4. **Update Templates**: Extend FamilyHub base template
5. **Migrate Database**: Run migrations in main project

## 📚 API Documentation

### AJAX Endpoints

#### Overlap Validation
- **URL**: `/api/validate-overlap/`
- **Method**: POST
- **Parameters**: 
  - `date`: Work date (YYYY-MM-DD)
  - `start_time`: Start time (HH:MM)
  - `end_time`: End time (HH:MM)
  - `entry_id`: Optional, for editing existing entries
- **Response**: `{"valid": true/false, "message": "error message"}`

## 🐛 Troubleshooting

### Common Issues

**Import Error on Startup**
- Ensure `timesheet_app` is in `INSTALLED_APPS`
- Check Python path and virtual environment

**Database Errors**
- Run `python manage.py makemigrations`
- Run `python manage.py migrate`
- Check database permissions

**Static Files Not Loading**
- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATICFILES_DIRS` settings

**Template Not Found**
- Verify template directory structure
- Check `TEMPLATES` setting in `settings.py`

### Debug Mode
Enable debug toolbar for development:
```python
# Add to INSTALLED_APPS
'debug_toolbar',

# Add to MIDDLEWARE
'debug_toolbar.middleware.DebugToolbarMiddleware',
```

## 📝 License

This project is part of the FamilyHub family management platform. See main project for licensing information.

## 👥 Contributing

1. Follow Django best practices
2. Use PEP 8 style guidelines
3. Add tests for new features
4. Update documentation
5. Test across different browsers

## 📞 Support

For issues and feature requests, please use the main FamilyHub project repository issue tracker.

---

**Built with ❤️ using Django & Bootstrap**  
*Part of the FamilyHub Family Management Platform*
