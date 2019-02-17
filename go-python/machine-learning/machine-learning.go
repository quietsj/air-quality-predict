package machine_learning

import (
	"air-quality-predict/go-python"
	"air-quality-predict/models"
	"github.com/astaxie/beego"
	"github.com/robfig/cron"
	"strconv"
	"strings"
)

var TestDays = 30

func getRealAndPredict(res string) ([]float64, []float64, []string)  {
	pr := strings.Split(res, "\n")
	y_ := make([]float64, 0, 0)
	y := make([]float64, 0, 0)
	yDate := strings.Split(pr[2], ",")
	for _, v := range strings.Split(pr[0], ","){
		v1, err := strconv.ParseFloat(v, 64)
		models.CheckErr(err)
		y_ = append(y_, v1)
	}
	for _, v := range strings.Split(pr[1], ","){
		v1, err := strconv.ParseFloat(v, 64)
		models.CheckErr(err)
		y = append(y, v1)
	}
	return y, y_, yDate
}

func TrainModel()  {
	aqiData := make([]models.AirQualityIndex, 0, 0)
	models.Select(&aqiData)
	res := go_python.CallPythonInterface(
		"train-model",
		"train",
		[]string{
			models.StructToString(aqiData[:len(aqiData)-TestDays]),
			beego.AppConfig.String("modelSave")})
	beego.Debug(res)
}

func CompareAqi(stringData string, compareData map[string]interface{})  {
	knnres := go_python.CallPythonInterface(
		"predict-aqi",
		"nearest_neighbors",
		[]string{stringData, beego.AppConfig.String("modelSave")})
	knny, knny_, knnDate := getRealAndPredict(knnres)
	gbtres := go_python.CallPythonInterface(
		"predict-aqi",
		"gradient_boosting_tree",
		[]string{stringData, beego.AppConfig.String("modelSave")})
	gbty, gbty_, gbtDate := getRealAndPredict(gbtres)
	compareData["knnReal"] = knny
	compareData["knnPredict"] = knny_
	compareData["knnLabel"] = knnDate
	compareData["gbtReal"] = gbty
	compareData["gbtPredict"] = gbty_
	compareData["gbtLabel"] = gbtDate
}

func  IndexAqi(stringData string, indexData map[string]interface{})  {
	indexRes := go_python.CallPythonInterface(
		"predict-aqi",
		"index_data",
		[]string{stringData, beego.AppConfig.String("modelSave")})
	predictDays := 7
	pr := strings.Split(indexRes, "\n")
	date := strings.Split(pr[0], ",")
	aqi := make([]float64, 0, 0)
	for _, v := range strings.Split(pr[1], ","){
		v1, err := strconv.ParseFloat(v, 64)
		models.CheckErr(err)
		aqi = append(aqi, v1)
	}
	aqiLength := len(aqi)
	indexData["dateHistory"] = date[aqiLength-2*predictDays:aqiLength-predictDays]
	indexData["dateFuture"] = date[aqiLength-predictDays:]
	indexData["aqiHistory"] = aqi[aqiLength-2*predictDays:aqiLength-predictDays]
	indexData["aqiFuture"] = aqi[aqiLength-predictDays:]
}

func UpdateModel() {
	c := cron.New()
	updateTime := "0 0 0 1 * *"
	err := c.AddFunc(updateTime, TrainModel)
	models.CheckErr(err)
	c.Start()
	select {}
}