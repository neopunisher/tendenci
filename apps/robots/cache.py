from django.core.cache import cache

CACHE_PRE_KEY = "robots"

def cache_all_robots():
    """ Caches all query of robots """
    from robots.models import Robot
    key = [CACHE_PRE_KEY, 'all']
    key = '.'.join(key)
    
    robots = Robot.objects.all()
    is_set = cache.add(key, robots)
    if not is_set:
        cache.set(key, robots)