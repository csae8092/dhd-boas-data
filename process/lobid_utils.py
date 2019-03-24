import re
import requests


def coords_from_wkt(wkt):
    """
    parses a (POINT) WKT and returns a tuple of lat, lng coordinates
    :param: Point-WKT like: "Point ( +011.338888 +044.493888 )"
    :return: A tuple like (11.338888, 44.493888)
    """
    nums = re.findall(r'\d+(?:\.\d*)?', wkt)
    return (float(nums[0]), float(nums[1]))


def gnd_url_to_lobid_json(gnd="http://d-nb.info/gnd/112454-7"):
    """
    Transforms a GND URL or GND ID to a lobid-json url
    :param gnd: A GND URL e.g. http://d-nb.info/gnd/112454-7 or GND ID 112454-7
    :return: A lobid-gnd-json, e.g. http://lobid.org/gnd/112454-7.json
    """
    gnd_nr = gnd.split('/')[-1]
    lobid_json = "http://lobid.org/gnd/{}.json".format(gnd_nr)
    return lobid_json


def get_place_of_business_id(gnd="http://d-nb.info/gnd/112454-7"):
    """
    Gets the (first) placeOfBusiness object
    :param gnd: A GND URL e.g. http://d-nb.info/gnd/4048989-9 or GND ID 2067664-5
    :return: The GND URL of the (first) related placeOfBusiness object
    """
    lobid_url = gnd_url_to_lobid_json(gnd)
    r = requests.get(lobid_url)
    try:
        return r.json()['placeOfBusiness'][0]['id']
        return
    except Exception as e:
        print(e)
        return None


def get_place_of_business_coords(gnd="http://d-nb.info/gnd/112454-7"):
    """
    Gets the coordinates of the (first) placeOfBusiness object for the passed in GND-ID/URL
    :param gnd: A GND URL e.g. http://d-nb.info/gnd/4048989-9 or GND ID 2067664-5
    :return: A tuple like (11.338888, 44.493888)
    """
    lobid_url = get_place_of_business_id(gnd=gnd)
    if lobid_url is not None:
        r = requests.get(gnd_url_to_lobid_json(lobid_url))
        wkt = r.json()['hasGeometry'][0]['asWKT'][0]
        coords = coords_from_wkt(wkt)
        return coords
    else:
        return None
