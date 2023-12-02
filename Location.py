from flask import Flask, render_template
import requests
import xml.etree.ElementTree as ET

Location = Flask(__name__)

# Replace 'YOUR_API_KEY' with your Bing Maps API key
api_key = 'AoRdp4vR9rrO8oKqaW-9kEPECNGBg9Kde3QtGPKCVdd2CTv9E1A3aGtbRH2Tjg4k'

@Location.route('/')
def get_names_list():
    # Define the parameters for the request
    #  12.840711  77.676369 - Electronic City
    # 19.076090, 72.877426 - Mumbai 
    SearchLatitude = 19.076090
    SearchLongitude = 72.877426
    Radius = 10

    service_list=[5540,6000,7897,283,5800]
    names=["GasStation","Banks","RestArea","TollPlaza","Restaurant"]
    names_list = []
    j=0
    for i in service_list:
        requestUrl = f"http://spatial.virtualearth.net/REST/v1/data/Microsoft/PointsOfInterest?" \
                 f"spatialFilter=nearby({SearchLatitude},{SearchLongitude},{Radius})&$filter=EntityTypeID%20eq%20'{i}'&$select=EntityID,DisplayName,Latitude,Longitude,__Distance&$top=2&key={api_key}"
        response = requests.get(requestUrl)
        if response.status_code == 200:
            xml_data = response.content
            root = ET.fromstring(xml_data)
            name_elements = root.findall(".//m:properties/d:DisplayName", namespaces={'m': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata', 'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices'})
            dis_elements = root.findall(".//m:properties/d:__Distance", namespaces={'m': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata', 'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices'})
            zi=zip(name_elements,dis_elements)
            for name_element,dis_element in zi:
                name = name_element.text
                dis=dis_element.text
                dis_formatted = f"{float(dis):.2f}"
                names_list.append(names[j]+" : "+name+" - "+dis_formatted+"Km")
        j=j+1
    else:
        print(f'Error: {response.status_code} - {response.text}')
    ############################################################################################################################
    
    return render_template('./business.html', names_list=names_list)

if __name__ == '__main__':
    Location.run(port=8081)
