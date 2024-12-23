import os
import sys
import requests
import zipfile
import shutil
import shlex
from bs4 import BeautifulSoup
from natsort import natsorted
from pathlib import Path

#* Colors for terminal
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    END = "\033[0m"

#* Help message
HELP_MESSAGE = f"""
{Colors.MAGENTA}******************{Colors.END}
HELP MESSAGE ===>
This tool automatically combines your manga chapters into volumes using mangadex.org API and if wanted even adds covers.

{Colors.MAGENTA}*** USAGE ***{Colors.END}
1. Put all your chapters in one folder.
2. Find the manga on mangadex.org and get its ID from the URL. (https://mangadex.org/title/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/manga)
3. Run the script from command using:
    python3 app.py -id [ID] -f [FOLDER] -p [INPUT FILE PREFIX] <-cp [CREATED FILE PREFIX]> <-c> -<kc> <-l [LIMIT]>
    OR  
    py app.py -id [ID] -f [FOLDER] -p [INPUT FILE PREFIX] <-cp [CREATED FILE PREFIX]> <-c> -<kc> <-l [LIMIT]>

{Colors.MAGENTA}*** ARGUMENTS ***{Colors.END}
{Colors.RED}REQUIRED:{Colors.END}
{Colors.YELLOW}-f{Colors.END}: Target folder to process. !Can't have spaces or qoutes. I know its realy stupid. Plan to fix!
{Colors.YELLOW}-p{Colors.END}: Prefix in input chapter files naming (to strip and read its number).
{Colors.YELLOW}-id{Colors.END}: UUID of manga dex manga (you can find it in url: https://mangadex.org/title/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/manga title).
{Colors.CYAN}OPTIONAL:{Colors.END}
{Colors.YELLOW}-h, -help{Colors.END}: Print this message.
{Colors.YELLOW}-cp{Colors.END}: Prefix for created files.
{Colors.YELLOW}-l{Colors.END}: Request limit for API.
{Colors.YELLOW}-cr{Colors.END}: Cover version Explenation: (You can view covers on mangadex.org in 'art' tab of manga. They are sorted by 'volume'. If any 'volume' is there multiple times these are various 'versions'. These 'versions' are sorted from left to right.)
{Colors.YELLOW}-ca{Colors.END}: Cover variation Explenation: (You can view covers on mangadex.org in 'art' tab of manga. They are sorted by 'volume'. Some of them have decimal point '.' and number after it. These are variations.)
{Colors.YELLOW}-cl{Colors.END}: Cover locale (local cover) (on mangadex.org you can filter by locale) For language codes refere to https://api.mangadex.org/docs/3-enumerations/ ===> https://en.wikipedia.org/wiki/IETF_language_tag and https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes

{Colors.MAGENTA}*** SWITCHES ***{Colors.END}
{Colors.YELLOW}-c{Colors.END}: Download and add covers.
{Colors.YELLOW}-kc{Colors.END}: Keep downloaded covers.
{Colors.YELLOW}-pc{Colors.END}: Log (print) API's cover response.

{Colors.MAGENTA}******************{Colors.END}
"""

#* INIT
MANGA_ID = None
FOLDER = None
REQUEST_LIMIT = 100
FILE_ID_PREFIX = ""
CREATED_FILE_PREFIX = "vol "
API_URL = "https://api.mangadex.org/"
DOWNLOAD_COVERS = False
KEEP_COVERS = False
LOG_COVERS = False
COVER_VERSION = 1
COVER_VARIATION = 0
COVER_LOCALE = 'ja'


for i, argv in enumerate(sys.argv[1:]):
    if i + 2 < len(sys.argv):
        nextARGV = sys.argv[i + 2]
    else:
        nextARGV = None

    if argv == "-h" or argv == "-help":
        print(HELP_MESSAGE)
        sys.exit(0)
    if argv == "-id":
        MANGA_ID = nextARGV
    if argv == "-f":
        try:    
            FOLDER = shlex.split(nextARGV)[0] if nextARGV else None
        except ValueError as e:
            print(f"{Colors.RED}Error parsing folder path: {str(e)}{Colors.END}")
            sys.exit(1)
    if argv == "-l":
        REQUEST_LIMIT = nextARGV
    if argv == "-p":
        FILE_ID_PREFIX = nextARGV
    if argv == "-cp":
        CREATED_FILE_PREFIX = nextARGV
    if argv == "-c":
        DOWNLOAD_COVERS = True
    if argv == "-kc":
        KEEP_COVERS = True
    if argv == "-cr":
        COVER_VERSION = nextARGV
    if argv == "-ca":
        COVER_VARIATION = nextARGV
    if argv == "-cl":
        COVER_LOCALE = nextARGV
    if argv == "-pc":
        LOG_COVERS = True
    

