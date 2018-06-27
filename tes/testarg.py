# -*-coding:utf-8
def foo(arg1,arg2="OK",*tupleArg,**dictArg):
    print "arg1=",arg1
    print "arg2=",arg2
    for i,element in enumerate(tupleArg):
        print "tupleArg %d-->%s" % (i,str(element))
    for  key in dictArg:
        print "dictArg %s-->%s" %(key,dictArg[key])

myList=["my1","my2"]
myDict={"name":"Tom","age":22}
foo("formal_args",arg2="argSecond",a=1)
print "*"*40
foo(123,myList,myDict)
print "*"*40
foo(123,rt=123,*myList,**myDict)