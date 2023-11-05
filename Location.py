from flask import Flask, render_template
import requests
import xml.etree.ElementTree as ET

Location = Flask(__name__)

# Replace 'YOUR_API_KEY' with your Bing Maps API key
api_key = 'AoRdp4vR9rrO8oKqaW-9kEPECNGBg9Kde3QtGPKCVdd2CTv9E1A3aGtbRH2Tjg4k'

@Location.route('/')
def get_names_list():
    # Define the parameters for the request
    SearchLatitude = 19.076090
    SearchLongitude = 72.877426
    Radius = 10

    service_list=[5540,6000,7897,283,5800]
    names=["GasStation","Banks","RestArea","TollPlaza","Restaurant"]
    names_list = []
    j=0
    for i in service_list:
        requestUrl = f"http://spatial.virtualearth.net/REST/v1/data/Microsoft/PointsOfInterest?" \
                 f"spatialFilter=nearby({SearchLatitude},{SearchLongitude},{Radius})&$filter=EntityTypeID%20eq%20'{i}'&$select=EntityID,DisplayName,Latitude,Longitude,__Distance&$top=3&key={api_key}"
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
                names_list.append(names[j]+" : "+name+" - "+dis+"Km")
        j=j+1


        


    # requestUrl = f"http://spatial.virtualearth.net/REST/v1/data/Microsoft/PointsOfInterest?" \
    #              f"spatialFilter=nearby({SearchLatitude},{SearchLongitude},{Radius})&$filter=EntityTypeID%20eq%20'5540'&$select=EntityID,DisplayName,Latitude,Longitude,__Distance&$top=3&key={api_key}"
    # requestUrl2 = f"http://spatial.virtualearth.net/REST/v1/data/Microsoft/PointsOfInterest?" \
    #              f"spatialFilter=nearby({SearchLatitude},{SearchLongitude},{Radius})&$filter=EntityTypeID%20eq%20'6000'&$select=EntityID,DisplayName,Latitude,Longitude,__Distance&$top=3&key={api_key}"
    # requestUrl3 = f"http://spatial.virtualearth.net/REST/v1/data/Microsoft/PointsOfInterest?" \
    #              f"spatialFilter=nearby({SearchLatitude},{SearchLongitude},{Radius})&$filter=EntityTypeID%20eq%20'6000'&$select=EntityID,DisplayName,Latitude,Longitude,__Distance&$top=3&key={api_key}"
    # response = requests.get(requestUrl)
    # response2 = requests.get(requestUrl2)
    # response3 = requests.get(requestUrl3)
    # names_list = []

    # if response.status_code and response2.status_code == 200:
    #     # Parse the XML content
    #     xml_data = response.content
    #     xml_data2= response2.content
    #     xml_data3= response3.content
    #     # Parse the XML using ElementTree
    #     root = ET.fromstring(xml_data)
    #     root2 = ET.fromstring(xml_data2) 
    #     root3 = ET.fromstring(xml_data3) 
    #     # Iterate through the XML elements and add their values to names_list
    #     name_elements = root.findall(".//m:properties/d:DisplayName", namespaces={'m': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata', 'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices'})
        
    #     name_elements2 =root2.findall(".//m:properties/d:DisplayName", namespaces={'m': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata', 'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices'})
    #     name_elements3 =root3.findall(".//m:properties/d:DisplayName", namespaces={'m': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata', 'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices'})
    #     for name_element in name_elements2:
    #         name = name_element.text
    #         names_list.append("Banks:"+name)
    #     for name_element in name_elements:
    #         name = name_element.text
    #         names_list.append("GasStations:"+name)
    #     for name_element in name_elements3:
    #         name = name_element.text
    #         names_list.append("ATM:"+name)
    else:
        print(f'Error: {response.status_code} - {response.text}')
    ############################################################################################################################
    
    return render_template('./business.html', names_list=names_list)

if __name__ == '__main__':
    Location.run(port=8081)
