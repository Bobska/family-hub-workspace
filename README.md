# FamilyHub - Multi-App Web Platform

## Overview
FamilyHub is a comprehensive family management platform consisting of multiple standalone Django applications that can run independently or as part of an integrated system.

## Applications
- **Timesheet** - Time tracking and management
- **Daycare Invoice** - Daycare billing and invoice tracking
- **Employment History** - Career and job history management
- **Upcoming Payments** - Payment scheduling and reminders
- **Credit Card Management** - Credit card tracking and management
- **Household Budget** - Family budget planning and tracking

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL (for production)
- Git

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd family-hub-workspace
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements/development.txt
```

4. Set up environment variables:
```bash
cp FamilyHub/.env.example FamilyHub/.env
# Edit .env with your settings
```

5. Run migrations:
```bash
cd FamilyHub
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## Development

### Working on Individual Apps
```bash
cd standalone-apps/timesheet
python manage.py runserver 8001
```

### Working on FamilyHub (All Apps)
```bash
cd FamilyHub
python manage.py runserver
```

## Testing
```bash
python manage.py test
```

## License
Private Project - All Rights Reserved
