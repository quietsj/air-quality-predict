package conf

import (
	"air-quality-predict/models"
	"fmt"
	"github.com/astaxie/beego"
)

func init() {
	err := beego.SetLogger("file", fmt.Sprintf(`{"filename":"%s"}`, beego.AppConfig.String("logOutput")))
	models.CheckErr(err)
}