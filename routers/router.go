package routers

import (
	"air-quality-predict/controllers"
	"github.com/astaxie/beego"
)

func init() {
    beego.Router("/", &controllers.MainController{})
	beego.Router("/history", &controllers.HistoryController{})
    beego.Router("/login", &controllers.LoginController{})
	beego.Router("/register", &controllers.RegisterController{})
}
