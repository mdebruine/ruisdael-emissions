def reademisoptions(path2file, show_log=False):
    
    from datetime import datetime
    from datetime import timedelta

    """
    Create variables required for the creation of hourly emission files, i.e.:
    1. Datetime object for iteration
    2. Domain specifications
    3. Tracer specifications

    Required input: textfile with combinations of keywords and values. Example:

    ----
    startyear   2017
    startmonth     1
    startday       1
    starthour      0
    runlength     24

    xmin 115000
    xmax 125000
    ymin 410000
    ymax 456700

    tracer co2 verkeer 1 power 7 residential 4
    tracer ch4 landbouw 10 waste 9
    ----
    """
    
    tracers, sources, categos = [], [], []

    with open(path2file, "r") as fh:
        for line in fh.readlines():
            words = line.split()

            if len(words) > 0:
                keyword = words[0]
                values  = words[1:]

                if keyword == 'startyear':
                    startyear  = int(values[0])
                elif keyword == 'startmonth':
                    startmonth = int(values[0])
                elif keyword == 'startday':
                    startday   = int(values[0])
                elif keyword == 'starthour':
                    starthour  = int(values[0])
                elif keyword == 'runlength':
                    runlength  = int(values[0])

                elif keyword == 'xmin':
                    xmin = int(values[0])
                elif keyword == 'xmax':
                    xmax = int(values[0])
                    
                elif keyword == 'ymin':
                    ymin = int(values[0])
                elif keyword == 'ymax':
                    ymax = int(values[0])
                    
                elif keyword == 'zmin':
                    zmin = int(values[0])
                elif keyword == 'zmax':
                    zmax = int(values[0])
                    
                elif keyword == 'tracer':
                    tracers.append(values[0])
                    sources.append(values[1::2])
                    categos.append(values[2::2])

    domainbounds = {'xmin': xmin, 'xmax': xmax, 
                    'ymin': ymin, 'ymax': ymax, 
                    'zmin': zmin, 'zmax': zmax}
    
    if show_log:
        for it, tracer in enumerate(tracers):
            print("Tracer: ", tracer, )
            for isrc, source in enumerate(sources[it]):
                print("{:02d}".format(int(categos[it][isrc])), source)
            print()
         
    tstart = datetime(startyear, startmonth, startday, starthour)
    tend   = tstart + timedelta(hours=runlength)

    if show_log:
        print("start:", tstart.strftime("%Y-%m-%d %H:%M"))
        print("end  :", tend  .strftime("%Y-%m-%d %H:%M"), "\n")

    return domainbounds, tstart, tend, tracers, sources, categos

