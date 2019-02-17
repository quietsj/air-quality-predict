package controllers

import (
	"air-quality-predict/go-python/machine-learning"
	"air-quality-predict/models"
	"encoding/json"
	"fmt"
	"github.com/astaxie/beego"
	"io/ioutil"
)

type MainController struct {
	beego.Controller
}

type CompareController struct {
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
	trainJson := make(map[string]interface{})
	data, err := ioutil.ReadFile(beego.AppConfig.String("modelSave")+"train-model.json")
	models.CheckErr(err)
	err = json.Unmarshal(data, &trainJson)
	models.CheckErr(err)
	gbdtM := trainJson["gbdt_m"].(float64)
	machine_learning.IndexAqi(models.StructToString(aqiData[len(aqiData)-int(gbdtM):]), indexData)
	c.TplName = "pages/charts/index-js.html"
	c.Data["dateHistory"] = indexData["dateHistory"]
	c.Data["aqiHistory"] = indexData["aqiHistory"]
	c.Data["dateFuture"] = indexData["dateFuture"]
	c.Data["aqiFuture"] = indexData["aqiFuture"]
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

func (c *CompareController)Get()  {
	aqiData := make([]models.AirQualityIndex, 0, 0)
	models.Select(&aqiData)
	compareData := make(map[string]interface{})
	machine_learning.CompareAqi(models.StructToString(aqiData[len(aqiData)-machine_learning.TestDays:]), compareData)
	c.TplName = "pages/charts/compare-js.html"
	c.Data["knnReal"] = compareData["knnReal"]
	c.Data["knnPredict"] = compareData["knnPredict"]
	c.Data["knnLabel"] = compareData["knnLabel"]
	c.Data["gbtReal"] = compareData["gbtReal"]
	c.Data["gbtPredict"] = compareData["gbtPredict"]
	c.Data["gbtLabel"] = compareData["gbtLabel"]
	c.Layout = "layout/layout.html"
	c.LayoutSections = make(map[string]string)
	c.LayoutSections["LayoutContent"] = "pages/charts/compare.html"
	c.LayoutSections["Scripts"] = "pages/charts/compare-js.html"
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