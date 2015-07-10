from requests import get, ConnectionError, put 
from json import load, dump, dumps
from platform import system

def set_backup_data(current_json):
    print '\nBacking up data\n'
    if system() == "Darwin":
        backup_location = 'Backup/backup.json'
    else:
        backup_location = '/home/pi/FutureCities/MurmurWall/Onsite/Raspi/Backup/backup.json'
    with open(backup_location, 'w') as backup_json:
        dump(current_json, backup_json)


def get_backup_data():
    print '\nConnection Error, Using Backup JSON File\n'
    if system() == "Darwin":
        backup_file = 'Backup/backup.json'
    else:
        backup_file = '/home/pi/FutureCities/MurmurWall/Onsite/Raspi/Backup/backup.json'  
    with open(backup_file) as backup_json_file:    
        current_json = load(backup_json_file)
    return current_json

def get_latest_data():
    try:
        print '\nRequesting new data.....\n'
        response = get("https://api.myjson.com/bins/2csub")
        if response.status_code is 200:
            print '\nSuccess (200) in downloading data\n'
            current_json = response.json()
            set_backup_data(current_json)
        else: 
            current_json = get_backup_data()
    except ConnectionError:
        current_json = get_backup_data()
    return current_json

def get_whispers():
    try:
        new_whispers = []
        response = get("https://api.myjson.com/bins/46ec7")
        if response.status_code is 200:
            data = get("https://api.myjson.com/bins/46ec7").json()
            for word in data:
                if word is not "" and word is not '':
                    new_whispers.append(word.encode('ascii', 'ignore'))
            headers = {'Content-type': 'application/json'}
            put("https://api.myjson.com/bins/46ec7", data=dumps([""]), headers=headers)
        return new_whispers
    except ConnectionError:
        return []

def get_curated_words():
    try:
        response = get("https://api.myjson.com/bins/3ddib")
        if response.status_code is 200:
            words = [word.encode('ascii', 'ignore') for word in response.json()]
            return words
        else: 
            return []
    except ConnectionError:
        return []

def main():
    print get_latest_data()

if __name__ == "__main__":
    main()
