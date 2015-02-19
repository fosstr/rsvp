#!/usr/bin/env python

import requests
import settings

def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
        else:
                ip = request.META.get('REMOTE_ADDR')
        return ip


def validateCaptcha(CAPTCHA_RESPONSE,REMOTE_IP=None):
	payload = {'secret': settings.RECAPTCHA_PRV_KEY , 'response': CAPTCHA_RESPONSE , 'remoteip': REMOTE_IP }
	if REMOTE_IP == None:
		payload = {'secret': settings.RECAPTCHA_PRV_KEY , 'response': CAPTCHA_RESPONSE  }
	resp_obj = requests.get(settings.RECAPTCHA_VERIFY_URL, params=payload )
	if resp_obj.status_code != 200:
		return False
	response = resp_obj.json()
	return response['success']