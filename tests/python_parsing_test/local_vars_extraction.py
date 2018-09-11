# vars local to function should be extracted


def func1():
    var11 = 0

    def func2():
        var2 = 0

    var12 = 0
    var13, var14 = 0, 0


# test snake-case splitting
def f3_func3():
    v3_var3 = 0


# classes and instances shouldn't be extracted as local vars
class Class1:
    classvar0 = 0  # shouldn't be extracted as local var

    def func4(self):
        classvar1 = 0


class1 = Class1()

# shouldn't be extracted as local var
print(42)
var0 = 1
