import subprocess
import re

def check_images_for_doubles( img_dir_path ):
    images = sorted(
        img_dir_path.iterdir(),
        key=lambda entry: entry.stat().st_ctime 
    ) 
    hash_dict = {}
    
    for img in images:
        res_str = subprocess.run(['md5', img.resolve()], capture_output=True).stdout.decode('utf8').strip()
        res = re.match(r'MD5 \(.+?\) = (.+)', res_str)
        
        if res:
            hash_value = res.groups()[0]
            
            if hash_value not in hash_dict:
                hash_dict[hash_value] = []
                
            hash_dict[hash_value].append(img)
    
    return hash_dict


def delete_doubles( hash_table ):
    for hash_value in hash_table:
        if len(hash_table[hash_value]) > 1:
            for img in hash_table[hash_value][1:]:
                img.unlink()


def add_id_db( id_str, db_path ):
    with db_path.open('a') as db_file:
        db_file.write(id_str + '\n')


def is_id_in_db( id_str, db_path ):
    if db_path.exists() == False:
        print("db not existing")
        return False
    
    with db_path.open() as db_file:
        downloaded_images = db_file.read().split('\n')
        
    return id_str in downloaded_images