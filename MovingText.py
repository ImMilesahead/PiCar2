class MovingText:
    def __init__(self, text, maxLength):
        self.text = text
        self.displayText = self.text
        self.maxLength = maxLength
        self.startchar = 0
        self.endChar = 0
    def logic(self, deltaTime):
        if len(self.text) > self.maxLength:
            self.displayText = self.text[:self.maxLength]
            '''
            self.startchar += deltaTime
            if self.startchar > len(self.text):
                self.startchar = 0
                self.endChar = self.maxLength
            self.endChar = self.startchar + self.maxLength
            self.displayText = self.text[int(self.startchar):int(self.endChar)] 
            '''
    def getText(self):
        return self.displayText