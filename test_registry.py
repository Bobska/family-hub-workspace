from FamilyHub.app_registry import app_registry

print('=== APP REGISTRY STATUS ===')
dashboard_data = app_registry.get_dashboard_data()
for app in dashboard_data:
    print(f'App: {app["name"]}')
    print(f'  Available: {app["available"]}')
    print(f'  URLs Available: {app["urls_available"]}')
    print(f'  URL: {app["url"]}')
    print(f'  Status: {app["status"]}')
    print()
