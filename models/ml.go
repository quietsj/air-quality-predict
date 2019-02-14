package models

import (
	"fmt"
	"github.com/astaxie/beego"
	"github.com/sbinet/go-python"
	"strconv"
	"strings"
)

func init()  {
	err := python.Initialize()
	if err != nil {
		CheckErr(err)
	}
}

var PyStr = python.PyString_FromString
var GoStr = python.PyString_AS_STRING

func GetAirQualityIndexData()  {
	aqiData := make([]AirQualityIndex, 0, 0)
	Select(&aqiData)
	//TrainModel(structToString(aqiData[:len(aqiData)-50]))
	htmlData := make(map[string]interface{})
	PredictAqi(StructToString(aqiData[len(aqiData)-50:]), htmlData)
}

func TrainModel(stringData string)  {
	trainModule := importModule(beego.AppConfig.String("modulePath"), beego.AppConfig.String("trainModuleName"))
	train := trainModule.GetAttrString("train")
	// trainArgs = tuple(stringData, path)
	trainArgs := python.PyTuple_New(2)
	err := python.PyTuple_SetItem(trainArgs, 0, PyStr(stringData))
	if err != nil{
		CheckErr(err)
	}
	err = python.PyTuple_SetItem(trainArgs, 1, PyStr(beego.AppConfig.String("modelSave")))
	if err != nil{
		CheckErr(err)
	}
	res := train.Call(trainArgs, python.Py_None)
	beego.Debug(GoStr(res))
}

func PredictAqi(stringData string, htmlData map[string]interface{})  {
	predictModule := importModule(beego.AppConfig.String("modulePath"), beego.AppConfig.String("predictModuleName"))
	nearestNeighbors := predictModule.GetAttrString("nearest_neighbors")
	// trainArgs = tuple(stringData, path)
	nearestNeighborsArgs := python.PyTuple_New(2)
	err := python.PyTuple_SetItem(nearestNeighborsArgs, 0, PyStr(stringData))
	if err != nil{
		CheckErr(err)
	}
	err = python.PyTuple_SetItem(nearestNeighborsArgs, 1, PyStr(beego.AppConfig.String("modelSave")))
	if err != nil{
		CheckErr(err)
	}
	res := nearestNeighbors.Call(nearestNeighborsArgs, python.Py_None)
	pr := strings.Split(GoStr(res), "\n")
	y_ := make([]float64, 0, 0)
	y := make([]float64, 0, 0)
	yDate := strings.Split(pr[2], ",")
	for _, v := range strings.Split(pr[0], ","){
		v1, err := strconv.ParseFloat(v, 64)
		CheckErr(err)
		y_ = append(y_, v1)
	}
	for _, v := range strings.Split(pr[1], ","){
		v1, err := strconv.ParseFloat(v, 64)
		CheckErr(err)
		y = append(y, v1)
	}
	htmlData["ChartReal"] = y
	htmlData["ChartPredict"] = y_
	htmlData["ChartLabel"] = yDate
}

// ImportModule will import python module from given directory
func importModule(dir, name string) *python.PyObject {
	sysModule := python.PyImport_ImportModule("sys") // import sys
	path := sysModule.GetAttrString("path")       // path = sys.path
	err := python.PyList_Insert(path, 0, PyStr(dir)) // path.insert(0, dir)
	if err != nil{
		panic(err)
	}
	return python.PyImport_ImportModule(name)              // return __import__(name)
}

func StructToString(aqiData []AirQualityIndex) string {
	stringData := ""
	for i, v:= range aqiData{
		r := fmt.Sprintf("%v,%v,%v,%v,%v,%v,%v,%v,%v",
			v.Date,
			v.AQI,
			v.QualityGrade,
			v.PM2_5,
			v.PM10,
			v.SO2,
			v.CO,
			v.NO2,
			v.O3_8h)
		if i == len(aqiData) - 1{
			stringData += r
		}else {
			stringData += r + "\n"
		}
	}
	return stringData
}
