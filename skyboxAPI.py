import requests
import creds
import pprint
import time 
skyb_gen_url = 'https://backend.blockadelabs.com/api/v1/skybox'
skyb_req_url = 'https://backend.blockadelabs.com/api/v1/skybox/submit/2'
#0 fantasy
#1 anime
#2 surreal
#14 lowpoly
def create_gen():
    gen_params={
        'api_key':creds.skybox_key
    }

    gen = requests.get(skyb_gen_url,params=gen_params)
    pprint.pprint(gen.json())

def req_sb(prompt):
    req_params={
        'api_key':creds.skybox_key,
        'prompt[USER_INPUT_1]': prompt
    }
    sbreq = requests.post(skyb_req_url,params=req_params)
    return sbreq.json().get('imaginations')[0].get('id')

def getSB(ID):
    get_url = f'https://backend.blockadelabs.com/api/v1/imagine/requests/{ID}'
    params ={'api_key':creds.skybox_key}
    r = requests.get(get_url,params=params)
    hdri_name = f"D:/thesisMeshesandAnims/hdris/{ID}.hdr"
    hdri = requests.get(r.json().get('request').get('file_url'))
    with open (hdri_name,'wb') as f:
        f.write(hdri.content)
    return hdri_name

def main(prompt):
    id = req_sb(prompt)
    print(id)
    time.sleep(60)
    filepath = getSB(id)
    return filepath
