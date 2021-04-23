#mcandrew

def interpolateDensity(xs,dens):
    from scipy.interpolate import UnivariateSpline as spline
    return spline(xs,dens)

def ecdf(xs,dens,time=False):
    from scipy.integrate import simpson
    from scipy.interpolate import UnivariateSpline as spline
    
    mn,mx = min(xs), max(xs)
    if time:
        xs = (xs-mn)/(mx-mn)
 
    cdf = []
    if time:
        areaUnderCurve = spline(xs,dens).integral(0,1)
    else:
        areaUnderCurve = spline(xs,dens).integral(mn,mx)
    for i in range(len(xs)):
        x,den = xs[:i], dens[:i]
        cdf.append( simpson(den,x)/ areaUnderCurve )
    return cdf

def qcdf(xs,dens,x,time=False):
    from scipy.integrate import simpson
    from scipy.interpolate import UnivariateSpline as spline

    mn,mx = min(xs), max(xs)
    if time:
        xs = (xs-mn)/(mx-mn)
        x = (x-mn)/(mx-mn)
    if time:
        areaUnderCurve = spline(xs,dens).integral(0,1)
    else:
        areaUnderCurve = spline(xs,dens).integral(mn,mx)
    F = spline(xs,dens).integral(0,x)
    
    return F/areaUnderCurve

def quantile(xs,cdfs,qs):
    import numpy as np
    from scipy.interpolate import PchipInterpolator as spline
    from scipy.optimize import root

    cdfs = np.array(cdfs)
    f = spline(xs,cdfs)

    quantiles = {}
    for q in qs:
        findRoot = root(lambda x: f(x)-q, x0 = xs[np.argmin(abs(cdfs-q))] )
        rootValue = float(findRoot.x)

        quantiles[q] = rootValue
    return quantiles

def compMean(xs,dens,time=False):
    from scipy.interpolate import UnivariateSpline as spline
       
    mn,mx = min(xs), max(xs)
    if time:
        xs = (xs-mn)/(mx-mn)

    if time:
        avg = spline(xs,xs*dens).integral(0,1)
        return avg*(mx-mn) + mn
    else:
        avg = spline(xs,xs*dens).integral(mn,mx)/(mx-mn)
        return avg
