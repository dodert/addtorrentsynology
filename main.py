from encodings import utf_8
import os, pathlib, re, shutil
from re import ASCII
from tqdm import tqdm
from time import sleep
from configparser import ConfigParser, ExtendedInterpolation
from dataclasses import dataclass

_CONFIGFILE = 'config_dodert.cfg'
_SETTINGS = None
_TorrentsList = []
_NameToLookForAndTorrent = []
_NameToLookFor = []

@dataclass
class Settings:
    torrentFilesFrom: str
    shareFolderMovies1: str
    shareFolderMovies2: str
    shareFolderMovies3: str
    shareFolderMovies4: str
    shareFolderTvShows1: str
    shareFolderTvShows2: str
    shareFolderTvShows3: str
    shareFolderDocumentales4: str

    shareFolderMovies1Dest: str 
    shareFolderMovies2Dest: str 
    shareFolderMovies3Dest: str 
    shareFolderMovies4Dest: str 
    shareFolderTvShows1Dest: str
    shareFolderTvShows2Dest: str
    shareFolderTvShows3Dest: str
    shareFolderDocumentary4Dest: str

def readConfiguration():
    cfg = ConfigParser(interpolation=ExtendedInterpolation())
    cfg.read(_CONFIGFILE)
    global _SETTINGS

    _SETTINGS = Settings(
        cfg['DEFAULT']['TorrentFilesFrom']
        , cfg['Forders Where files where dowloaded']['ShareFolderMovies1']
        , cfg['Forders Where files where dowloaded']['ShareFolderMovies2']
        , cfg['Forders Where files where dowloaded']['ShareFolderMovies3']
        , cfg['Forders Where files where dowloaded']['ShareFolderMovies4']
        , cfg['Forders Where files where dowloaded']['ShareFolderTVShows1']
        , cfg['Forders Where files where dowloaded']['ShareFolderTVShows2']
        , cfg['Forders Where files where dowloaded']['ShareFolderTVShows3']
        , cfg['Forders Where files where dowloaded']['ShareFolderDocumentary4']
        , cfg['Forders to place torrent base on files downloaded folders']['ShareFolderMovies1Dest']
        , cfg['Forders to place torrent base on files downloaded folders']['ShareFolderMovies2Dest']
        , cfg['Forders to place torrent base on files downloaded folders']['ShareFolderMovies3Dest']
        , cfg['Forders to place torrent base on files downloaded folders']['ShareFolderMovies4Dest']
        , cfg['Forders to place torrent base on files downloaded folders']['ShareFolderTvShows1Dest']
        , cfg['Forders to place torrent base on files downloaded folders']['ShareFolderTvShows2Dest']
        , cfg['Forders to place torrent base on files downloaded folders']['ShareFolderTvShows3Dest']
        , cfg['Forders to place torrent base on files downloaded folders']['ShareFolderDocumentary4Dest']
    )
    print (_SETTINGS.shareFolderMovies2Dest)

def prepareFolders():
    if not os.path.exists(_SETTINGS.shareFolderMovies1Dest):
        os.makedirs(_SETTINGS.shareFolderMovies1Dest)

    if not os.path.exists(_SETTINGS.shareFolderMovies2Dest):
        os.makedirs(_SETTINGS.shareFolderMovies2Dest)

    if not os.path.exists(_SETTINGS.shareFolderMovies3Dest):
        os.makedirs(_SETTINGS.shareFolderMovies3Dest)

    if not os.path.exists(_SETTINGS.shareFolderMovies4Dest):
        os.makedirs(_SETTINGS.shareFolderMovies4Dest)

    if not os.path.exists(_SETTINGS.shareFolderTvShows1Dest):
        os.makedirs(_SETTINGS.shareFolderTvShows1Dest)

    if not os.path.exists(_SETTINGS.shareFolderTvShows2Dest):
        os.makedirs(_SETTINGS.shareFolderTvShows2Dest)

    if not os.path.exists(_SETTINGS.shareFolderTvShows3Dest):
        os.makedirs(_SETTINGS.shareFolderTvShows3Dest)

    if not os.path.exists(_SETTINGS.shareFolderDocumentary4Dest):
        os.makedirs(_SETTINGS.shareFolderDocumentary4Dest)

def listFiles():
    path = _SETTINGS.torrentFilesFrom
    dirs = os.scandir(path)
    for file in dirs:
        if file.is_file() and pathlib.Path(file.path).suffix == ".torrent":
            _TorrentsList.append(file)
    dirs.close

