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

def extractData(json_obj, extractor: Extractor):
    return extractor().extract(json_obj)

if __name__ == "__main__":
    d = {'cat1': {'searchResults': {'listResults': 'pupupu'}}}
    print(CatalogExtractor().extract(d))
    