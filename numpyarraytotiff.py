from osgeo import gdal, osr
import numpy as np
#create a bogus grid
mag_grid = np.arange(-500, 500, .1).reshape((100, 100))
lats = np.arange(-10,90,1.)
lons = np.arange(-10,90,1.)

xres = lons[1] - lons[0]
yres = lats[1] - lats[0]
ysize = len(lats)
xsize = len(lons)
ulx = lons[0] - (xres / 2.)
uly = lats[-1] - (yres / 2.)


driver = gdal.GetDriverByName('GTiff')
ds = driver.Create('output.tif',xsize, ysize, 1, gdal.GDT_Byte)
##################################
#pixel type of gdal.GDT_Float32 results in transparent image
##################################

# this assumes the projection is Geographic lat/lon WGS 84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)
ds.SetProjection(srs.ExportToWkt())
gt = [ulx, xres, 0, uly, 0, yres ]
ds.SetGeoTransform(gt)
outband=ds.GetRasterBand(1)
outband.SetStatistics(np.min(mag_grid), np.max(mag_grid), np.average(mag_grid), np.std(mag_grid))
outband.WriteArray(mag_grid)
print outband
ds = None