#* Checks before run
error = False
if not MANGA_ID:
    print(f"{Colors.RED}Manga UUID is required.{Colors.END} Please use:{Colors.YELLOW} -id [UUID]{Colors.END} \n (you can find in the url: https://mangadex.org/title/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/)")
    error = True
if not FOLDER:
    print(f"{Colors.RED}Target folder is required.{Colors.END} Please use:{Colors.YELLOW} -f [FOLDER]{Colors.END}")
    error = True
if not FILE_ID_PREFIX:
    print(f"{Colors.RED}File prefix is required.{Colors.END} Please use:{Colors.YELLOW} -p [PREFIX]{Colors.END}")
    error = True

if error:
    print(f"For more info use {Colors.YELLOW}-h{Colors.END}.")
    sys.exit(1)

# [1: [1, 13], 2: [14, 26], ....]
volumes = {}

#* Get volumes of the manga
MANGA_URL = f"{API_URL}/manga/{MANGA_ID}"
COVER_URL = f"{API_URL}/cover?manga[]={MANGA_ID}"  # Fixed: Added [] for array parameter
CHAPTER_URL = f"{API_URL}/chapter?manga={MANGA_ID}&translatedLanguage[]=en&order[volume]=asc&order[chapter]=asc"

#* Fetch info and print it
manga = requests.get(MANGA_URL).json()
covers_response = requests.get(COVER_URL).json()
chapters = requests.get(CHAPTER_URL).json()

manga_title = manga['data']['attributes']['title']['en']
manga_dir = Path(manga_title)
if not manga_dir.exists():
    os.makedirs(manga_dir)

print(f"{Colors.GREEN} Manga fetched successfully: {Colors.END}")
print(f"{Colors.MAGENTA} Title: {Colors.END}{manga_title}")
amount_of_chapters_info = manga['data']['attributes']['lastChapter']
amount_of_volumes_info = manga['data']['attributes']['lastVolume']
if not(amount_of_chapters_info or amount_of_volumes_info) and not(amount_of_chapters_info == '' or amount_of_volumes_info == ''):
    amount_of_chapters_info = 'N/A'
    amount_of_volumes_info = 'N/A'
print(f"{Colors.CYAN} Chapters: {Colors.END}{amount_of_chapters_info} || {Colors.CYAN}Volumes: {Colors.END}{amount_of_volumes_info}")
    

def fetch_all_covers(url):
    all_covers = []
    offset = 0
    limit = REQUEST_LIMIT

    try:
        while True:
            response = requests.get(f"{url}&limit={limit}&offset={offset}").json()
            
            if 'result' in response and response['result'] == 'ok':
                data = response.get('data', [])
                all_covers.extend(data)
                
                # Check if we've received all covers
                total = response.get('total', 0)
                if offset >= total or not data:
                    break
                offset += limit
            else:
                print(f"{Colors.RED}Error in API response: {response}{Colors.END}")
                break

    except Exception as e:
        print(f"{Colors.RED}Error fetching covers: {str(e)}{Colors.END}")
    
    if LOG_COVERS:
        print(all_covers)
        
    return all_covers

if DOWNLOAD_COVERS:
    print(f'{Colors.YELLOW}Downloading covers...{Colors.END}: Version: {COVER_VERSION} || Variation {COVER_VARIATION}')

    all_covers = fetch_all_covers(COVER_URL)
    volume_covers = []
    
    for cover in all_covers:
        # Filter by version
        cover_ver = cover['attributes']['version']
        
        if not float(cover_ver) == float(COVER_VERSION):
            continue

        # Filter by variation
        cover_var = -1
        try:
            cover_var = cover['attributes']['volume'].split('.')[1]
        except Exception as e:
            if cover['attributes']['volume'].split('.')[0]:
                cover_var = 0
        if not float(cover_var) == float(COVER_VARIATION):
            continue
            
        # Filter by locale
        if not cover['attributes']['locale'] == COVER_LOCALE:
            continue
        
        try:
            volume = cover['attributes']['volume']
            if volume:  # Check if volume is not None and is a number
                volume = float(volume)
                if volume != float(int(volume)):
                    volume = str(volume)
                    volume = int(volume.split('.')[0])
                cover_url = f"https://uploads.mangadex.org/covers/{MANGA_ID}/{cover['attributes']['fileName']}"
                volume_covers.append({'volume': volume, 'coverURL': cover_url})
                # Download the image and save it
                response = requests.get(cover_url)
                try:
                    covers_dir = manga_dir / "covers"
                    if not covers_dir.exists():
                        os.makedirs(covers_dir)
                    with open(covers_dir / f"{volume}.jpg", 'wb') as f:
                        print(f"{Colors.YELLOW}Downloading cover{Colors.END} {volume} ({cover['attributes']['fileName']})...")
                        f.write(response.content)
                except Exception as e:
                    (f"{Colors.RED}Error downloading cover: {str(e)}{Colors.END}")
        except (KeyError, ValueError) as e:
            print(f"{Colors.YELLOW}Warning: Could not process cover: {str(e)}{Colors.END}")
            continue


