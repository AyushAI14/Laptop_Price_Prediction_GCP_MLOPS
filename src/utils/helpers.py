import os
import re


def create_file_folder(file_path):
    # file_path = Path(file_path)
    file_dir,filename = os.path.split(file_path)
    os.makedirs(file_dir, exist_ok=True)
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path)==0):
        with open(file_path,'w') as f:
            f.write("")
        print(f"{file_path} Created Successfully !")
    else:
        print(f"file exist at {file_path}")

def cpu_tier(cpu):
    if 'Xeon' in cpu or 'i7' in cpu and ('HQ' in cpu or 'HK' in cpu):
        return 'high'
    elif 'i7' in cpu or 'Ryzen' in cpu or 'FX' in cpu:
        return 'mid_high'
    elif 'i5' in cpu:
        return 'mid'
    else:
        return 'low'
def gpu_tier(gpu):
    if any(x in gpu for x in ['GTX 1080','GTX 1070','GTX 1060','980','970','Quadro','FirePro']):
        return 'high'
    elif any(x in gpu for x in ['GTX 1050','GTX 960','RX 580','RX 560']):
        return 'mid_high'
    elif any(x in gpu for x in ['MX150','MX130','940','930','920','Radeon 530','Radeon 540']):
        return 'mid'
    else:
        return 'low'

def os_identifier(os):
    if os in ["macOS","Mac OS X"]:
        return 'macOS'
    elif os in ['Windows 10','Windows 10 S','Windows 7']:
        return 'Windows'
    else:
        return "Unpopular os"
def extract_series(name):
    keywords = ['MacBook','XPS','ThinkPad','ROG','Legion','Inspiron','Pavilion','EliteBook','ProBook','Aspire','ZenBook','VivoBook','Omen','Alienware']
    for k in keywords:
        if k.lower() in name.lower():
            return k
    return 'Other'


def process_memory(mem):
    ssd = 0
    hdd = 0
    flash = 0
    
    parts = mem.split('+')
    
    for part in parts:
        part = part.strip()
        
        size = int(re.findall(r'\d+', part)[0])
        
        if 'TB' in part:
            size *= 1024
        if 'SSD' in part:
            ssd += size
        elif 'HDD' in part:
            hdd += size
        elif 'Flash' in part:
            flash += size
    
    return ssd, hdd, flash

def other_companies(companies):
    if companies in ['Vero','Xiaomi','Chuwi','Fujitsu','LG','Huawei']:
        return "other_companies"
    else:
        return companies