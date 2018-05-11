from helper import *
'''
Button is depreceated use MenuItem instead
'''

class Button:
    def __init__(self, dim=(0, 0, 100, 100), color=Color.Primary, text='None', text_size=60, text_color=Color.Text, text_offset=(0, 0), callback=None, width=2, args=None, image=None, image_offset=(3, 3), image_offscale=(6, 6), drawRect=True):
        self.skrn = skrn
        self.dim = dim
        self.color = color
        self.drawRect = drawRect
        self.text = text
        self.image = image
        self.image_offset= image_offset
        self.image_offscale = image_offscale
        if not image == None:
            self.image = pygame.image.load(PICTURES_PATH + image)
            self.image = pygame.transform.scale(self.image, (self.dim[2]-self.image_offscale[0], self.dim[3]-self.image_offscale[1]))
        self.text_size = text_size
        self.text_color = text_color
        self.text_offset = text_offset
        self.callback = callback
        self.width = width
        self.args=args

    def set_dim(self, dim):
        self.dim = dim
    
    def draw(self):
        if self.drawRect:
            pygame.draw.rect(self.skrn, self.color, self.dim, self.width)
        # draw text
        if not self.image == None:
            self.skrn.blit(self.image, (self.dim[0]+self.image_offset[0], self.dim[1]+self.image_offset[1]))
        else:
            text(skrn, self.text, (self.dim[0] + self.text_offset[0], self.dim[1] + self.text_offset[1]), self.text_size, self.text_color)

    def logic(self):
        '''mouse_pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()
        if mouse_pos[0] >= self.dim[0] and mouse_pos[0] <= self.dim[0] + self.dim[2] and mouse_pos[1] >= self.dim[1] and mouse_pos[1] <= self.dim[1] + self.dim[3]:
            if pressed[0]:
               self.callback()'''
        pass

    def event(self, event):
        if event == 'Tap':
            mouse_pos = pygame.mouse.get_pos()
            self.start_mouse_pos = mouse_pos
            if mouse_pos[0] >= self.dim[0] and mouse_pos[0] <= self.dim[0] + self.dim[2] and mouse_pos[1] >= self.dim[1] and mouse_pos[1] <= self.dim[1] + self.dim[3]:
                if self.args == None:
                    if not self.callback == None:
                        self.callback()
                else:
                    self.callback(self.args)
