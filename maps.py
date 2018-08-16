import fiona
import numpy as np
import matplotlib.pyplot as plt
import sys
import osr
import shapely
from PIL import Image,TiffImagePlugin
from shapely.geometry import shape
from sklearn.preprocessing import PolynomialFeatures
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from shapely.wkt import loads
import rasterio
import rasterio.features
import rasterio.warp
import rasterio.mask
from scipy import stats
from numpy.polynomial import polynomial as P

import numpy as np
from sklearn.decomposition import PCA
shaper = fiona.open("parcels_exam.shp")
#{'geometry': 'LineString', 'properties': OrderedDict([(u'FID', 'float:11')])}
#first feature of the shapefile
first = shaper.next()
regr = linear_model.LinearRegression()
#im = Image.open('example.tif')
#im.show()
poly = PolynomialFeatures(degree=2)
born="born"
#shx_text=open("parcels_exam.shx", 'r').read()
prj_text = open("parcels_exam.prj", 'r').read()
srs = osr.SpatialReference()

priceper=[]
priceperSlope=[]
priceperSlopeTwo=[]
gdds=[]
gddsExtra=[]
ConvexSpace=[]
while(born!= ""):
    price_per_acre=first['properties']['tot_price'] / first['properties']['area']
    priceper.append(price_per_acre)
    priceperSlope.append(price_per_acre/first['properties']['gdd'])
    priceperSlopeTwo.append(first['properties']['_id'])

    cord = shape(first['geometry'])
    cords=first['geometry']
    #the amount of extior cordinates means more convexity
    ConvexityEx=(len(cord.convex_hull.exterior.coords[:]))
    ConvexSpace.append(cord)
    gdds.append([first['properties']['gdd'], first['properties']['slope'], first['properties']['water'],
             first['properties']['road'], first['properties']['organic'], first['properties']['ponding']])

    gddsExtra.append([first['properties']['gdd'], first['properties']['slope'], first['properties']['water'],
             first['properties']['road'], first['properties']['organic'], first['properties']['ponding'], ConvexityEx])

    try:
        first=shaper.next() #(GeoJSON format)

    except:
        born=""
results={}

im=Image.open('example.tif','r')
tags=im.tag
with rasterio.open("example.tif") as src:
        out_image, out_transform = rasterio.mask.mask(src, ConvexSpace,invert=True,
                                                      crop=False)
        out_meta = src.meta.copy()
        out_image[out_image > 0] += 100
        out_meta.update({'height': out_image.shape[1],
                         'width': out_image.shape[2],
                         'transform': out_transform})
        crop_filename = 'test_crop.tif'
        with rasterio.open(crop_filename, 'w', **out_meta) as dest:
            dest.write(out_image)

        im = Image.open("test_crop.tif")
        im.show()
#print(priceper)
#print(gdds)
#im = Image.open('example.tif')
#im.show()
#gdds=np.transpose(gdds)

pca = PCA(n_components=6)
pca.fit_transform(gdds)
print("how much the variacne is expalined ")
print(pca.explained_variance_ratio_)
print("Pca weights of each")
print(pca.singular_values_)
c, stats = P.polyfit(priceper,gdds,6,full=True)
print("Polynominal Results for regular=")

print(c,stats)
print( "poor results")
print("by having our linear equation and using our data as a test to predict the Price_per_acre we can see how robust our model is")
linear=regr.fit(gdds[:250],priceper[:250])
print(linear.coef_,linear.intercept_)
xres=np.asarray(priceper[250:])
xmult=np.asarray(gdds[250:])
results['coe'] = linear.coef_


#print(results)
#print(polys.coef_)
coef=linear.coef_
output=np.multiply(coef,xmult)
predictions=output.sum(axis=1)+linear.intercept_
print("predicitons")
print("linear R^2=")
print(r2_score(xres, predictions))
print("Polynominal Results for convextion=")
c, stats = P.polyfit(priceper,gddsExtra,7,full=True)
print(c,stats)
print("poor results but worse for convexity")
linear=regr.fit(gddsExtra[:250],priceper[:250])
print(linear.coef_,linear.intercept_)
xres=np.asarray(priceper[250:])
xmult=np.asarray(gddsExtra[250:])
results['coe'] = linear.coef_

coef=linear.coef_
output=np.multiply(coef,xmult)
predictions=output.sum(axis=1)+linear.intercept_
print(predictions)
print("linear with convexity added R^2=")
print(r2_score(xres, predictions))
print("poor results but better")

d=(np.histogram(np.sort(priceper)))

n, bins, patches = plt.hist(x=d, bins='auto')

plt.grid(axis='y', alpha=0.75)
plt.xlabel('PricePErAce')
plt.ylabel('Frequency')
plt.title('My  Price_per_area Histogram')
plt.show()