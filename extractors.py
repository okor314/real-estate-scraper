import json 

class Extractor:
    def __init__(self):
        self.pathToData: list = []

    def extract(self, response_json):
        dataContainer = response_json
        for key in self.pathToData:
            dataContainer = dataContainer.get(key)
        
        return dataContainer
    
class CatalogExtractor(Extractor):
    def __init__(self):
        self.pathToData = ['cat1', 'searchResults', 'listResults']

    def extract(self, response_json):
        dataContainer = response_json
        for key in self.pathToData:
            dataContainer = dataContainer.get(key)

        result = []

        for item in dataContainer:
            result.append(
                {
                    'status': item.get('statusType'),
                    'zpid': item.get('zpid'),
                    'price': item.get('unformattedPrice'),
                    'beds': item.get('beds'),
                    'baths': item.get('baths'),
                    'area': item.get('area'),
                    'street': item.get('addressStreet'),
                    'city': item.get('addressCity'),
                    'state': item.get('addressState'),
                    'zipcode': item.get('addressZipcode'),
                    'latitude': item.get('latLong').get('latitude'),
                    'longitude': item.get('latLong').get('longitude'),
                    'url': item.get('detailUrl')
                }
            )
        return result
    
class CatalogDomExtractor(CatalogExtractor):
    def __init__(self):
        super().__init__()
        self.pathToData = ['props', 'pageProps', 'searchPageState', 'cat1', 'searchResults', 'listResults']

class CacheExtractor(Extractor):
    def __init__(self):
        super().__init__()
        self.pathToData = ['props', 'pageProps', 'componentProps', 'gdpClientCache']

    def extract(self, response_json):
        return json.loads(super().extract(response_json))

class DetailDOMExtractor(Extractor):
    def __init__(self):
        super().__init__()

    def extract(self, response_json):
        dataContainer = extractData(response_json, CacheExtractor)
        
        for k, v in dataContainer.items():
            property_data = v.get('property')
            break
        if property_data:
            return {
                'zpid': property_data.get('zpid'),
                'status': property_data.get('homeStatus'),
                'type': property_data.get('homeType'),
                'price': property_data.get('price'),
                'living area': property_data.get('livingArea'),
                'year built': property_data.get('resoFacts').get('yearBuilt'),
                'bedrooms': property_data.get('bedrooms'),
                'bathrooms': property_data.get('bathrooms'),
                'agent name': property_data.get('attributionInfo').get('agentName'),
                'phone number': property_data.get('attributionInfo').get('agentPhoneNumber'),
                'lot size': property_data.get('resoFacts').get('lotSize'),
                'price per sqft': property_data.get('resoFacts').get('pricePerSquareFoot'),
                'parking capacity': property_data.get('resoFacts').get('parkingCapacity')
            }


def extractData(json_obj, extractor: Extractor):
    return extractor().extract(json_obj)

if __name__ == "__main__":
    d = {'cat1': {'searchResults': {'listResults': 'pupupu'}}}
    print(CatalogExtractor().extract(d))
    