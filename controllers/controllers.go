package controllers

import (
	"air-quality-predict/go-python/machine-learning"
	"air-quality-predict/models"
	"fmt"
	"github.com/astaxie/beego"
)

type MainController struct {
	beego.Controller
}

type HistoryController struct {
	beego.Controller
}

type LoginController struct {
	beego.Controller
}

type RegisterController struct {
	beego.Controller
}

func (c *MainController) Get() {
	aqiData := make([]models.AirQualityIndex, 0, 0)
	models.Select(&aqiData)
	indexData := make(map[string]interface{})
	machine_learning.Index(
		models.StructToString(aqiData[len(aqiData)-machine_learning.TestDays:]),
		indexData)
	c.TplName = "pages/charts/index-js.html"
	c.Data["dateHistory"] = indexData["dateHistory"]
	c.Data["aqiHistory"] = indexData["aqiHistory"]
	c.Data["dateFuture"] = indexData["dateFuture"]
	c.Data["knnFuture"] = indexData["knnFuture"]
	c.Data["gbdtFuture"] = indexData["gbdtFuture"]
	c.Data["nnFuture"] = indexData["nnFuture"]
	c.Layout = "layout/layout.html"
	c.LayoutSections = make(map[string]string)
	c.LayoutSections["LayoutContent"] = "index.html"
	c.LayoutSections["Scripts"] = "pages/charts/index-js.html"
}

type user struct {
	Username string `form:"username"`
	Password string `form:"password"`
	Check string `form:"check"`
}
func (c *LoginController)Post()  {
	u := user{}
	err := c.ParseForm(&u)
	models.CheckErr(err)
	fmt.Println(u.Check == "on")
	c.Redirect("/", 302)
}

type date struct {
	StartDate string `form:"start_date"`
	EndDate string `form:"end_date"`
}

func (c *HistoryController)Post()  {
	d := date{}
	err := c.ParseForm(&d)
	models.CheckErr(err)
	HistoryData := make(map[string]interface{})
	machine_learning.History(d.StartDate, d.EndDate, HistoryData)
	c.TplName = "pages/charts/history-js.html"
	c.Layout = "layout/layout.html"
	c.Data["Pstart"] = d.StartDate
	c.Data["Pend"] = d.EndDate
	c.Data["Date"] = HistoryData["Date"]
	c.Data["AQI"] = HistoryData["AQI"]
	c.LayoutSections = make(map[string]string)
	c.LayoutSections["LayoutContent"] = "pages/charts/history.html"
	c.LayoutSections["Scripts"] = "pages/charts/history-js.html"
}

func (c *HistoryController)Get()  {
	aqiData := make([]models.AirQualityIndex, 0, 0)
	models.Select(&aqiData)
	start := fmt.Sprintf("%v", aqiData[len(aqiData)-30].Date)[:10]
	end := fmt.Sprintf("%v", aqiData[len(aqiData)-1].Date)[:10]
	HistoryData := make(map[string]interface{})
	machine_learning.History(start, end, HistoryData)
	c.TplName = "pages/charts/history-js.html"
	c.Layout = "layout/layout.html"
	c.Data["Start"] = start
	c.Data["End"] = end
	c.Data["Date"] = HistoryData["Date"]
	c.Data["AQI"] = HistoryData["AQI"]
	c.LayoutSections = make(map[string]string)
	c.LayoutSections["LayoutContent"] = "pages/charts/history.html"
	c.LayoutSections["Scripts"] = "pages/charts/history-js.html"
}

func (c *LoginController)Get()  {
	c.TplName = "pages/usage/login.html"
}

func (c *RegisterController)Get()  {
	c.TplName = "pages/usage/register.html"
}

func (c *RegisterController)Post()  {
	fmt.Println(c.GetString("username"), c.GetString("password"), c.GetString("confirm"))
	c.Redirect("/", 302)
}