import pygame
class MediaPlayer:
    def __init__(self):
        self.currentSong = None
        self.currentPlaylist = None
        self.paused = False
        pygame.mixer.init()
    def logic(self):
        if not self.paused and not pygame.mixer.music.get_busy():
            self.nextSong()
    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True
    def unpause(self):
        pygame.mixer.music.unpause()
        self.paused = False
    def playSong(self, song):
        self.currentSong = song
        pygame.mixer.music.load(song.getRealPath())
        pygame.mixer.music.play()
        print('Playing song: ' + song.name)
    def nextSong(self):
        if not self.playlist == None:
            self.playSong(self.playlist.playNextSong())
    def prevSong(self):
        if not self.playlist == None:
            self.playSong(self.playlist.playPrevSong())
    def playPlaylist(self, playlist):
        self.playlist = playlist
        self.playSong(self.playlist.getCurrentSong())
    def getCurSong(self):
        return self.currentSong
    def getCurPlaylist(self):
        return self.currentPlaylist
    def toggle(self):
        if not self.playlist == None:
            if pygame.mixer.music.get_busy:
                if self.paused:
                    self.unpause()
                else:
                    self.pause()
            else:
                self.playSong(self.playlist.getCurrentSong())