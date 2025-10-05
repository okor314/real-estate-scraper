import random

def isKeyExist(json_obj, key) -> bool:
    if type(json_obj) is dict:
        keys = json_obj.keys()
        if key in keys:
            return True
        else:
            return any([isKeyExist(json_obj[k], key) for k in keys])
    elif type(json_obj) is list:
        return any([isKeyExist(item, key) for item in json_obj])
    else:
        return False
    
def fetchResponse(response):
    if response.status == 200 and "zillow.com" in response.url:
        try:
            return isKeyExist(response.json(), 'listResults')
        except:
            return False
    return False

def rateLimiter(n: int):
    pauseDuration = 60/n 
    sigma = pauseDuration / 3
    pauseDuration = pauseDuration + random.uniform(-sigma, sigma)
    return int(pauseDuration * 1000)