# FamilyHub Architecture Reference Document

## Project Overview

**Project Name**: FamilyHub  
**Type**: Multi-Application Family Management Platform  
**Architecture Pattern**: Hub-and-Spoke with Unified Navigation  
**Technology Stack**: Django, Bootstrap 5, PostgreSQL/SQLite  

## Core Architecture Principles

### 1. Hub-and-Spoke Model
- **Hub**: Central FamilyHub dashboard acts as the main entry point
- **Spokes**: Individual applications (Timesheet, Budget, Daycare, etc.)
- **Integration**: Apps can run standalone OR integrated within FamilyHub
- **Data Sharing**: Shared user authentication, optional cross-app data access

### 2. Template Inheritance Hierarchy
```
FamilyHub/templates/base.html (Master Template)
    ├── FamilyHub/templates/app_base.html (App Container Template)
    │   ├── apps/timesheet/templates/timesheet/base.html
    │   ├── apps/budget/templates/budget/base.html
    │   └── apps/daycare/templates/daycare/base.html
    └── FamilyHub/home/templates/home/dashboard.html
```

### 3. Navigation Architecture

#### Two-Tier Navigation System
- **Tier 1 - Global Navigation** (Always Visible)
  - FamilyHub brand/logo (links to main dashboard)
  - App switcher (horizontal tabs or dropdown)
  - User account menu (profile, settings, logout)
  - Notification bell (future feature)

- **Tier 2 - App Navigation** (Context-Sensitive)
  - Visible only when inside an app
  - App-specific menu items
  - Subordinate to global navigation
  - Maintains app context

#### Navigation State Management
- Active app highlighting in global nav
- Active page highlighting in app nav
- Breadcrumb trail for deep navigation
- Mobile-responsive hamburger menu

### 4. URL Structure Convention

```
/                                   # FamilyHub main dashboard
/accounts/login/                    # Authentication
/accounts/logout/                   
/accounts/profile/                  

/timesheet/                         # Timesheet dashboard
/timesheet/entries/daily/           # Daily entries
/timesheet/entries/weekly/          # Weekly summary
/timesheet/jobs/                    # Job management
/timesheet/jobs/add/               
/timesheet/jobs/<id>/edit/         

/budget/                            # Budget dashboard
/budget/transactions/               # Transaction list
/budget/categories/                 # Category management
/budget/reports/                    # Financial reports

/daycare/                           # Daycare dashboard
/daycare/invoices/                  # Invoice list
/daycare/payments/                  # Payment tracking
/daycare/providers/                 # Provider management
```

### 5. Application Structure

#### Directory Organization
```
family-hub-workspace/
├── FamilyHub/                      # Main hub project
│   ├── FamilyHub/                  # Project configuration
│   │   ├── settings.py            
│   │   ├── urls.py                # Root URL configuration
│   │   └── wsgi.py
│   ├── home/                       # Dashboard application
│   ├── apps/                       # Integrated applications
│   │   ├── timesheet_app/         
│   │   ├── budget_app/            
│   │   └── daycare_app/           
│   ├── templates/                  # Global templates
│   │   ├── base.html              # Master base template
│   │   └── app_base.html          # App container template
│   ├── static/                     # Global static files
│   │   ├── css/                   
│   │   │   └── familyhub.css     # Global styles
│   │   ├── js/                    
│   │   │   └── familyhub.js      # Global JavaScript
│   │   └── img/                   # Global images/icons
│   └── media/                      # User uploads
└── standalone-apps/                # Standalone versions
    ├── timesheet/                  
    ├── budget/                     
    └── daycare/                    
```

### 6. Design System Architecture

