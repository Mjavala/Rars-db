import requests
import json

# TODO: Define & add other query fields - ie CaseType
# TODO: Remove flask classfull and go with bare flask or tornado

def slide_request(slideid):
    try:
        url = "http://127.0.0.1:9999/retrieve_slide/{}".format(slideid)
        #myobj = {"slideid": slideid}
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

if __name__ == '__main__':
    res = slide_request('hello_world')
    print(res)
    