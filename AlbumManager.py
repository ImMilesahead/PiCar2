from Album import *

class AlbumManager:
    def __init__(self, songs):
        self.songs = songs
        self.albums = []
        self.albums.append(Album('All Songs'))
        for song in self.songs:
            flag = False
            self.albums[0].addSong(song)
            for album in self.albums[1:]:
                flag = album.addSong(song) or flag 
            if not flag:
                self.albums.append(Album(song.album))
                self.albums[-1].addSong(song)
        for album in self.albums:
            print(album.name)
    def getAlbum(self, album):
        return self.albums[album]