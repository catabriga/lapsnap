import os
import os.path
import datetime
import shutil
import sys

DAYS_TO_KEEP = 2

def delete_old_folders(folder_path):
    for f in os.listdir(folder_path):
        if(os.path.isdir(folder_path+f)):
            today = datetime.date.today()
            folder_day = datetime.datetime.strptime(f, '%Y-%m-%d').date()
            diff = (today-folder_day).days
            if(diff > DAYS_TO_KEEP):
                print('removing '+folder_path+f)
                shutil.rmtree(folder_path+f)


delete_old_folders(sys.argv[1])