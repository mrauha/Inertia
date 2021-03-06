import numpy as np

def parallel_axis(Ic, m, d):
    '''Returns the moment of inertia of a body about a different point.

    Parameters
    ----------
    Ic : ndarray, shape(3,3)
        The moment of inertia about the center of mass of the body with respect
        to an orthogonal coordinate system.
    m : float
        The mass of the body.
    d : ndarray, shape(3,)
        The distances along the three ordinates that located the new point
        relative to the center of mass of the body.

    Returns
    -------
    I : ndarray, shape(3,3)
        The moment of inertia about of the body about a point located by d.

    '''
    a = d[0]
    b = d[1]
    c = d[2]
    dMat = np.zeros((3, 3), dtype=object)
    dMat[0] = np.array([b**2 + c**2, -a * b, -a * c])
    dMat[1] = np.array([-a * b, c**2 + a**2, -b * c])
    dMat[2] = np.array([-a * c, -b * c, a**2 + b**2])
    return Ic + m * dMat

def inertia_components(jay, beta):
    '''Returns the 2D orthogonal inertia tensor.

    When at least three moments of inertia and their axes orientations are
    known relative to a common inertial frame of a planar object, the orthoganl
    moments of inertia relative the frame are computed.

    Parameters
    ----------
    jay : ndarray, shape(n,)
        An array of at least three moments of inertia. (n >= 3)
    beta : ndarray, shape(n,)
        An array of orientation angles corresponding to the moments of inertia
        in jay.

    Returns
    -------
    eye : ndarray, shape(3,)
        Ixx, Ixz, Izz

    '''
    sb = np.sin(beta)
    cb = np.cos(beta)
    betaMat = np.matrix(np.vstack((cb**2, -2 * sb * cb, sb**2)).T)
    eye = np.squeeze(np.asarray(np.dot(betaMat.I, jay)))
    return eye

def tube_inertia(l, m, ro, ri):
    '''Calculate the moment of inertia for a tube (or rod) where the x axis is
    aligned with the tube's axis.

    Parameters
    ----------
    l : float
        The length of the tube.
    m : float
        The mass of the tube.
    ro : float
        The outer radius of the tube.
    ri : float
        The inner radius of the tube. Set this to zero if it is a rod instead
        of a tube.

    Returns
    -------
    Ix : float
        Moment of inertia about tube axis.
    Iy, Iz : float
        Moment of inertia about normal axis.

    '''
    Ix = m / 2. * (ro**2 + ri**2)
    Iy = m / 12. * (3 * ro**2 + 3 * ri**2 + l**2)
    Iz = Iy
    return Ix, Iy, Iz
    
def cylinder_inertia(l, m, ro, ri):
    '''Calculate the moment of inertia for a hollow cylinder (or solid cylinder) where the x axis is
    aligned with the cylinder's axis.

    Parameters
    ----------
    l : float
        The length of the cylinder.
    m : float
        The mass of the cylinder.
    ro : float
        The outer radius of the cylinder.
    ri : float
        The inner radius of the cylinder. Set this to zero for a solid cylinder.

    Returns
    -------
    Ix : float
        Moment of inertia about cylinder axis.
    Iy, Iz : float
        Moment of inertia about cylinder axis.

    '''
    Ix = m / 2. * (ro**2 + ri**2)
    Iy = m / 12. * (3 * ro**2 + 3 * ri**2 + l**2)
    Iz = Iy
    return Ix, Iy, Iz

def total_com(coordinates, masses):
    '''Returns the center of mass of a group of objects if the indivdual
    centers of mass and mass is provided.

    coordinates : ndarray, shape(3,n)
        The rows are the x, y and z coordinates, respectively and the columns
        are for each object.
    masses : ndarray, shape(3,)
        An array of the masses of multiple objects, the order should correspond
        to the columns of coordinates.

    Returns
    -------
    mT : float
        Total mass of the objects.
    cT : ndarray, shape(3,)
        The x, y, and z coordinates of the total center of mass.

    '''
    products = masses * coordinates
    mT = np.sum(masses)
    cT = np.sum(products, axis=1) / mT
    return mT, cT

def rotate_inertia_tensor(I, angle):
    '''Returns inertia tensor rotated through angle. Only for 2D'''
    ca = np.cos(angle)
    sa = np.sin(angle)
    C    =  np.array([[ca, 0., -sa],
                      [0., 1., 0.],
                      [sa, 0., ca]])
    Irot =  np.dot(C, np.dot(I, C.T))
    return Irot