def loadsnap():
    
    import numpy as np
    
    """
    Create arrays for temporal dissaggregation based on Denier van der Gon et al. (2010)
    using 10 SNAP cstegories
    
    INPUT: None
    OUTPUT: 
    
    tprof_mnth, np.array 10x12
    tprof_week, np.array 10x7
    tprof_hour, np.array 10x24
    
    """
    nsnap = 10

    tprof_mnth = np.zeros([nsnap, 12])
    tprof_week = np.zeros([nsnap, 7])
    tprof_hour = np.zeros([nsnap, 24])

    # SNAP 1 - Power generation
    tprof_mnth[0] = [1.20, 1.15, 1.05, 1.00, 0.90, 0.85, 0.80, 0.87, 0.95, 1.00, 1.08, 1.15]
    tprof_week[0] = [1.06, 1.06, 1.06, 1.06, 1.06, 0.85, 0.85]
    tprof_hour[0] = [0.79, 0.72, 0.72, 0.71, 0.74, 0.80, 0.92, 1.08, 1.19, 1.22, 1.21, 1.21, 
                     1.17, 1.15, 1.14, 1.13, 1.10, 1.07, 1.04, 1.02, 1.02, 1.01, 0.96, 0.88]

    # SNAP 2 - Residential, commercial and other combustion
    tprof_mnth[1] = [1.70, 1.50, 1.30, 1.00, 0.70, 0.40, 0.20, 0.40, 0.70, 1.05, 1.40, 1.65]
    tprof_week[1] = [1.08, 1.08, 1.08, 1.08, 1.08, 0.8, 0.8]
    tprof_hour[1] = [0.38, 0.36, 0.36, 0.36, 0.37, 0.50, 1.19, 1.53, 1.57, 1.56, 1.35, 1.16,
                     1.07, 1.06, 1.00, 0.98, 0.99, 1.12, 1.41, 1.52, 1.39, 1.35, 1.00, 0.42]

    # SNAP 3 - Industrial combustion
    tprof_mnth[2] = [1.10, 1.08, 1.05, 1.00, 0.95, 0.90, 0.93, 0.95, 0.97, 1.00, 1.02, 1.05]
    tprof_week[2] = [1.08, 1.08, 1.08, 1.08, 1.08, 0.8, 0.8]
    tprof_hour[2] = [0.75, 0.75, 0.78, 0.82, 0.88, 0.95, 1.02, 1.09, 1.16, 1.22, 1.28, 1.30,
                     1.22, 1.24, 1.25, 1.16, 1.08, 1.01, 0.95, 0.90, 0.85, 0.81, 0.78, 0.75]

    # SNAP 4 - Industrial processes
    tprof_mnth[3] = [1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.00, 0.84, 1.02, 1.02, 1.02, 0.90]
    tprof_week[3] = [1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.00]
    tprof_hour[3] = 24*[1.]

    # SNAP 5 - Extraction & distribution of fossil fuels
    tprof_mnth[4] = [1.20, 1.20, 1.20, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 1.20, 1.20, 1.20]
    tprof_week[4] =  7*[1.]
    tprof_hour[4] = 24*[1.]

    # SNAP 6 - Solvent use
    tprof_mnth[5] = [0.95, 0.96, 1.02, 1.00, 1.01, 1.03, 1.03, 1.01, 1.04, 1.03, 1.01, 0.91]
    tprof_week[5] = [1.2, 1.2, 1.2, 1.2, 1.2, 0.5, 0.5]
    tprof_hour[5] = [0.50, 0.35, 0.20, 0.10, 0.10, 0.20, 0.75, 1.25, 1.40, 1.50, 1.50, 1.50,
                     1.50, 1.50, 1.50, 1.50, 1.50, 1.40, 1.25, 1.10, 1.00, 0.90, 0.80, 0.70]

    # SNAP 7 - Road transport
    tprof_mnth[6] = [0.88, 0.92, 0.98, 1.03, 1.05, 1.06, 1.01, 1.02, 1.06, 1.05, 1.01, 0.93]
    tprof_week[6] = [1.02, 1.06, 1.08, 1.10, 1.14, 0.81, 0.79]
    tprof_hour[6] = [0.19, 0.09, 0.06, 0.05, 0.09, 0.22, 0.86, 1.84, 1.86, 1.41, 1.24, 1.20,
                     1.32, 1.44, 1.45, 1.59, 2.03, 2.08, 1.51, 1.06, 0.74, 0.62, 0.61, 0.44]

    # SNAP 8 - Other mobile sources and machinery
    tprof_mnth[7] = [0.88, 0.92, 0.98, 1.03, 1.05, 1.06, 1.01, 1.02, 1.06, 1.05, 1.01, 0.93]
    tprof_week[7] =  7*[1.]
    tprof_hour[7] = [0.19, 0.09, 0.06, 0.05, 0.09, 0.22, 0.86, 1.84, 1.86, 1.41, 1.24, 1.20,
                     1.32, 1.44, 1.45, 1.59, 2.03, 2.08, 1.51, 1.06, 0.74, 0.62, 0.61, 0.44]

    # SNAP 9 - Waste treatment and disposal
    tprof_mnth[8] = 12*[1.]
    tprof_week[8] =  7*[1.]
    tprof_hour[8] = 24*[1.]

    # SNAP 10 - Agriculture
    tprof_mnth[9] = [0.45, 1.30, 2.35, 1.70, 0.85, 0.85, 0.85, 1.00, 1.10, 0.65, 0.45, 0.45]
    tprof_week[9] =  7*[1.]
    tprof_hour[9] = 24*[1.]
    
    return tprof_hour, tprof_week, tprof_mnth

