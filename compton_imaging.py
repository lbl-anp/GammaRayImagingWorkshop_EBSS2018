import numpy as np
import numpy.testing as npt
from tqdm import tqdm

class ComptonBackprojection2D(object):
    """
    Class for handling 2D backprojection of Compton cones.
    """
    def __init__(self, imspace_discr_size=1, intersection_kernel_width=0.5):
        """
        Agent for computing 2D backprojection of Compton cones based on 
        far-field approximation.

        Parameters
        ----------
        imspace_discr_size : float, optional, default = 1
            Size of angular bins to use when creating an angular imaging space,
            in degrees. Default is 1 degree. 
            WARNING: reducing binsize greatly increases memory usage and 
            backprojection computation time!

        intersection_kernel_width : float, default = 0.5
            Width of the overlap function for determining cone surface 
            intersection with the image space. Value should be specified in
            degrees.
        """
        self.ang_binsize = imspace_discr_size
        self.intersection_sd = intersection_kernel_width
        self._create_imaging_space_and_initialize_image()
        self._num_cones_in_image = 0

    def _create_imaging_space_and_initialize_image(self):
        """
        Discretize the unit sphere (4-pi) according to self.ang_binsize.

        Internal method intended for use in constructor.
        """
        # Range of bin centers in angular space, in radians
        phi_range = np.linspace(0, 360, int(360/self.ang_binsize)+1)
        th_range = np.linspace(0, 180, int(180/self.ang_binsize)+1)
        # Convert to radians
        phi_range *= (np.pi / 180)
        th_range *= (np.pi / 180)
        # 2D array of angular space according to above binning scheme
        phi, th = np.meshgrid(phi_range, th_range)
        self.img_shape = phi.shape
        # Convert angular imaging space to unit vectors
        imx = np.sin(th) * np.cos(phi)
        imy = np.sin(th) * np.sin(phi)
        imz = np.cos(th)
        imspace = np.array([imx.ravel(), imy.ravel(), imz.ravel()]).T
        # Verify normalization
        try : npt.assert_almost_equal( np.sqrt(np.sum(imspace**2, axis=1)),
                                       np.ones_like(imx).ravel() )
        except AssertionError:
            raise ValueError('imspace normalization failure!')
        # Re-orient imaging space: align with simulation coord system and 
        # rotate crappy sampling effects to the poles.
        # NOTE: Not super rigorous here, true orientation might be off by 
        # several rotations/reflections... doesn't matter for case when point
        # source in forward direction (i.e. [phi, th] = [0, 0]).
        imspace_transform = np.array([[0, 0, 1],
                                      [1, 0, 0],
                                      [0, 1, 0]])
        imspace = np.dot(imspace, imspace_transform)
        # Set image space to object
        self.imspace = imspace
        # Create a container for the image data
        self.clear_image()

    @property
    def extent(self):
        """
        Angular extent of imaging space: [phi_min, phi_max, th_min, th_max]

        WARNING: HARD-CODED - needs modification if image space bounds or
        transformation is modified!
        """
        return [-180, 180, -90, 90]

    def clear_image(self):
        self.img_data = np.zeros(self.imspace.shape[0])

    def intersection_operator(self, angular_distance, sd):
        """
        Kernel for computing intersection of cone with discretized imaging
        space.

        Converts 'angular distance' to surface of cone into a backprojection
        value based on Gaussian overlap.
        """
        return np.exp(-(angular_distance)**2 / (2*sd**2))

    def backproject_cones(self, cone_axes, cone_angles):
        """
        Compute intersection of Compton cones with the imaging space.

        Parameters
        ----------
        cone_axes : array of unit vectors with shape N x 3
            The scatter-axes of N number of Compton cones. Must be input as
            array with shape N x 3 where N is the number of events and the 
            columns are the x, y, and z components of the unit vector 
            specifying the direction of the cone axis.
            Note that these MUST be unit vectors!

        cone_angles : array of angles with shape N, in degrees
            Cone opening angle as computed from Compton equation.
            Values should be given in DEGREES, and must be in the range 
            [0, 180].
        """
        # Default behavior: clear image for each new call
        self.clear_image()
        # Handle single cone
        if cone_axes.ndim < 2:
            cone_axes = np.array(cone_axes, ndmin=2)
            cone_angles = np.array(cone_angles, ndmin=1)
        for cax, can in tqdm(zip(cone_axes, cone_angles)):
            # Angular difference between cone axis and imaging space
            ang_diff = np.arccos(np.dot(self.imspace, cax)) * (180 / np.pi)
            # Handle precision issues
            ang_diff[~np.isfinite(ang_diff)] = 0
            # Compute cone intersection
            cone_intersection = self.intersection_operator(np.abs(ang_diff - can), 
                                                           self.intersection_sd)
            # Accumulate result
            self.img_data += cone_intersection
            self._num_cones_in_image += 1
        return self.img_data.reshape(self.img_shape)

if __name__ == "__main__":
    import os
    import tables
    import matplotlib.pyplot as plt
    from event_processing import compute_cone_opening_angle, \
                                 compute_cone_scatter_axes

    # Load data
    with tables.open_file('hits.h5', 'r') as hf:
        ptrs, lens = hf.root.EventPointers.read(), hf.root.EventLengths.read()
        idata = hf.root.InteractionData.read()

    # Focus only on double-interaction, photopeak events
    double_interaction_mask = lens == 2
    p2, l2 = ptrs[double_interaction_mask], lens[double_interaction_mask]
    evs = np.array([idata[p:p+l] for p, l in zip(p2, l2)])
    ppk_mask = (evs['energy'].sum(axis=1) > 660)
    ppk_evs = evs[ppk_mask]

    # Convert events to cone data
    cone_axes = compute_cone_scatter_axes(ppk_evs)
    cone_angles = compute_cone_opening_angle(661.657, ppk_evs['energy'][:,0])

    # Test initialization of backprojector
    backprojector = ComptonBackprojection2D()
    print "Shape of image space: %s" %(backprojector.imspace.shape,)
    print "Shape of image: %s" %(backprojector.img_shape,)
    print "Image data array dims: %s" %(backprojector.img_data.shape,)

    # Test backprojection
    num_events = 1000
    img = backprojector.backproject_cones(cone_axes[:num_events, :], 
                                          cone_angles[:num_events])
    plt.imshow(img, extent=[-180, 180, -90, 90],  interpolation="none");
    plt.title('Compton backprojection\n%s events with $\sigma$ = %.2f deg' 
              %(num_events, backprojector.intersection_sd))
    plt.colorbar();
    plt.show()
