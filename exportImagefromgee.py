import ee
ee.Initialize()

# Dongdong Kong, Sun Yat-sen University
# 13 Jan, 2018
# resample data into 0.05 deg


def resample(img):
    targetScale = 0.05
    img = (img.reproject(ee.Projection('EPSG:4326').scale(targetScale/10, targetScale/10))
           .reduceResolution(reducer=ee.Reducer.mean(), maxPixels=3600)
           .reproject(ee.Projection('EPSG:4326').scale(targetScale, targetScale))
           .copyProperties(img, ['system:time_start']))
    return img


def calEmiss(img):
    return (img.reduce(ee.Reducer.mean()).multiply(0.002).add(0.49)
            .copyProperties(img, ['system:time_start', 'system:id']))

# return list object of ImgCol date
def getDate(img):
    return ee.Date(ee.Image(img).get('system:time_start')).format('yyyy-MM-dd')


def ExportImgCol(ImgCol, name):
    n = ImgCol.size().getInfo()
    dates = ImgCol.toList(n).map(getDate).getInfo()

    for i in range(n):
        date = dates[i]
        img = ee.Image(ImgCol.filterDate(date).first())
        file = "%s_%s" % (name, date.format("YYYY-mm-dd"))
        task = ee.batch.Export.image.toDrive(
            image=img,
            description=file,
            crs='EPSG:4326',
            region=region,
            dimensions='842x681',
            maxPixels=1e10,
            skipEmptyTiles=True,
            folder=folder)
        # fileFormat = 'csv')
        task.start()
        print file

# import multiprocessing as mp
# pool = mp.Pool(processes=4)
# def ExportImgCol(date):
#     name = 'hardvalue'
#     img = ee.Image(ImgCol.filterDate(date).first())
#     file = "%s_%s" % (name, date.format("YYYY-mm-dd"))
#     task = ee.batch.Export.image.toDrive(
#         image=img,
#         description=file,
#         crs='EPSG:4326',
#         region=region,
#         dimensions='842x681',
#         maxPixels=1e10,
#         skipEmptyTiles=True,
#         folder=folder)
#     # fileFormat = 'csv')
#     task.start()
# pool.map_async(ExportImgCol,dates)
# pool.close()
# pool.join()
#print(dates);
bound = ee.Geometry.Rectangle(
    [111.975, -44.025, 154.075, -9.975], 'EPSG:4326', False)
region = ee.Feature(bound).geometry().getInfo()["coordinates"]

# folder = "AU-flow/LAI"
folder = "AU-flow/Emiss"
# name = 'MCD15A3H_006_Lai'
name = 'MOD11A2_006_Emiss'
# load ImgCol
# Land Surface Temperature and Emissivity 8-Day Global 1km
filterDate = ee.Filter.date('2008-01-01', "2016-12-31")
ImgCol = (ee.ImageCollection('MODIS/006/MOD11A2')
          .select(['Emis_31', 'Emis_32'])
          .filter(filterDate)
          .map(calEmiss))
ExportImgCol(ImgCol, name)
