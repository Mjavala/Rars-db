import sys

import requests

"""
Simple script for intergration testing with Rars Simulation
"""
# TODO: Define & add other query fields - ie CaseType
# TODO: Remove flask classfull and go with bare flask or tornado
# TODO: Return if request succesfull / slide exists
# TODO: Multiple slides


def slide_request(slideid):
    try:
        url = "https://evil-dragonfly-55.loca.lt/retrieve_slide/{}".format(
            slideid
        )
        # myobj = {"slideid": slideid}
        res = requests.get(url)
        return res.text

    except requests.exceptions.Timeout:

        print("!--- Update Film: Request timeout ---!")
        sys.exit()
    except requests.exceptions.TooManyRedirects:

        print("!--- Update Film: Too Many Redirects ---!")
    except requests.exceptions.RequestException as e:

        print("!--- Update Film: Requests Error: {}".format(e))
        raise SystemExit(e)


if __name__ == "__main__":
    res = slide_request("hello_world")
    print(res)