def checkbounds(domainbounds, x, y, z, show_log=False):
    
    import numpy as np

    xminidx, xmaxidx, yminidx, ymaxidx, zminidx, zmaxidx = np.nan, np.nan, np.nan, np.nan, np.nan, np.nan

    # Check domain bounds
    # --- XMIN ------------------------------------------------------------------------------------------------
    do_proceed = True
    if domainbounds['xmin'] >= np.min(x):
        xminidx = np.argmax(x >= domainbounds['xmin'])
    else:
        do_proceed = False
        print("Requested lower bound x too low, request:", domainbounds['xmin'], "source file min:", np.min(x))
    
    # --- XMAX ------------------------------------------------------------------------------------------------
    if domainbounds['xmax'] <= np.max(x):
        xmaxidx = np.argmax(x >= domainbounds['xmax'])
    else:
        do_proceed = False
        print("Requested upper bound x too high, request:", domainbounds['xmax'], "source file max:", np.max(x))
    
    # --- YMIN ------------------------------------------------------------------------------------------------
    if domainbounds['ymin'] >= np.min(y):
        yminidx = np.argmax(y >= domainbounds['ymin'])
    else:
        do_proceed = False
        print("Requested lower bound y too low, request:", domainbounds['ymin'], "source file min:", np.min(y))

    # --- YMAX ------------------------------------------------------------------------------------------------
    if domainbounds['ymax'] <= np.max(y):
        ymaxidx = np.argmax(y >= domainbounds['ymax'])
    else:
        do_proceed = False
        print("Requested upper bound y too high, request:", domainbounds['ymax'], "source file max:", np.max(y))
    
    if z is not None:
        # --- ZMIN --------------------------------------------------------------------------------------------
        # Since this is about altitude, it does not make sense to check minimum, 
        # because we always work from the ground up. Hence, don't stop execution here in any way.' 
        zminidx = np.argmax(z >= domainbounds['zmin'])
        
        # --- ZMAX --------------------------------------------------------------------------------------------
        if domainbounds['zmax'] <= np.max(z):
            zmaxidx = np.argmax(z >= domainbounds['zmax'])
        else:
            do_proceed = False
            print("Requested upper bound z too high, request:", domainbounds['zmax'], "source file max:", np.max(z))
    else:
        zminidx = -999
        zmaxidx = -999
        
    if show_log: print( 'Checkbounds:', xminidx, xmaxidx, yminidx, ymaxidx, zminidx, zmaxidx )   
    return do_proceed, int(xminidx), int(xmaxidx), int(yminidx), int(ymaxidx), int(zminidx), int(zmaxidx)

