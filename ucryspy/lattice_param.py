import header

def lattice_param_func(array):
    Lx, Ly, Lz = header.np.linalg.norm(array[0]), header.np.linalg.norm(array[1]), header.np.linalg.norm(array[2])
    if Lx != 0 and Ly != 0 and Lz != 0:
        alpha = header.np.rad2deg(header.np.arccos(round(header.np.dot(array[2]/header.np.linalg.norm(array[2]), array[1]/header.np.linalg.norm(array[1])), 4)))
        beta = header.np.rad2deg(header.np.arccos(round(header.np.dot(array[0]/header.np.linalg.norm(array[0]), array[2]/header.np.linalg.norm(array[2])), 4)))
        gamma = header.np.rad2deg(header.np.arccos(round(header.np.dot(array[0]/header.np.linalg.norm(array[0]), array[1]/header.np.linalg.norm(array[1])), 4)))
        return [Lx, Ly, Lz, alpha, beta, gamma]
    else:
        return []

def lattice_param_func_hoomd(v):
    Lx = header.np.sqrt(header.np.dot(v[0], v[0]))
    a2x = header.np.dot(v[0], v[1]) / Lx
    st1 = header.np.dot(v[1],v[1]) - a2x*a2x
    if st1 > 0:
        Ly = header.np.sqrt(st1)
        if Ly != 0 and Lx != 0:
            xy = a2x / Ly
            v0xv1 = header.np.cross(v[0], v[1])
            st2 = header.np.dot(v0xv1, v0xv1)
            if st2 > 0:
                v0xv1mag = header.np.sqrt(st2)
                Lz = abs(header.np.dot(v[2], v0xv1) / v0xv1mag)
                if Lz != 0:
                    a3x = header.np.dot(v[0], v[2]) / Lx
                    xz = a3x / Lz
                    yz = (header.np.dot(v[1],v[2]) - a2x*a3x) / (Ly*Lz)

                    box = header.freud.box.Box(Lx=Lx, Ly=Ly, Lz=Lz,
                                                        xy=xy, xz=xz, yz=yz, is2D=False)
                    volume = box.volume
                    gamma = header.np.rad2deg(header.np.arccos(round(xy/header.np.sqrt(1+xy*xy), 4)))
                    beta = header.np.rad2deg(header.np.arccos(round(xz/header.np.sqrt(1+xz*xz+yz*yz), 4)))
                    alpha = header.np.rad2deg(header.np.arccos(round((xy*xz+yz)/(header.np.sqrt(1+xy*xy)*header.np.sqrt(1+xz*xz+yz*yz)), 4)))

                    return [Lx, Ly, Lz, alpha, beta, gamma, xy, xz, yz, volume]
                else:
                    return [0, 0, 0, 0, 0, 0, 0, 0, 0]
            else:
                return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    else:
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
