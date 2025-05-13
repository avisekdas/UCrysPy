import header

def get_posi_orien_local_frame_func(R, positions, orientations):
    # matrix format
    selected_particles_orientations = []
    for i in range(len(orientations)):
        mat_form = header.rowan.to_matrix(header.np.array(orientations[i]), require_unit=False)
        mat = header.np.matmul(header.np.linalg.inv(R), mat_form)
        selected_particles_orientations.append(header.rowan.from_matrix(mat, require_orthogonal=False))

    # First coordinate shift to the particle's local position then you rotate it with the rotation matrix
    positions_in_original_frame = header.np.array([positions[i] for i in range(len(positions))])
    selected_particles_positions = positions_in_original_frame[:]
    # Now rotate the particles in the UC local frame
    positions_in_rotated_frame = []
    for i in range(len(selected_particles_positions)):
        positions_in_rotated_frame.append(header.np.matmul(header.np.linalg.inv(R), header.np.array(selected_particles_positions[i])))
    selected_particles_positions = positions_in_rotated_frame[:]
    #******************************************************
    # Quaternion format
    '''selected_particles_orientations = [header.rowan.normalize(header.rowan.multiply(header.rowan.inverse(q), orientations[t])) for t in particle_arr]
    positions_in_original_frame = header.np.array([positions[particle_arr[i]] for i in range(len(particle_arr))])
    positions_wrt_ref_particle = header.np.array([box_arr.wrap(positions_in_original_frame[i] - positions_in_original_frame[0]) for i in range(len(positions_in_original_frame))])
    # With respect to center
    center_in_local_frame = (header.np.average(positions_wrt_ref_particle, axis=0))
    # Selected particles' positions in shifted coordinate
    selected_particles_positions = header.np.array([box_arr.wrap(positions_wrt_ref_particle[i]-center_in_local_frame) for i in range(len(positions_wrt_ref_particle))])

    # Now rotate the particles in the UC local frame
    selected_particles_positions = [(header.rowan.rotate(header.rowan.inverse(q), selected_particles_positions[i])) for i in range(len(selected_particles_positions))]
    '''

    return selected_particles_positions, selected_particles_orientations