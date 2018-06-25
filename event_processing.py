import numpy as np

# Constants
m_e = 511.  # Electron restmass, keV

def compute_cone_opening_angle(E_0, E_dep):
    """
    Compute cone opening angle from Compton kinematics.

    Parameters
    ----------
    E_0   : float
        Initial energy of incident gamma-rays, in keV
    E_dep : array_like, float
        Energy deposited in first Compton scatter interaction, in keV

    Returns
    -------
    angle : array_like, float
        Compton scatter angle in degrees
    """
    A0 = E_0 / m_e
    Ad = (E_0 - E_dep) / m_e
    mu = 1 + (1 / A0) - (1 / Ad)
    return np.arccos(mu) * (180/np.pi)

def compute_cone_scatter_axes(events):
    """
    Convert interaction positions to normalized cone scatter axes.

    Parameters
    ----------
    events : array_like, dtype = interaction_data_type
        An N x M array where N is the number of events and M is the length of
        each event (e.g., for double-interaction events, M = 2).
        The dtype of this array must be the same as that from the HDF5 archive;
        in particular, it must have 'x', 'y', and 'z' fields for the 3D 
        interaction position.
        Events are assumed to be time-sequenced.

    Returns
    -------
    cone_axes : array_like, N x 3
        An array of cone axes where N is the number of input events.
    """
    xd = events['x'][:,0] - events['x'][:,1]
    yd = events['y'][:,0] - events['y'][:,1]
    zd = events['z'][:,0] - events['z'][:,1]
    return (np.array([xd, yd, zd]) / np.sqrt(xd**2 + yd**2 + zd**2)).T
