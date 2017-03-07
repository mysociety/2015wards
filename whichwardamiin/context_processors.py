from django.conf import settings

def add_settings( request ):
    """Add some selected settings values to the context"""
    return {
        'settings': {
            'GOOGLE_ANALYTICS_ACCOUNT': settings.GOOGLE_ANALYTICS_ACCOUNT,
            'DEBUG': settings.DEBUG,
            'ELECTION_DATE': settings.ELECTION_DATE,
            'ELECTION_YEAR': settings.ELECTION_YEAR,
        }
    }
