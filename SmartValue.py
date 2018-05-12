class SmartValue:
    def __init__(self, initValue, speed=10):
        self.value = initValue
        self.initValue = initValue
        self.targetValue = initValue
        self.speed = speed
    def logic(self, deltaTime):
        deltaValue = self.targetValue - self.value
        self.value += deltaValue*deltaTime*self.speed
    def getValue(self):
        return self.value
    def setTarget(self, targetValue):
        self.targetValue = targetValue
    def reset(self):
        self.targetValue = self.initValue
    def getInitPos(self):
        return self.initValue
    def getOff(self):
        return self.targetValue - self.value
    def setValue(self, value):
        self.value = value
    def getTarget(self):
        return self.targetValue