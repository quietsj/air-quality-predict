package controllers

import (
	"air-quality-predict/models"
	"fmt"
	"github.com/astaxie/beego"
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
	c.Layout = "layout/layout.html"
	c.TplName = "index.html"
	c.LayoutSections = make(map[string]string)
	c.LayoutSections["LayoutContent"] = "index.html"
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
	htmlData := make(map[string]interface{})
	models.PredictAqi(models.StructToString(aqiData[len(aqiData)-50:]), htmlData)
	c.TplName = "pages/charts/compare-js.html"
	c.Data["ChartReal"] = htmlData["ChartReal"]
	c.Data["ChartPredict"] = htmlData["ChartPredict"]
	c.Data["ChartLabel"] = htmlData["ChartLabel"]
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