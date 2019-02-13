package main

import (
	_ "air-quality-predict/conf"
	_ "air-quality-predict/models"
	_ "air-quality-predict/routers"
	"github.com/astaxie/beego"
)


// env GOPATH="/Users/quietsj/go"
func main() {
	//models.GetAirQualityIndexData()

	beego.Run()
}