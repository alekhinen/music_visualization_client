import settings
import requests


# @name post_colors()
# @description posts a color object to the IoT url.
# @param color_object Object a color object.
# @returns None
def post_colors(color_object):
  r = requests.post(settings.URL, data=color_object)
  
  if r.status_code != requests.codes.ok:
    print "There was a problem sending the payload!"
    r.raise_for_status()

