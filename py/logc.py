colors = {
	'black'    : 30,   #  黑色
    'red'      : 31,   #  红色
    'green'    : 32,   #  绿色
    'yellow'   : 33,   #  黄色
    'blue'     : 34,   #  蓝色
    'purple'   : 35,   #  紫红色
    'cyan'     : 36,   #  青蓝色
    'white'    : 37,   #  白色
}
def printINFO(s):
	print("\033[%sm"%colors['green'],"--INFO--",'\033[0m',s)

def printWARN(s):
	print("\033[%sm"%colors['red'],"--WARN--",'\033[0m',s)

def printTEST(s):
	print("\033[%sm"%colors['purple'],"--INFO--",'\033[0m',s)