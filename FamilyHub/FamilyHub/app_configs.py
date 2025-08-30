"""
Application configuration for Docker vs Local deployment detection.
"""

import environ

# Initialize django-environ
env = environ.Env()

# Detect if running in Docker container
IS_DOCKER = env.bool('IS_DOCKER', default=False)

# Template configuration based on deployment environment
def get_template_dirs(base_dir):
    """
    Return template directories based on deployment environment.
    
    Args:
        base_dir: Django BASE_DIR path
        
    Returns:
        List of template directories
    """
    template_dirs = [base_dir / 'templates']
    
    if IS_DOCKER:
        # In Docker, timesheet app is available in the container
        template_dirs.append(base_dir.parent / 'timesheet_app' / 'templates')
    else:
        # Local development might use standalone timesheet templates
        template_dirs.append(base_dir.parent / 'timesheet_app' / 'templates')
    
    return template_dirs
