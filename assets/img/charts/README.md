# Official FAA charts used on the KOLS pilot-guide post

All files here are cropped or rasterized from current-cycle U.S. government
publications (public domain). They were not redrawn or AI-generated.

Current cycle used (built 19 November 2026):

## FAA Phoenix VFR Sectional (`kols-sectional-*`)

- Product: Phoenix Sectional Aeronautical Chart, raster GeoTIFF
- Effective: 29 October 2026 to 24 December 2026
- Source ZIP: https://aeronav.faa.gov/visual/10-29-2026/sectional-files/Phoenix.zip
- Catalog: https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/vfr/
- Crop: landscape 1200/630 crop of `Phoenix SEC.tif` centered on KOLS
  (runway 04/22, Nogales VOR/DME OLS, the U.S.–Mexico border, and
  Santa Cruz Valley terrain). Used as the blog hero and index card.

## FAA Chart Supplement airport sketch (`kols-airport-sketch.*`)

- Product: Chart Supplement Southwest, airport listing/sketch for OLS (KOLS)
- Effective: 29 October 2026 to 24 December 2026
- Source PDF: https://aeronav.faa.gov/afd/29Oct2026/sw_68_29OCT2026.pdf
- Search: https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/dafd/search/results/?cycle=2611&ident=OLS
- Note: KOLS has no published FAA d-TPP Airport Diagram (`06151AD.PDF` is 404).
  The official field layout graphic is this Chart Supplement sketch.

## FAA instrument approach procedures (`kols-rnav-gps-a.*`, `kols-vor-b.*`)

- Product: d-TPP cycle 2611
- Effective: 0901Z 29 October 2026 to 0901Z 26 November 2026
- RNAV (GPS)-A: https://aeronav.faa.gov/d-tpp/2611/06151RA.PDF
- VOR-B: https://aeronav.faa.gov/d-tpp/2611/06151VB.PDF
- Catalog: https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/dtpp/
- Also linked from https://www.airnav.com/airport/KOLS

Rendered with `pdftoppm -png -r 250` (plates) or `-r 400` (sketch); white PDF
margins trimmed only enough to keep the full chart border, header, cycle dates,
plan view, profile, and minimums intact.
