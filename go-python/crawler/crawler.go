package crawler

import (
	"air-quality-predict/go-python"
	"air-quality-predict/models"
	"fmt"
	"github.com/robfig/cron"
	"time"
)

func CrawlData()  {
	month := fmt.Sprintf("%v", time.Now())[:7]
	res := go_python.CallPythonInterface(
		"crawl-data",
		"get_days",
		[]string{month})
	models.Insert(res)
}

func UpdateDatabase()  {
	c := cron.New()
	updateTime := "0/30 * * * * *"
	err := c.AddFunc(updateTime, CrawlData)
	models.CheckErr(err)
	c.Start()
	select {}
}
