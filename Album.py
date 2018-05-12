class Album:
    def __init__(self, name='None'):
        self.name = name
        self.songs = []
        self.currentSong = 0
    def addSong(self, song):
        if song.album == self.name or self.name == 'All Songs':
            self.songs.append(song)
            return True
        else:
            return False
    def getCurrentSong(self):
        return self.songs[self.currentSong]
    def playNextSong(self):
        self.currentSong += 1
        if self.currentSong >= len(self.songs):
            self.currentSong = 0
        return self.getCurrentSong()
    def playPrevSong(self):
        if self.currentSong == 0:
            self.currentSong = len(self.songs)-1
        else:
            self.currentSong -= 1
        return self.getCurrentSong()
    def getAlbumName(self):
        return self.name
    def getLength(self):
        length = 0
        for song in self.songs:
            length += song.length
        return float(length)/60