# Official U.S. government charts and imagery used on the KOLS pilot-guide post

All files here are cropped or rasterized from U.S. government publications
(public domain). They were not redrawn or AI-generated.

Current cycle used (built 19 November 2026):

## FAA Phoenix VFR Sectional (`kols-sectional-*`)

- Product: Phoenix Sectional Aeronautical Chart, raster GeoTIFF
- Effective: 29 October 2026 to 24 December 2026
- Source ZIP: https://aeronav.faa.gov/visual/10-29-2026/sectional-files/Phoenix.zip
- Catalog: https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/vfr/
- Crop: landscape 1200/630 crop of `Phoenix SEC.tif` centered on KOLS
  (runway 04/22, Nogales VOR/DME OLS, the U.S.–Mexico border, and
  Santa Cruz Valley terrain). Used as the blog hero and index card.

## USGS/NAIP aerial photograph (`kols-aerial.*`)

- Source: USGS NAIP Plus ImageServer, The National Map
  https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPPlus/ImageServer
- Imagery: USDA National Agriculture Imagery Program (NAIP), public domain
  U.S. federal government work (USDA-FSA-APFO / USGS)
- Tile: `m_3111034_sw_12_030_20230805` (Arizona, 0.30 m, 4-band CNIR)
- Acquisition date: 5 August 2023
- Service copyright notice: "USGS, USDA, The National Map: Orthoimagery. March 12, 2025."
- Export: `exportImage` with `bboxSR=3857`, `imageSR=3857` (Web Mercator, undistorted),
  `renderingRule=NaturalColor`, 3840×2560 (3:2 landscape) tightly framed on
  Runway 04/22, Taxiway A, connectors, FBO/terminal ramp, hangars, and
  surrounding Santa Cruz Valley terrain
- Bounding box (EPSG:3857):
  xmin=-12341607.44, ymin=3685733.38, xmax=-12337453.65, ymax=3688502.57
- Used under "The airfield at a glance" on the KOLS pilot-guide post
  (clickable to `kols-aerial.jpg`; responsive 480/800/1200/1600/2400 derivatives)

## FAA instrument approach procedures (`kols-rnav-gps-a.*`, `kols-vor-b.*`)

- Product: d-TPP cycle 2611
- Effective: 0901Z 29 October 2026 to 0901Z 26 November 2026
- RNAV (GPS)-A: https://aeronav.faa.gov/d-tpp/2611/06151RA.PDF
- VOR-B: https://aeronav.faa.gov/d-tpp/2611/06151VB.PDF
- Catalog: https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/dtpp/
- Also linked from https://www.airnav.com/airport/KOLS

Approach plates were rendered with `pdftoppm -png -r 250`; white PDF margins
trimmed only enough to keep the full chart border, header, cycle dates,
plan view, profile, and minimums intact.