#### Visual Hierarchy
- **Primary Brand Color**: Gradient (#667eea to #764ba2)
- **Typography Scale**: Consistent font sizes (12, 14, 16, 18, 24, 32px)
- **Spacing System**: 4px base unit (4, 8, 16, 24, 32, 48px)
- **Component Library**: Bootstrap 5 with custom overrides

#### CSS Architecture
- **Global Styles**: `FamilyHub/static/css/familyhub.css`
- **App-Specific Styles**: `apps/[app_name]/static/[app_name]/css/app.css`
- **CSS Variables**: Design tokens for consistency
- **Mobile-First**: Responsive breakpoints (576px, 768px, 992px, 1200px)

### 7. Data Architecture

#### User Model
- Django's built-in User model
- Extended with UserProfile for additional fields
- Single sign-on across all apps

#### App Data Isolation
- Each app manages its own models
- Foreign keys to User for ownership
- Optional cross-app relationships through interfaces

#### Database Strategy
- Development: SQLite
- Production: PostgreSQL
- Migrations: Managed per app
- Backup: Daily automated backups

### 8. Integration Patterns

#### App Registration
- Apps register themselves with FamilyHub
- Provide metadata (name, icon, description, color)
- Define navigation menu items
- Specify required permissions

#### Context Processors
- `familyhub_context`: Provides global navigation data
- `app_context`: Provides current app information
- `user_context`: Provides user preferences and permissions

#### Middleware
- `AppDetectionMiddleware`: Identifies current app from URL
- `NavigationMiddleware`: Builds navigation structure
- `ThemeMiddleware`: Handles user theme preferences

### 9. Authentication & Authorization

#### Authentication Flow
- Centralized login/logout
- Session-based authentication
- Optional "Remember Me" functionality
- Password reset via email

#### Authorization Levels
- **Superuser**: Full system access
- **Staff**: Admin panel access
- **App-specific roles**: Defined per application
- **Family sharing**: Future feature for multi-user families

### 10. Deployment Architecture

#### Development Environment
- Local Django development server
- SQLite database
- Debug mode enabled
- Hot reload for templates/static files

#### Production Environment
- Docker containerization
- Nginx reverse proxy
- Gunicorn WSGI server
- PostgreSQL database
- Static files served by Nginx
- Media files in persistent volume

#### Docker Structure
```
services:
  - familyhub (Django application)
  - postgres (Database)
  - nginx (Web server)
  - redis (Cache - future)
```

### 11. Static File Management

#### Collection Strategy
- Global static files in `FamilyHub/static/`
- App static files in `apps/[app_name]/static/[app_name]/`
- Collected to `STATIC_ROOT` for production
- Served by Nginx in production

#### Media File Handling
- User uploads to `MEDIA_ROOT`
- Organized by app and date
- Backup strategy for user data
- CDN integration (future)

### 12. Template Block Structure

#### Master Base Template Blocks
- `{% block title %}` - Page title
- `{% block extra_css %}` - Additional CSS
- `{% block navigation %}` - Navigation area
- `{% block app_navigation %}` - App-specific navigation
- `{% block breadcrumb %}` - Breadcrumb trail
- `{% block content %}` - Main content area
- `{% block extra_js %}` - Additional JavaScript

### 13. JavaScript Architecture

#### Module Structure
- Global utilities in `familyhub.js`
- App-specific code in app directories
- Event-driven architecture
- AJAX for dynamic updates

#### Third-party Libraries
- Bootstrap 5 JavaScript
- Bootstrap Icons
- Font Awesome (optional)
- Chart.js (for dashboards)

### 14. API Architecture (Future)

#### RESTful Endpoints
- `/api/v1/` - API root
- `/api/v1/apps/` - Available applications
- `/api/v1/[app_name]/` - App-specific endpoints

#### Authentication
- Token-based for API access
- Session-based for web interface
- OAuth2 for third-party integrations (future)

### 15. Testing Architecture

#### Test Levels
- Unit tests per app
- Integration tests for app interactions
- End-to-end tests for user flows
- Performance tests for scalability

#### Test Organization
- Tests located in `apps/[app_name]/tests/`
- Shared test utilities in `FamilyHub/tests/`
- Fixtures for test data
- CI/CD integration

### 16. Documentation Structure

#### Code Documentation
- Docstrings for all classes and methods
- Type hints for function parameters
- Inline comments for complex logic

#### User Documentation
- README.md in each app directory
- User guides in `docs/user/`
- API documentation (when implemented)
- Architecture documentation (this document)

### 17. Version Control Strategy

#### Branch Structure
- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Emergency fixes

#### Commit Conventions
- Conventional commits format
- Clear, descriptive messages
- Reference issue numbers
- Atomic commits

### 18. Performance Considerations

#### Optimization Strategies
- Database query optimization (select_related, prefetch_related)
- Template caching for static content
- Static file minification
- Lazy loading for images
- Pagination for large datasets

#### Monitoring
- Application performance monitoring
- Error tracking and logging
- User analytics (privacy-conscious)
- Database query analysis

### 19. Security Architecture

#### Security Measures
- CSRF protection on all forms
- XSS prevention through template escaping
- SQL injection prevention via ORM
- Secure password hashing
- HTTPS enforcement in production
- Regular security updates

#### Data Protection
- User data encryption at rest
- Secure session management
- Personal data anonymization
- GDPR compliance considerations

### 20. Scalability Considerations

#### Horizontal Scaling
- Stateless application design
- Session storage in cache (Redis)
- Database read replicas
- Load balancing ready

#### Vertical Scaling
- Resource monitoring
- Database optimization
- Caching strategies
- CDN for static assets

## Architecture Decision Records (ADRs)

### ADR-001: Hub-and-Spoke Architecture
**Decision**: Use hub-and-spoke pattern for app integration
**Rationale**: Allows apps to function independently while providing unified experience
**Consequences**: More complex navigation but better modularity

### ADR-002: Template Inheritance Strategy
**Decision**: Three-level template hierarchy
**Rationale**: Provides flexibility while maintaining consistency
**Consequences**: Clear separation of concerns, easier maintenance

### ADR-003: Two-Tier Navigation
**Decision**: Implement global and app-specific navigation layers
**Rationale**: Users need context at both platform and app levels
**Consequences**: More complex navigation but better user orientation

### ADR-004: CSS Design Tokens
**Decision**: Use CSS variables for design system
**Rationale**: Single source of truth for styling
**Consequences**: Easier theme management and consistency

### ADR-005: Django Built-in Features
**Decision**: Maximize use of Django's built-in functionality
**Rationale**: Reduce custom code, improve maintainability
**Consequences**: Faster development, better stability

## Maintenance Notes

### Regular Tasks
- Weekly dependency updates
- Monthly security patches
- Quarterly performance review
- Annual architecture review

### Monitoring Checklist
- Application logs
- Error rates
- Performance metrics
- User feedback
- Security alerts

## Future Enhancements

### Planned Features
- Real-time notifications
- Mobile applications
- API for third-party integrations
- Advanced reporting
- Multi-language support
- Theme customization
- Family sharing features

### Technical Debt
- Refactor legacy code
- Improve test coverage
- Optimize database queries
- Update documentation
- Standardize error handling

---

**Document Version**: 1.0.0  
**Last Updated**: Current  
**Status**: Active Architecture  
**Review Cycle**: Quarterly