def writereademission_3d(domainbounds, tstart, tend, tracers, sources, categos, show_log=False):
    import numpy as np
    import netCDF4 as netc
    import os
    from datetime import datetime
    from datetime import timedelta

    """
    Read tracer sources of all categories, apply temporal profile and combine in 1 new file per tracer.

    Source files have to be in same directory and have to following form:
    <tracer>_<year>_<category>.nc
    In-file variables should be at least: 
    x-coordinates          (rank 1, size X) 
    y-coordinates          (rank 1, size Y)
    z-coordinates          (rank 1, size Z)
    tracer yearly emission (rank 3, size X . Y . Z) e.g. "co2", "ch4"

    TODO: Set in-file tracer name to lowercase, is UPPERCASE now.
    """

    tstep = tstart
    dt = timedelta(hours=1)
    do_proceed = True
    hourly_emis = np.zeros([10, 10])  # dummy

    tprof_hour, tprof_week, tprof_mnth = loadsnap()

    while tstep <= tend and do_proceed:

        efs = tprof_mnth[:, tstep.month - 1] * tprof_week[:, tstep.weekday()] * tprof_hour[:, tstep.hour]

        for itrac, tracer in enumerate(tracers):

            # Reset for new tracer
            hourly_emis[:] = 0

            tfname = "{}_emis_{}_3d.nc".format(tracer, tstep.strftime("%Y%m%d%H%M"))
            if show_log:
                print("Target file: ", tfname)

            # -- Loop over source categories
            for isrc, sourcename in enumerate(sources[itrac]):

                icat = int(categos[itrac][isrc])

                # -- Read field
                sfname = "{}_{}_{}.nc".format(tracer, str(tstep.year), sourcename)
                if show_log:
                    print("Adding source: {:30s} (SNAP {:02d})".format(sfname, icat))

                if os.path.isfile(sfname):
                    sfobj = netc.Dataset(sfname, 'r')
                    rank = len(sfobj.variables[tracer.upper()].shape)
                    
                    x = sfobj.variables['x'][:]
                    y = sfobj.variables['y'][:]
                    
                    #NEW
                    if  rank == 3: 
                        z = sfobj.variables['z'][:]
                        do_proceed, xminidx, xmaxidx, yminidx, ymaxidx, zminidx, zmaxidx = checkbounds(domainbounds, x, y, z, show_log=show_log)
                    else: 
                        do_proceed, xminidx, xmaxidx, yminidx, ymaxidx, _,       _       = checkbounds(domainbounds, x, y, None, show_log=show_log)
                   
                    nx = xmaxidx - xminidx + 1
                    ny = ymaxidx - yminidx + 1
                    
                    if nx == len(x): 
                        sx = np.s_[:]
                    else:
                        sx = np.s_[xminidx:xmaxidx+1]
                            
                    if ny == len(y): 
                        sy = np.s_[:]
                    else:
                        sy = np.s_[yminidx:ymaxidx+1]    
                            
                    #NEW
                    
                    if rank == 3:
                    
                        nz = zmaxidx - zminidx + 1
                        
                        if nz == len(z): 
                            sz = np.s_[:]
                        else:
                            sz = np.s_[zminidx:zmaxidx+1]        
                            
                        if (itrac + isrc) == 0:
                            hourly_emis = np.zeros([nz, ny, nx])
                            
                        if show_log:
                            print(f"Field dimensions:        ({nz}, {ny}, {nx})")
                            print(f"Source file dimensions:  {sfobj.variables[tracer.upper()][sz, sy, sx].shape}")
                            print(f"Target array dimensions: {hourly_emis.shape}")

                        hourly_emis += sfobj.variables[tracer.upper()][sz, sy, sx] * efs[icat - 1] / (365 * 24)
                        
                    elif rank == 2:
  
                        if (itrac + isrc) == 0:
                            print("ERROR: Initializing with 2D! Reconsider category order!")
                            break

                        hourly_emis[0] += sfobj.variables[tracer.upper()][sx, sy].T * efs[icat - 1] / (365 * 24)    
                        
                    sfobj.close()
                else:
                    do_proceed = False
                    print("File does not exist:", sfname)

            if do_proceed:
                # --- Create netCDF file
                tfobj = netc.Dataset(tfname, 'w')


                t0 = tstep.strftime("%Y-%m-%d %H:%M")
                t1 = (tstep + dt).strftime("%H:%M")
                dx = int(x[1]-x[0])
                dy = int(y[1]-y[0])
                
                # --- Global attributes
                tfobj.title = f"{dx}x{dy}m {tracer.upper()} hourly emissions map for {t0}-{t1}"
                tfobj.history = "Created: " + datetime.now().strftime("%d %b %Y")

                tfobj.description = f"Total {tracer.upper()} emission from categories {sources}"
                tfobj.valid = "Valid from " + tstep.strftime("%Y-%m-%d %H:%M") + ' to ' + (tstep + dt).strftime(
                    "%Y-%m-%d %H:%M")
                tfobj.author = 'M. de Bruine (VU)'
                tfobj.email = 'm.de.bruine@vu.nl'

                # -- Declaration of dimensions and variables
                dim_x = tfobj.createDimension('x', nx)
                dim_y = tfobj.createDimension('y', ny)
                dim_z = tfobj.createDimension('z', nz)

                var_x = tfobj.createVariable('x', 'f4', ('x',))
                var_y = tfobj.createVariable('y', 'f4', ('y',))
                var_z = tfobj.createVariable('z', 'f4', ('z',))
                var_e = tfobj.createVariable(tracer.lower(), 'f8', ('z', 'y', 'x',))

                # -- Assigning values to variables
                var_x[:] = x[sx]
                var_y[:] = y[sy]
                var_z[:] = z[sz]
                var_e[:, :, :] = hourly_emis

                # -- Variable attributes
                var_x.units = 'Rijksdriehoekcoordinaat x in meters'
                var_y.units = 'Rijksdriehoekcoordinaat y in meters'
                var_z.units = 'Hoogte z in meters (middelpunt gridbox)'
                var_e.units = 'Kilogram ' + tracer.lower() + ' per hour (kg hour-1)'

                tfobj.close()

            tstep += dt