class MyMixin(object):
    mixin_prop = ''

    def get_prop(self):
        return self.mixin_prop.upper()
    #приводим к верхнему регистру передаваемую строку/объект
    def get_upper(self, s):
        if isinstance(s, str): # является ли то, что мы передаем, строкой
            return s.upper() # если строка - приводим к верхнему регистру
        else:
            return s.title.upper() # если это объект(queryset в нашем случае), переводим title в верхний регистр