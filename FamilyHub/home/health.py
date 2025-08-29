"""
Health check views for FamilyHub monitoring and load balancer checks.
"""

import os
import psutil
from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.core.cache import cache
from django.conf import settings


class HealthCheckView(View):
    """
    Comprehensive health check endpoint for monitoring and load balancers.
    Returns JSON with system status information.
    """
    
    def get(self, request):
        """Return health status of the application."""
        health_data = {
            'status': 'healthy',
            'timestamp': self._get_timestamp(),
            'version': getattr(settings, 'FAMILYHUB_SETTINGS', {}).get('VERSION', '1.0.0'),
            'checks': {}
        }
        
        # Database check
        health_data['checks']['database'] = self._check_database()
        
        # Cache check
        health_data['checks']['cache'] = self._check_cache()
        
        # Disk usage check
        health_data['checks']['disk'] = self._check_disk_usage()
        
        # Memory check
        health_data['checks']['memory'] = self._check_memory()
        
        # Determine overall status
        all_healthy = all(
            check['status'] == 'healthy' 
            for check in health_data['checks'].values()
        )
        
        if not all_healthy:
            health_data['status'] = 'unhealthy'
            return JsonResponse(health_data, status=503)
        
        return JsonResponse(health_data)
    
    def _get_timestamp(self):
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()
    
    def _check_database(self):
        """Check database connectivity."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            return {
                'status': 'healthy',
                'message': 'Database connection successful'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Database connection failed: {str(e)}'
            }
    
    def _check_cache(self):
        """Check cache connectivity."""
        try:
            test_key = 'health_check_test'
            test_value = 'test_value'
            cache.set(test_key, test_value, 30)
            retrieved_value = cache.get(test_key)
            cache.delete(test_key)
            
            if retrieved_value == test_value:
                return {
                    'status': 'healthy',
                    'message': 'Cache connection successful'
                }
            else:
                return {
                    'status': 'unhealthy',
                    'message': 'Cache test failed'
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Cache connection failed: {str(e)}'
            }
    
    def _check_disk_usage(self):
        """Check disk usage."""
        try:
            disk_usage = psutil.disk_usage('/')
            usage_percent = (disk_usage.used / disk_usage.total) * 100
            
            threshold = getattr(settings, 'HEALTH_CHECK', {}).get('DISK_USAGE_MAX', 90)
            
            if usage_percent < threshold:
                return {
                    'status': 'healthy',
                    'usage_percent': round(usage_percent, 2),
                    'message': f'Disk usage: {usage_percent:.1f}%'
                }
            else:
                return {
                    'status': 'unhealthy',
                    'usage_percent': round(usage_percent, 2),
                    'message': f'Disk usage too high: {usage_percent:.1f}%'
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Disk check failed: {str(e)}'
            }
    
    def _check_memory(self):
        """Check memory usage."""
        try:
            memory = psutil.virtual_memory()
            available_mb = memory.available / (1024 * 1024)
            
            threshold = getattr(settings, 'HEALTH_CHECK', {}).get('MEMORY_MIN', 100)
            
            if available_mb > threshold:
                return {
                    'status': 'healthy',
                    'available_mb': round(available_mb, 2),
                    'usage_percent': round(memory.percent, 2),
                    'message': f'Memory available: {available_mb:.0f}MB'
                }
            else:
                return {
                    'status': 'unhealthy',
                    'available_mb': round(available_mb, 2),
                    'usage_percent': round(memory.percent, 2),
                    'message': f'Low memory: {available_mb:.0f}MB available'
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Memory check failed: {str(e)}'
            }


class ReadinessCheckView(View):
    """
    Readiness check for Kubernetes/container orchestration.
    Quick check to determine if the application is ready to serve traffic.
    """
    
    def get(self, request):
        """Return readiness status."""
        try:
            # Quick database check
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            return JsonResponse({
                'status': 'ready',
                'timestamp': self._get_timestamp()
            })
        except Exception as e:
            return JsonResponse({
                'status': 'not_ready',
                'message': str(e),
                'timestamp': self._get_timestamp()
            }, status=503)
    
    def _get_timestamp(self):
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()


class LivenessCheckView(View):
    """
    Liveness check for Kubernetes/container orchestration.
    Simple check to determine if the application is alive.
    """
    
    def get(self, request):
        """Return liveness status."""
        return JsonResponse({
            'status': 'alive',
            'timestamp': self._get_timestamp()
        })
    
    def _get_timestamp(self):
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()
