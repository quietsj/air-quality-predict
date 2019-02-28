package machine_learning

import (
	"air-quality-predict/go-python"
	"air-quality-predict/models"
	"fmt"
	"github.com/astaxie/beego"
	"github.com/robfig/cron"
	"strconv"
	"strings"
)

var TestDays = 30

func TrainModel()  {
	aqiData := make([]models.AirQualityIndex, 0, 0)
	models.Select(&aqiData)
	res := go_python.CallPythonInterface(
		"train-model",
		"train",
		[]string{
			models.StructToString(aqiData[:len(aqiData)-TestDays]),
			beego.AppConfig.String("modelSave")})
	beego.Informational(res)
}

func History(start, end string, HistoryData map[string]interface{})  {
	aqiData := make([]models.AirQualityIndex, 0, 0)
	models.DateSelect(&aqiData, start, end)
	date := make([]string, 0 ,0)
	aqi := make([]float64, 0 ,0)
	for _, v := range aqiData{
		date = append(date, fmt.Sprintf("%v", v.Date)[:10])
		aqi = append(aqi, v.AQI)
	}
	HistoryData["Date"] = date
	HistoryData["AQI"] = aqi
}

func  Index(stringData string, indexData map[string]interface{})  {
	indexRes := go_python.CallPythonInterface(
		"predict-aqi",
		"index_data",
		[]string{stringData, beego.AppConfig.String("modelSave")})
	predictDays := 7
	pr := strings.Split(indexRes, "\n")
	date := strings.Split(pr[0], ",")
	aqi := make([]float64, 0, 0)
	knn := make([]float64, 0, 0)
	gbdt := make([]float64, 0, 0)
	nn := make([]float64, 0, 0)
	for _, v := range strings.Split(pr[1], ","){
		v1, err := strconv.ParseFloat(v, 64)
		models.CheckErr(err)
		aqi = append(aqi, v1)
	}
	for _, v := range strings.Split(pr[2], ","){
		v1, err := strconv.ParseFloat(v, 64)
		models.CheckErr(err)
		knn = append(knn, v1)
	}
	for _, v := range strings.Split(pr[3], ","){
		v1, err := strconv.ParseFloat(v, 64)
		models.CheckErr(err)
		gbdt = append(gbdt, v1)
	}
	for _, v := range strings.Split(pr[4], ","){
		v1, err := strconv.ParseFloat(v, 64)
		models.CheckErr(err)
		nn = append(nn, v1)
	}
	indexData["dateHistory"] = date[:predictDays]
	indexData["dateFuture"] = date[predictDays:]
	indexData["aqiHistory"] = aqi
	indexData["knnFuture"] = knn
	indexData["gbdtFuture"] = gbdt
	indexData["nnFuture"] = nn
}

func UpdateModel() {
	c := cron.New()
	updateTime := "0 0 0 1 * 1"
	err := c.AddFunc(updateTime, TrainModel)
	models.CheckErr(err)
	c.Start()
	select {}
}