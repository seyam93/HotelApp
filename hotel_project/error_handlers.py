from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

def handler404(request, exception=None):
    logger.error(f"404 error occurred: {exception}")
    try:
        return render(request, '404.html', {'hotel': None}, status=404)
    except Exception as e:
        logger.error(f"Error rendering 404 template: {e}")
        return render(request, '404.html', {'hotel': None, 'error': str(e)}, status=404)

def handler500(request, exception=None):
    logger.error(f"500 error occurred: {exception}")
    return render(request, '500.html', {'hotel': None}, status=500)

def handler403(request, exception=None):
    logger.error(f"403 error occurred: {exception}")
    return render(request, '403.html', {'hotel': None}, status=403)

def handler400(request, exception=None):
    logger.error(f"400 error occurred: {exception}")
    return render(request, '400.html', {'hotel': None}, status=400) 