def getNames():
    with tqdm(total=len(_TorrentsList), postfix=["Getting file names"]) as pbar:
        for file in _TorrentsList:
            file1 = open(file.path, 'r', encoding="utf_8",errors='ignore' )
            asdf = file1.readline()
            columns = asdf.split(':')
            found_mkv = False
            folderre = re.compile('12$')
            folderFi = re.compile('.mkv12$')
            toignnore = re.compile('^path')
            #print (file.name)
            for column in columns:
                #print(folderFi.match(column))
                if folderFi.search(column) != None: #'.mkv12' in column: #when is 1 file
                    found_mkv = True
                    #print ('file ' + folderFi.sub('.mkv', column))
                    _NameToLookForAndTorrent.append(file.path + '|' + folderFi.sub('.mkv', column))
                    _NameToLookFor.append(folderFi.sub('.mkv', column))
                    #print (column)
                    exit
                elif folderre.search(column) != None and toignnore.search(column) == None: #folders
                    found_mkv = True
                    #print ('Folder ' + file.name + '--' + folderre.sub('', column))
                    #print (folderre.sub('', column))
                    _NameToLookForAndTorrent.append(file.path + '|' +  folderre.sub('', column))
                    _NameToLookFor.append(folderre.sub('', column))
                    exit
                #else:
                #    print ('not clasified ' + file.name + '--' + folderre.sub('', column))
            if found_mkv == False:
                print ('MISSING ' + file.name)
            #sleep(0.)
            #pbar.set_description('Getting names %i' % file.name )
            pbar.update(1)
        #pbar.update(1)

def assignFolder_ForPelis():
    #with tqdm(total=len(os.), postfix=["Scanning " + _SETTINGS.shareFolderMovies1]) as pbar:
    #t = tqdm(total=1, unit="file")
    for file in os.scandir(_SETTINGS.shareFolderMovies1):
        for torr in _NameToLookForAndTorrent:
            #t.set_postfix(filename = file.name)
            #t.total += 1
            #t.update()
            #sleep(0.25)
            if file.name == torr.split('|')[1]:
                print('Moving 1: ' + torr.split('|')[0])
                shutil.move(torr.split('|')[0], _SETTINGS.shareFolderMovies1Dest)
        #tqdm.update(1)
   # t.close()            
    for file in os.scandir(_SETTINGS.shareFolderMovies2):
        for torr in _NameToLookForAndTorrent:
            if file.name == torr.split('|')[1]:
                print('Moving 2: ' + torr.split('|')[0])
                shutil.move(torr.split('|')[0], _SETTINGS.shareFolderMovies2Dest)

    for file in os.scandir(_SETTINGS.shareFolderMovies3):
        for torr in _NameToLookForAndTorrent:
            if file.name == torr.split('|')[1]:
                print('Moving 3: ' + torr.split('|')[0])
                shutil.move(torr.split('|')[0], _SETTINGS.shareFolderMovies3Dest)

    for file in os.scandir(_SETTINGS.shareFolderMovies4):
        for torr in _NameToLookForAndTorrent:
            if file.name == torr.split('|')[1]:
                print('Moving 4: ' + torr.split('|')[0])
                shutil.move(torr.split('|')[0], _SETTINGS.shareFolderMovies4Dest)
  
def assignFolder_ForSeries():
    for file in os.scandir(_SETTINGS.shareFolderTvShows1):
        for torr in _NameToLookForAndTorrent:
            if file.name == torr.split('|')[1]:
                print('Moving 1: ' + torr.split('|')[0] + '-->' + _SETTINGS.shareFolderTvShows1Dest)
                shutil.move(torr.split('|')[0], _SETTINGS.shareFolderTvShows1Dest)
                
    for file in os.scandir(_SETTINGS.shareFolderTvShows2):
        for torr in _NameToLookForAndTorrent:
            if file.name == torr.split('|')[1]:
                print('Moving 2: ' + torr.split('|')[0] + '-->' + _SETTINGS.shareFolderTvShows2Dest)
                shutil.move(torr.split('|')[0], _SETTINGS.shareFolderTvShows2Dest)

    for file in os.scandir(_SETTINGS.shareFolderTvShows3):
        for torr in _NameToLookForAndTorrent:
            if file.name == torr.split('|')[1]:
                print('Moving 3: ' + torr.split('|')[0] + '-->' + _SETTINGS.shareFolderTvShows3Dest)
                shutil.move(torr.split('|')[0], _SETTINGS.shareFolderTvShows3Dest)

def assignFolder_ForDocumentales():
    for file in os.scandir(_SETTINGS.shareFolderDocumentales4):
        for torr in _NameToLookForAndTorrent:
            if file.name == torr.split('|')[1]:
                print('Moving 1: ' + torr.split('|')[0] + '-->' + _SETTINGS.shareFolderDocumentary4Dest)
                shutil.move(torr.split('|')[0], _SETTINGS.shareFolderDocumentary4Dest)

def main():
    print('-----STARTING----')
    readConfiguration()
    prepareFolders()
    listFiles()
    getNames()
    #exit()
    assignFolder_ForPelis()
    assignFolder_ForSeries()
    assignFolder_ForDocumentales()
    print('-----COMPLETED----')


if __name__ == "__main__":
    main()