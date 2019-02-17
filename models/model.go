package models

import (
	"fmt"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/orm"
	_ "github.com/lib/pq"
	"strings"
	"time"
)

type AirQualityIndex struct {
	Date time.Time `orm:"pk"`
	AQI float64
	QualityGrade string `orm:"size(20)"`
	PM2_5 float64
	PM10 float64
	SO2 float64
	CO float64
	NO2 float64
	O3_8h float64
}


func init()  {
	psqlInfo := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		beego.AppConfig.String("postgresqlHost"), beego.AppConfig.String("postgresqlPort"),
		beego.AppConfig.String("postgresqlUser"), beego.AppConfig.String("postgresqlPassword"),
		beego.AppConfig.String("postgresqlDbname"))
	err := orm.RegisterDriver("postgres", orm.DRPostgres)
	CheckErr(err)
	err = orm.RegisterDataBase("default", "postgres", psqlInfo)
	CheckErr(err)
	orm.RegisterModel(new(AirQualityIndex))
	err = orm.RunSyncdb("default", false, true)
	CheckErr(err)
}

func Insert(insertData string)  {
	o := orm.NewOrm()
	r := o.Raw("alter table air_quality_index add constraint unique_date unique(date)")
	_, err := r.Exec()
	CheckErr(err)
	dataList := strings.Split(string(insertData), "\n")
	values := "(?, ?, ?, ?, ?, ?, ?, ?, ?)"
	time1 := time.Now()
	for _, raw := range dataList{
		rawList := strings.Split(raw, ",")
		r = o.Raw(fmt.Sprintf("insert into air_quality_index values %s", values), rawList)
		_, err = r.Exec()
		CheckErr(err)
	}
	beego.Debug(fmt.Sprintf("%v s insert finish!", time.Since(time1).Seconds()))
}

func Select(aqi *[]AirQualityIndex)  {
	o := orm.NewOrm()
	time1 := time.Now()
	num, _ := o.Raw("select * from air_quality_index order by date asc").QueryRows(aqi)
	beego.Debug(fmt.Sprintf("%v s %d raws select finish!", time.Since(time1).Seconds(), num))
}

func StructToString(aqiData []AirQualityIndex) string {
	stringData := ""
	for i, v:= range aqiData{
		r := fmt.Sprintf("%v,%v,%v,%v,%v,%v,%v,%v,%v",
			v.Date,
			v.AQI,
			v.QualityGrade,
			v.PM2_5,
			v.PM10,
			v.SO2,
			v.CO,
			v.NO2,
			v.O3_8h)
		if i == len(aqiData) - 1{
			stringData += r
		}else {
			stringData += r + "\n"
		}
	}
	return stringData
}


func CheckErr(err error) {
	if err != nil {
		beego.Error(err)
	}
}