# AcreValue Coding Challenge

The primary aim of AcreValue data science is to value all the agricultural land in the US. We do that by
pulling together various data sources and building a valuation model. Your task for this challenge is to build
and validate a miniature version of our valuation model.

## Objectives

1) Extract and format information from raw data sources.
2) Engineer features from spatial information.
3) Fit and evaluate a valuation model that predicts the price-per-area of a parcel of land.

## How to Submit Your Answer

Email us your code as well as a summary of your findings within 24 hours of receiving this challenge.
(If you're stuck, feel free to email `adriantorchiana@granular.ag` and ask for a small hint or a clarification.)
Ideally your code submission would be a Jupyter notebook or an R or Python script, and your summary can be plain text.

## Data Sources

### Parcel shapefiles

  These files contain information about individual parcels of land in the form of geometry (polygons)
  describing the extent of the parcel and scalar attributes describing various features
  of the parcel.

  `parcels_exam.cpg`

  `parcels_exam.dbf`

  `parcels_exam.prj`

  `parcels_exam.shp`

  `parcels_exam.shx`

  If you're unfamiliar with shapefiles, see <https://en.wikipedia.org/wiki/Shapefile/> for a brief overview.

### CDL raster

  This dataset provides land cover information in raster form, covering a window that intersects
  all parcels in the shapefile. Data are from <https://nassgeodata.gmu.edu/CropScape/> .

  `CDL_2017_clip_20180724175437_1417941736.tif`

  `cdl_mapping.csv`

## Proposed Task Order

If you have not worked much with spatial data, dealing with unfamiliar file types and joining
spatial information can be quite a challenge. We recommend that you complete the tasks in the
following order:

1) Load the parcels and extract their scalar attributes. Each parcel in the shapefile has properties including
`gdd` (growing degree days) and `slope` which are relevant for predicting land value. (Don't worry about
the units in which these scalar attributes are measured: this is a simulated dataset, not real data.) As a warmup
exercise, define `price_per_area` as the `tot_price` (total price) divided by the parcel's `area`, and show us a
histogram of `price_per_area`, which will be the predicted variable (the "Y") for your valuation models.

2) Build and validate a baseline valuation model using only the scalar attributes. In other words, predict
`price_per_area` using `gdd`, `slope`, and the other attributes you loaded in part (1).

3) Calculate features from parcel geometries (polygons) and incorporate these into your model.  What features did
you derive from the parcel geometry and how did you encode them?  How does model performance improve relative to
the model you built in (2)?

4) Join CDL information to parcels and incorporate crop type or other land cover features into your
model. (Careful, this is a spatial join, not a traditional database join!) How does model performance
improve relative to the models you built in (2) and (3)? How did you encode the CDL features?  If you
get stuck on this step, you can get partial credit by giving us summary statistics describing the CDL raster.
For example, how many pixels are there in the raster? How many are coded as `almonds`?
The values in the CDL raster are integer land cover codes; see `cdl_mapping.csv` for what each code represents.

We do not expect that every candidate will complete all of these tasks in the time allotted.
It's okay if you only finish step (1)! Failing to complete everything does *not* disqualify you from consideration.

## Hints and Help

### Useful features

* Parcels of land tend to be more valuable when they are "more convex".
  Can you construct a continuous feature that encodes "convex-ness"?

* The CDL tells you whether parcels were used to grow high-value crops like grapes, almonds, or walnuts.
  How can you extract that information from the raster and encode it as a feature?

### Dataset Visualization

To help orient yourself, here are some screenshots showing both parcel polygons and the CDL raster.
The CDL window we have provided you happens to be located near Camden, California, but that
information isn't necessary for solving the challenge.

Overview (colors correspond to CDL land cover codes):
![CDL_overview](https://i.imgur.com/Fq17Sz1.png)

Detail (the blocks are individual CDL pixels):
![CDL_detail](https://i.imgur.com/ZVWfkSO.png)

Detail with parcels on top of CDL (parcels are in black and partially transparent):
![CDL_detail_with_parcels](https://i.imgur.com/5tvLuu8.png)

Remember, the values in the CDL raster (tif file) are integer land cover codes.
For example, code 75 represents almonds.

### Recommended Tools

If you are doing this challenge in Python, the following libraries may be useful to you:

* [Fiona](https://github.com/Toblerity/Fiona) for loading shapefiles.

* [Shapely](https://github.com/Toblerity/Shapely) for manipulating vectors and shapes.
  For example, you can use Shapely's `object.convex_hull` to easily get a parcel's convex hull.

* [Rasterio](https://github.com/mapbox/rasterio) for working with raster datasets. For example, you can use
  `rasterio.mask.mask` to find the CDL pixels that cover a parcel shape, which will be useful for figuring out
  what crops were grown on the parcel.
