package main

import (
	_ "air-quality-predict/conf"
	_ "air-quality-predict/go-python"
	"air-quality-predict/go-python/crawler"
	"air-quality-predict/go-python/machine-learning"
	_ "air-quality-predict/models"
	_ "air-quality-predict/routers"
	"github.com/astaxie/beego"
)

// sudo env GOPATH=$GOPATH bee run, scp - admin@39.108.12.40:/home/admin/go/src/air-quality-predict/
// CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build main.go
func main() {
	//machine_learning.TestMachineLearning()
	//crawler.CrawlData()
	go crawler.UpdateDatabase()
	go machine_learning.UpdateModel()
	beego.Run()
}