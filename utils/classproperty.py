class ClassProperty(property):
    def __get__(self, instance, cls):
        return classmethod(self.fget).__get__(instance, cls)()
