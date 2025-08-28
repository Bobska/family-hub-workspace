from django.shortcuts import render
from datetime import datetime

def home_dashboard(request):
    """Main dashboard view showing all apps overview"""
    
    # Prepare app cards with their information
    apps = [
        {
            'name': 'Timesheet',
            'icon': '⏰',
            'description': 'Track your work hours and projects',
            'url': '/timesheet/',
            'color': 'primary'
        },
        {
            'name': 'Household Budget',
            'icon': '💰',
            'description': 'Manage family finances and budgets',
            'url': '/budget/',
            'color': 'success'
        },
        {
            'name': 'Daycare Invoices',
            'icon': '🧒',
            'description': 'Track daycare bills and payments',
            'url': '/daycare/',
            'color': 'info'
        },
        {
            'name': 'Employment History',
            'icon': '💼',
            'description': 'Your career journey and records',
            'url': '/employment/',
            'color': 'warning'
        },
        {
            'name': 'Upcoming Payments',
            'icon': '📅',
            'description': 'Never miss a payment deadline',
            'url': '/payments/',
            'color': 'danger'
        },
        {
            'name': 'Credit Cards',
            'icon': '💳',
            'description': 'Manage credit cards and limits',
            'url': '/creditcards/',
            'color': 'secondary'
        },
    ]
    
    context = {
        'apps': apps,
        'user': request.user,
        'today': datetime.now(),
    }
    
    return render(request, 'home/dashboard.html', context)
