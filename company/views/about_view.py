from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import About
from rest_framework import status
from datetime import datetime
import logging
logger = logging.getLogger('ecommerce')
class AboutFooterView(APIView):
    def get(self, request):
        cache_key = 'about'
        print("Logging test")
        logger.debug("DEBUG")
        logger.info("INFO")
        logger.warning("WARNING")
        logger.error("ERROR")
        logger.critical("CRITICAL")
        about = cache.get(cache_key)
        if not about:
            try:
                data = About.objects.first()
                if data:
                    about = {
                        'company_name': data.company_name,
                        'official_email': data.official_email,
                        'num_employees': data.num_employees,
                        'linkedin_url': data.linkedin_url,
                        'about_content': data.about_content,
                        'location':data.location,
                        'updated_at':datetime.now(),
                        'user':f'wolcome {request.user.first_name} {request.user.last_name}'

                    }
                    cache.set(cache_key, about, timeout=20 ) 
                else:
                    logger.error("unvalid")
                    Response( {"msg": "u have to update about data"},status=status.HTTP_400_BAD_REQUEST) 
            except About.DoesNotExist:
                    logger.error("ex")
                    Response( {"msg": "u have to update about data"},status=status.HTTP_400_BAD_REQUEST) 
        return Response(about,status=status.HTTP_200_OK)

