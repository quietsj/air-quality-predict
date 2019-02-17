package go_python

import (
	"air-quality-predict/models"
	"github.com/astaxie/beego"
	"github.com/sbinet/go-python"
)

func init()  {
	err := python.Initialize()
	if err != nil {
		models.CheckErr(err)
	}
}

var PyStr = python.PyString_FromString
var GoStr = python.PyString_AS_STRING

// ImportModule will import python module from given directory
func ImportModule(dir, name string) *python.PyObject {
	sysModule := python.PyImport_ImportModule("sys") // import sys
	path := sysModule.GetAttrString("path")       // path = sys.path
	err := python.PyList_Insert(path, 0, PyStr(dir)) // path.insert(0, dir)
	if err != nil{
		panic(err)
	}
	return python.PyImport_ImportModule(name)              // return __import__(name)
}

func CallPythonInterface(moduleName, interfaceName string, args []string) string {
	module := ImportModule(beego.AppConfig.String("modulePath"), moduleName)
	pythonInterface := module.GetAttrString(interfaceName)
	pythonInterfaceArgs := python.PyTuple_New(len(args))
	for i, arg := range args{
		err := python.PyTuple_SetItem(pythonInterfaceArgs, i, PyStr(arg))
		models.CheckErr(err)
	}
	return GoStr(pythonInterface.Call(pythonInterfaceArgs, python.Py_None))
}