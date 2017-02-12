# coding:utf-8
import os
import sys
import datetime
import EXIF as exif

def insert_time_to_file_name(dirPath, newFileName):
    if dirPath is None or newFileName is None: error_with_exit("directory path or file name is none")
    if os.path.exists(dirPath) == False: error_with_exit("No directory " + dirPath)
    firstTimeStamp = None
    for root, dirs, files in os.walk(dirPath):
        for fileName in files:
            oldFilePath = os.path.join(root, fileName)
            nameWithoutExt , ext = os.path.splitext(fileName)
            # get lowercase extension
            lowercaseExt = ext.lower()
            timestamp = None
            if nameWithoutExt[0] == ".": continue
            if lowercaseExt == ".tiff" or lowercaseExt == ".jpg":
                timestamp = get_timestamp_from_exif(oldFilePath)
            if timestamp is None:
                timestamp = get_timestamp(oldFilePath)
            newFilePath = os.path.join(root, newFileName + "_" + timestamp + ext )
            newFilePath = add_counter_to_name(newFilePath)
            os.rename(oldFilePath, newFilePath)
            # タイムスタンプの一番最初のものをフォルダ名に用いる
            if firstTimeStamp is None: firstTimeStamp = timestamp

    # 写真を入れているフォルダの名前も変更する
    pathToDir = os.path.dirname(dirPath)
    newPath = os.path.join(pathToDir, firstTimeStamp[:8] + "_" + newFileName)
    os.rename(dirPath, newPath)

def add_counter_to_name(filePath):
    """ Add counter to the file name so that the file wont be deleted """
    nameWithoutExt, ext = os.path.splitext(filePath)
    counter = 1
    while os.path.exists(filePath):
        filePath = nameWithoutExt + "_" + str(counter) + ext
        counter += 1
    return filePath

def get_timestamp_from_exif(imagePath):
    # from file path to time stamp
    imageFile = open(imagePath, "rb")
    tags = exif.process_file(imageFile, stop_tag="DateTimeOriginal")
    if "EXIF DateTimeOriginal" not in tags:
        return None
    else:
        # you need to convert timestamp to string object
        timestamp = str(tags["EXIF DateTimeOriginal"])
        dateAndTime = datetime.datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S")
        return dateAndTime.strftime("%Y%m%d_%H%M%S")

def get_timestamp(filePath):
    # from file path to time stamp
    dateAndTime = datetime.datetime.fromtimestamp(os.path.getmtime(filePath))
    return dateAndTime.strftime("%Y%m%d_%H%M%S")

def error_with_exit(error_message):
    print(error_message)
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        error_with_exit("usage: python insert_time_to_file_name.py directoryPath fileName")
    dirPath = sys.argv[1]
    fileName = sys.argv[2]
    insert_time_to_file_name(dirPath, fileName)

