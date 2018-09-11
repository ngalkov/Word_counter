# function names should be extracted


def func1():
    var11 = 0

    def func2():
        var2 = 0

    var12 = 0


# test snake-case splitting
def f3_func3():
    v3_var3 = 0


# classes and instances shouldn't be extracted as func name
class Class1():
    classvar0 = 0

    def func4(self):
        classvar1 = 0


class1 = Class1()

# shouldn't be extracted as func name
print(42)
var0 = 1