def fetch_all_chapters(url):
    all_chapters = []
    offset = 0
    limit = REQUEST_LIMIT

    while True:
        response = requests.get(f"{url}&limit={limit}&offset={offset}").json()
        all_chapters.extend(response['data'])
        offset += limit
        if offset >= response['total']:
            break

    return all_chapters

# Fetch all chapters
all_chapters = fetch_all_chapters(CHAPTER_URL)

for i, chapter in enumerate(all_chapters):
    try:
        volume = int(chapter['attributes']['volume'])
        chapter_id = chapter['attributes']['chapter']
        if volume not in volumes:
                # Initialize the volume with the first chapter
                volumes[volume] = [chapter_id]
        else:
            if chapter_id in volumes[volume]:
                # Skip if the chapter is already in the volume
                continue
            # Append the chapter to the existing volume
            volumes[volume].append(chapter_id)
    except Exception as e:
        print(f'{Colors.RED}Chapter{Colors.END} {chapter_id} {Colors.RED}doesnt have volume asigned. Leaving it out{Colors.END}')
        continue

#* Fetch target folder
files = []
try:
    # Just get the files from the directory directly
    files = natsorted([f for f in os.listdir(FOLDER) if f.endswith('.cbz')])
    print(f"{Colors.CYAN}Files found: {Colors.END}{len(files)}")
except Exception as e:
    print(f"{Colors.RED}Error: {e}{Colors.END}")

def strip_file_number(file):
    try:
        return float(file.replace(FILE_ID_PREFIX, "").replace(".cbz", ""))
    except ValueError:
        print(f"{Colors.RED}Could not convert chapter number to floating point number (file: {file}). Check your -p (chapter prefix){Colors.END}")
        sys.exit(1)

last_volume = list(volumes.keys())[-1]
for volume in volumes:
    # Create volume directory if it doesn't exist
    volume_dir = manga_dir / (CREATED_FILE_PREFIX + str(volume))
    if not volume_dir.exists():
        os.makedirs(volume_dir)
    
    # Create new volume zip file
    with zipfile.ZipFile(manga_dir / (CREATED_FILE_PREFIX + str(volume) + ".cbz"), "w") as volume_zip:
        highest_img_num = 1
        
        # Sort files to ensure correct chapter order
        sorted_files = sorted(files, key=lambda x: strip_file_number(x))
        
        for file in sorted_files:
            file_id = strip_file_number(file)
            # Check if file belongs to current volume
            if file_id >= float(volumes[volume][0]) and file_id <= float(volumes[volume][-1]):
                print(f"{Colors.YELLOW}Processing {Colors.END}Volume {volume} || Chapter {file_id}")
                
                # Create temporary directory for this chapter
                temp_dir = volume_dir / f"temp_{file_id}"
                if not temp_dir.exists():
                    os.makedirs(temp_dir)
                
                try:
                    # Extract chapter
                    with zipfile.ZipFile(os.path.join(FOLDER, file), 'r') as chapter_zip:
                        chapter_zip.extractall(temp_dir)
                    
                    # Process images in natural sort order
                    chapter_images = natsorted([f for f in os.listdir(temp_dir) if f.endswith(('.jpg', '.png'))])
                    
                    if DOWNLOAD_COVERS and highest_img_num == 1:
                        # Add cover image to volume
                        cover_path = manga_dir / "covers" / f"{float(volume)}.jpg"
                        if cover_path.exists():
                            volume_zip.write(cover_path, f"000.jpg")
                            highest_img_num += 1
                        if (not KEEP_COVERS) and (volume == last_volume):
                            shutil.rmtree(manga_dir / "covers")
                    for img in chapter_images:
                        if img.endswith(('.jpg', '.png')):
                            # Get original and new paths
                            old_path = temp_dir / img
                            new_name = f"{highest_img_num:03d}{os.path.splitext(img)[1]}"
                            new_path = temp_dir / new_name
                            
                            # Rename and add to volume
                            os.rename(old_path, new_path)
                            volume_zip.write(new_path, new_name)
                            highest_img_num += 1
                    
                    # Clean up temp directory after processing
                    shutil.rmtree(temp_dir)
                    
                except Exception as e:
                    print(f"{Colors.RED}Error processing {file}: {str(e)}{Colors.END}")
                    continue
        
        print(f"{Colors.GREEN}Completed Volume{Colors.END} {volume}{Colors.END}")

    # Clean up volume directory
    if volume_dir.exists():
        shutil.rmtree(volume_dir)