# unit vector; useful for locating segments
xunit = np.array([[1],[0],[0]])
yunit = np.array([[0],[1],[0]])
zunit = np.array([[0],[0],[1]])

def rotate3(angles):
    '''Produces a three-dimensional rotation matrix as rotations around the 
    three cartesian axes.
    
    Parameters
    ----------
    angles : numpy.array or list or tuple, shape(3,)
        Three angles (in units of radians) that specify the orientation of
        a new reference frame with respect to a fixed reference frame. 
        The first angle is a pure rotation about the x-axis, the second about
        the y-axis, and the third about the z-axis. All rotations are with 
        respect to the initial fixed frame, and they occur in the order x,
        then y, then z.
        
    Returns
    -------
    R : numpy.matrix, shape(3,3)
        Three dimensional rotation matrix about three different orthogonal axes.
    '''
    cx = np.cos(angles[0])
    sx = np.sin(angles[0])

    cy = np.cos(angles[1])
    sy = np.sin(angles[1])

    cz = np.cos(angles[2])
    sz = np.sin(angles[2])

    Rz = np.mat([[ cz,-sz,  0],
                 [ sz, cz,  0],
                 [  0,  0,  1]])
    
    Ry = np.mat([[ cy,  0, sy],
                 [  0,  1,  0],
                 [-sy,  0, cy]])

    Rx = np.mat([[  1,  0,  0],
                 [  0, cx, -sx],
                 [  0, sx,  cx]])

    return Rz*Ry*Rx
    
def rotate3_rel(angles):
    '''The three-dimensional relative rotation matrix from Yeadon 1989-i used
    to describe the orientation of a human with respect to a fixed frame.
    
    Parameters
    ----------
    angles : numpy.array or list or tuple, shape(3,)
        Three angles (in units of radians) that specify the orientation of a
        new reference frame with respect to a fixed reference frame. The first
        angle, phi, is a rotation about the fixed frame's x-axis. The second
        angle, theta, is a rotation about the new y-axis (which is realized 
        after the phi rotation). The third angle, psi, is a rotation about the
        new z-axis (which is realized after the theta rotation). Thus, all 
        three angles are "relative" rotations with respect to the new frame. 
        Note: if the rotations are viewed as occuring in the opposite direction
        (z, then y, then x), all three rotations are with respect to the
        initial fixed frame rather than "relative".
        
    Returns
    -------
    R : numpy.matrix, shape(3,3)
        Three dimensional rotation matrix about three different orthogonal axes.
    '''
    cphi = np.cos(angles[0])
    sphi= np.sin(angles[0])

    cthe = np.cos(angles[1])
    sthe = np.sin(angles[1])

    cpsi = np.cos(angles[2])
    spsi = np.sin(angles[2])
    
    R1 = np.mat([[     1,     0,     0],
                 [     0,  cphi, -sphi],
                 [     0,  sphi,  cphi]])
    
    R2 = np.mat([[  cthe,     0,  sthe],
                 [     0,     1,     0],
                 [ -sthe,     0,  cthe]])

    R3 = np.mat([[  cpsi,  -spsi,     0],
                 [  spsi,  cpsi,     0],
                 [     0,     0,     1]])
                 
    return R1*R2*R3

def rotate3_inertia(RotMat,relInertia):
    '''Rotates an inertia tensor. A derivation of the formula in this function
    can be found in Crandall 1968, Dynamics of mechanical and electromechanical
    systems. This function only transforms an inertia tensor for rotations with
    respect to a fixed point. To translate an inertia tensor, one must use the
    parallel axis analogue for tensors. An inertia tensor contains both moments
    of inertia and products of inertia for a mass in a cartesian (xyz) frame.
    
    Parameters
    ----------
    RotMat : numpy.matrix, shape(3,3)
        Three-dimensional rotation matrix specifying the coordinate frame that
        the input inertia tensor is in, with respect to a fixed coordinate
        system in which one desires to express the inertia tensor.
    relInertia : numpy.matrix, shape(3,3)
        Three-dimensional cartesian inertia tensor describing the inertia of a
        mass in a rotated coordinate frame.
                 
    Returns
    -------
    Inertia : numpy.matrix, shape(3,3) 
        Inertia tensor with respect to a fixed coordinate system ("unrotated").

    '''
    return RotMat * relInertia * RotMat.T
