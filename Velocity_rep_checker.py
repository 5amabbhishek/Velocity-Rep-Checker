import requests
from xml.etree import ElementTree
import pgeocode
from gooey import Gooey, GooeyParser
import json

def get_lat_lng(zip_code):
    
    try:
        nomi = pgeocode.Nominatim('us')
        resp = nomi.query_postal_code(zip_code)
        lat = str(resp.latitude)
        lng = str(resp.longitude)
        
        
        session = requests.session()
        api_key = "AIzaSyBai-oUJPePJD6jIaiI8xO36F3AytcPwGY"
        url = f"https://maps.googleapis.com/maps/api/geocode/json?key={api_key}&components=postal_code:{zip_code}"
        response = session.get(url)
        
        if json.loads(response.content)['status'] != 'ZERO_RESULTS':
                lat = json.loads(response.content)['results'][0]['geometry']['location']['lat']
                lng = json.loads(response.content)['results'][0]['geometry']['location']['lng']

        else:
                return None
        
        return lat, lng    
     
    except Exception as e:
        return None
     
     
def velocity_check(zip_codes, miles):
    """Check reps availability for multiple ZIP codes"""
    results = []
    for zip_code in zip_codes:
        lat_lng = get_lat_lng(zip_code.strip())
        if lat_lng is not None:
            lat, lng = lat_lng
            session = requests.session()
            response = session.get(f'https://bpophotoflow.com/coverage_markers.php?lat={lat}&lng={lng}&radius={miles}')
            reps_available = 0
            
            for child in ElementTree.fromstring(response.content).iter('marker'):
                if child.attrib['color'] == 'blue.png':
                    reps_available += 1
            
            result_message = f"ZIP Code: {zip_code}  Reps Available: {reps_available}"
            results.append(result_message)
            print(result_message)  # Display the result immediately after checking

        else:
            results.append(f"ZIP Code: {zip_code}, Reps Available: 0")
            print(f"ZIP Code: {zip_code}  Reps Available: 0")  # Display the result immediately

    return results   
        


@Gooey(program_name='BPO PhotoFlow Rep Calculation')
def main():
    parser = GooeyParser(description='Calculate Rep Availability')   
    parser.add_argument('miles', metavar='Radius (Miles)', help='Enter radius in miles')
    parser.add_argument('phtghr_count', metavar='Min. Reps', help='Enter minimum number of reps')
    parser.add_argument('zip_codes', metavar='ZIP Codes', help='Enter ZIP code(s) separated by commas')

    args = parser.parse_args()

    zip_codes = args.zip_codes.split(',')
    miles = args.miles

    velocity_check(zip_codes, miles)

if __name__ == '__main__':
    main()
