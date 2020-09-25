# Setup of emissions for complete Ruisdael large domain

To be used with DALES code, including emission options [dalesteam/dales/4.2_emission](https://github.com/dalesteam/dales/tree/4.2_emission)

## Create hourly emission files

Emission files can be created for any date, but are only valid for the year 2017. This is done by running the create_hourly_emission Python script pointing to the [emisoptions file](emisoptions_large_domain.txt) in this folder. Please note that current base files are based on the large Ruisdael domain andhave a spatial resolution of 200 meter. More information is included in the emission base files, e.g. [co2_2017_1_power.nc](../co2_2017_1_power.nc).

All options for the emissions are specified in the [emisoptions file](emisoptions_large_domain.txt).
Starting date+hour and number of hourly emission files that are required, i.e.:

```
startyear   2017
startmonth     8
startday      19
starthour      0
runlength     24
```

Extent of the domain (in coordinates used in the HARMONIE NWP model) and vertical extent of emissions to be included, i.e.:

```
xmin   910000
xmax  1082600
ymin   940000
ymax  1055000
zmin  0
zmax  200
```

Tracers for which emission files have to be created plus on eor more pairs of an emission category name and a SNAP category time profile to use for temporal disaggration i.e.:

```
tracer co2 1_power 1 2_residential_commercial 2 3_industrial_combustion 3 4_industrial_processes 4 5_fossil_fuels 5 7_road 7 8_mobile 8 9_waste 9 10_agriculture 10
```

