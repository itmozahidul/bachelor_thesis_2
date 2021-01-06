import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from guessGame.polls.Mscripts.project_classes import fileInfo


def get_list_of_file_in_directory():
    fs = FileSystemStorage()
    filelist = []
    fileList = os.listdir(settings.MEDIA_ROOT)
    for f in fileList:
        url = fs.url(f)
        filelist .append(fileInfo(url, f))


    return filelist