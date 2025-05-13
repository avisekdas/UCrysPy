import header

def make_xyz_func(vertices):
    output_file = 'test' + '.xyz'
    f = open(output_file, 'w')
    f.write(str(len(vertices)) + "\n")
    f.write("ABC" + "\n")
    for i in range(len(vertices)):
        f.write("C"  + " " + str(vertices[i][0]) + " " + str(vertices[i][1]) + " " + str(vertices[i][2]) + "\n")
    f.close()
