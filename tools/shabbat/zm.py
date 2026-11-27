import json, sys, datetime as dt
from zmanim.util.geo_location import GeoLocation
from zmanim.zmanim_calendar import ZmanimCalendar
from pyluach import dates, parshios
PAGES=[[("לונדון",51.5074,-0.1278,"Europe/London",15),("מנצ'סטר",53.4808,-2.2426,"Europe/London",15),("גייטסהד",54.9527,-1.6036,"Europe/London",15),("אנטוורפן",51.2194,4.4025,"Europe/Brussels",18)],
 [("ניו יורק",40.7128,-74.0060,"America/New_York",18),("לייקווד",40.0821,-74.2097,"America/New_York",18),("מונטריאול",45.5017,-73.5673,"America/Toronto",18),("ירושלים",31.7683,35.2137,"Asia/Jerusalem",40)]]
CITIES=[("לונדון",51.5074,-0.1278,"Europe/London",15),("מנצ'סטר",53.4808,-2.2426,"Europe/London",15),("אנטוורפן",51.2194,4.4025,"Europe/Brussels",18),("ניו יורק",40.7128,-74.0060,"America/New_York",18),("מונטריאול",45.5017,-73.5673,"America/Toronto",18),("ירושלים",31.7683,35.2137,"Asia/Jerusalem",40)]
def next_saturday(d):
    return d+dt.timedelta(days=(5-d.weekday())%7)
today=dt.date.fromisoformat(sys.argv[1]) if len(sys.argv)>1 else dt.date.today()
sat=next_saturday(today);fri=sat-dt.timedelta(days=1)
rows=[]
for name,lat,lon,tz,off in CITIES:
    g=GeoLocation(name,lat,lon,tz,elevation=0)
    c=ZmanimCalendar(geo_location=g,date=fri,candle_lighting_offset=off)
    cl=c.candle_lighting()
    s=ZmanimCalendar(geo_location=g,date=sat)
    tz85=s.tzais({'degrees':8.5})
    rt=s.tzais_72()
    f=lambda x:x.strftime('%H:%M')
    rows.append({"city":name,"candles":f(cl),"motzei":f(tz85),"rt":f(rt)})
def h12(x):
    return f"{(x.hour-1)%12+1}:{x.minute:02d}"
ZROWS=[("הדלקת נרות","fri","candles"),("שקיעה ער״ש","fri","shkia"),("סוזק״ש גר״א","sat","shma_gra"),("סוז״ת גר״א","sat","tfila_gra"),("חצות","sat","chatzos"),("שקיעה","sat","shkia"),("מוצאי שבת","sat","motzei"),("רבינו תם","sat","rt")]
pages=[]
for pg in PAGES:
    cols=[]
    for name,lat,lon,tz,off in pg:
        g=GeoLocation(name,lat,lon,tz,elevation=0)
        f_=ZmanimCalendar(geo_location=g,date=fri,candle_lighting_offset=off);s_=ZmanimCalendar(geo_location=g,date=sat)
        v={"fri":{"candles":f_.candle_lighting(),"shkia":f_.sunset()},"sat":{"shma_mga":s_.sof_zman_shma_mga(),"shma_gra":s_.sof_zman_shma_gra(),"tfila_gra":s_.sof_zman_tfila_gra(),"chatzos":s_.chatzos(),"shkia":s_.sunset(),"motzei":s_.tzais({'degrees':8.5}),"rt":s_.tzais_72()}}
        cols.append({"city":name,"vals":[h12(v[d][k]) for _,d,k in ZROWS]})
    pages.append(cols)
hd=dates.GregorianDate(sat.year,sat.month,sat.day).to_heb()
parsha=parshios.getparsha_string(hd,israel=False,hebrew=True)
heb=hd.hebrew_date_string()
fhd=dates.GregorianDate(fri.year,fri.month,fri.day).to_heb().hebrew_date_string()
out={"date":sat.isoformat(),"parsha":parsha,"hebdate":heb,"frihebdate":fhd,"rows":rows,"zrows":[r[0] for r in ZROWS],"pages":pages}
print(json.dumps(out,ensure_ascii=False,indent=1))
json.dump(out,open('week.json','w'),ensure_ascii=False)
