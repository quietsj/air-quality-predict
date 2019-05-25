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

var TestDays = 100

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
	nnlr := make([]float64, 0, 0)
	for _, v := range strings.Split(pr[1], ","){
		v1, err := strconv.ParseFloat(v, 64)
		models.CheckErr(err)
		aqi = append(aqi, v1)
	}
	for _, v := range strings.Split(pr[2], ","){
		v1, err := strconv.ParseFloat(v, 64)
		models.CheckErr(err)
		nnlr = append(nnlr, v1)
	}
	predictAir := make([]models.PredictAir, 0, 0)
	models.PredictAirSelect(date[len(date)-predictDays:][0], &predictAir)
	aqiPredict := make([]float64, 0, 0)
	for _, value := range predictAir{
		aqiPredict = append(aqiPredict, value.AQI)
	}
	//if len(aqiPredict) > 7{
	//	aqiPredict = aqiPredict[len(aqiPredict)-predictDays:]
	//}
	indexData["dateHistory"] = date[len(date)-predictDays-len(aqiPredict):len(date)-predictDays]
	indexData["dateFuture"] = date[len(date)-predictDays:]
	indexData["aqiHistory"] = aqi
	indexData["aqiPredict"] = aqiPredict
	indexData["nnlrFuture"] = nnlr
}

func predictAir()  {
	aqiData := make([]models.AirQualityIndex, 0, 0)
	models.Select(&aqiData)
	stringData := models.StructToString(aqiData[len(aqiData)-TestDays:])
	indexRes := go_python.CallPythonInterface(
		"predict-aqi",
		"index_data",
		[]string{stringData, beego.AppConfig.String("modelSave")})
	predictDays := 7
	pr := strings.Split(indexRes, "\n")
	date := strings.Split(pr[0], ",")
	aqi := make([]float64, 0, 0)
	nnlr := make([]float64, 0, 0)
	for _, v := range strings.Split(pr[1], ","){
		v1, err := strconv.ParseFloat(v, 64)
		models.CheckErr(err)
		aqi = append(aqi, v1)
	}
	for _, v := range strings.Split(pr[2], ","){
		v1, err := strconv.ParseFloat(v, 64)
		models.CheckErr(err)
		nnlr = append(nnlr, v1)
	}
	fmt.Println(date[predictDays:][0], nnlr[0])
	models.PredictInsert(date[predictDays:][0], nnlr[0])

}

func UpdateModel() {
	c := cron.New()
	updateTime := "0 0 0 1 * 1"
	err := c.AddFunc(updateTime, TrainModel)
	models.CheckErr(err)
	c.Start()
	select {}
}

func UpdatePredictAir()  {
	c := cron.New()
	updateTime := "0 1 0/8 * * *"
	err := c.AddFunc(updateTime, predictAir)
	models.CheckErr(err)
	c.Start()
	select {}
}