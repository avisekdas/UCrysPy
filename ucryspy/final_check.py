# For a particular triplet, it finds the proper crystal class within two tolerances
# Returns the type of the class satisfied by the triplet

import header

def final_check_func(self):
    p = 'NONE'
    a, b, c, alpha, beta, gamma = self.lv[0], self.lv[1], self.lv[2], self.lv[3], self.lv[4], self.lv[5]
    # print(a, b, c, alpha, beta, gamma)
    if self.ty == 'CUBIC':
        if abs(a-b) <= self.dist_cutoff and abs(a-c) <= self.dist_cutoff and abs(b-c) <= self.dist_cutoff and abs(alpha-beta) <= self.angle_cutoff and abs(alpha-gamma) <= self.angle_cutoff and abs(gamma-beta) <= self.angle_cutoff and (90-self.angle_cutoff) < alpha <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < beta <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < gamma <= (90+self.angle_cutoff):
            p = 'CUBIC'
        else:
            p = 'NONE'

    elif self.ty == 'TETRAGONAL':
        if abs(a-b) <= self.dist_cutoff and abs(a-c) > self.dist_cutoff and abs(b-c) > self.dist_cutoff and abs(alpha-beta) <= self.angle_cutoff and abs(alpha-gamma) <= self.angle_cutoff and abs(gamma-beta) <= self.angle_cutoff and (90-self.angle_cutoff) < alpha <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < beta <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < gamma <= (90+self.angle_cutoff): 
            p = 'TETRAGONAL'   
        elif abs(c-b) <= self.dist_cutoff and abs(a-c) > self.dist_cutoff and abs(b-a) > self.dist_cutoff and abs(alpha-beta) <= self.angle_cutoff and abs(alpha-gamma) <= self.angle_cutoff and abs(gamma-beta) <= self.angle_cutoff and (90-self.angle_cutoff) < alpha <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < beta <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < gamma <= (90+self.angle_cutoff):
            p = 'TETRAGONAL'   
        elif abs(a-c) <= self.dist_cutoff and abs(a-b) > self.dist_cutoff and abs(b-c) > self.dist_cutoff and abs(alpha-beta) <= self.angle_cutoff and abs(alpha-gamma) <= self.angle_cutoff and abs(gamma-beta) <= self.angle_cutoff and (90-self.angle_cutoff) < alpha <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < beta <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < gamma <= (90+self.angle_cutoff): 
            p = 'TETRAGONAL'
        else:
            p = 'NONE'

    elif self.ty == 'RHOMBOHEDRAL':
        if abs(a-b) <= self.dist_cutoff and abs(a-c) <= self.dist_cutoff and abs(b-c) <= self.dist_cutoff and abs(alpha-beta) <= self.angle_cutoff and abs(alpha-gamma) <= self.angle_cutoff and abs(gamma-beta) <= self.angle_cutoff:
            count = 0
            if alpha < (90-self.angle_cutoff) or alpha >= (90+self.angle_cutoff):
                count = count + 1
            elif beta < (90-self.angle_cutoff) or beta >= (90+self.angle_cutoff):
                count = count + 1
            elif gamma < (90-self.angle_cutoff) or gamma >= (90+self.angle_cutoff):
                count = count + 1
            if count == 1:
                p = 'RHOMBOHEDRAL'
            else:
                p = 'NONE'

    elif self.ty == 'HEXAGONAL':
        if abs(a-b) <= self.dist_cutoff and abs(a-c) > self.dist_cutoff and abs(b-c) > self.dist_cutoff and  (90-self.angle_cutoff) < alpha <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < beta <= (90+self.angle_cutoff) and (120-self.angle_cutoff) < gamma <= (120+self.angle_cutoff):
            p = 'HEXAGONAL'
        elif abs(a-c) <= self.dist_cutoff and abs(a-b) > self.dist_cutoff and abs(b-c) > self.dist_cutoff and (90-self.angle_cutoff) < alpha <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < gamma <= (90+self.angle_cutoff) and (120-self.angle_cutoff) < beta <= (120+self.angle_cutoff):
            p = 'HEXAGONAL'
        elif abs(c-b) <= self.dist_cutoff and abs(a-c) > self.dist_cutoff and abs(b-a) > self.dist_cutoff and (90-self.angle_cutoff) < gamma <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < beta <= (90+self.angle_cutoff) and (120-self.angle_cutoff) < alpha <= (120+self.angle_cutoff):
            p = 'HEXAGONAL'
        else:
            p = 'NONE'

    elif self.ty == 'ORTHORHOMBIC':                                    
        if abs(a-b) > self.dist_cutoff and abs(a-c) > self.dist_cutoff and abs(b-c) > self.dist_cutoff and (90-self.angle_cutoff) < alpha <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < beta <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < gamma <= (90+self.angle_cutoff):
            p = 'ORTHORHOMBIC' 
        else:
            p = 'NONE'

    elif self.ty == 'MONOCLINIC':              
        if abs(a-b) > self.dist_cutoff and abs(a-c) > self.dist_cutoff and abs(b-c) > self.dist_cutoff and (90-self.angle_cutoff) < alpha <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < beta <= (90+self.angle_cutoff) and (90+self.angle_cutoff) < gamma:
            p = 'MONOCLINIC'     
        elif abs(a-b) > self.dist_cutoff and abs(a-c) > self.dist_cutoff and abs(b-c) > self.dist_cutoff and (90-self.angle_cutoff) < alpha <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < gamma <= (90+self.angle_cutoff) and (90+self.angle_cutoff) < beta:           
            p = 'MONOCLINIC' 
        elif abs(a-b) > self.dist_cutoff and abs(a-c) > self.dist_cutoff and abs(b-c) > self.dist_cutoff and (90-self.angle_cutoff) < gamma <= (90+self.angle_cutoff) and (90-self.angle_cutoff) < beta <= (90+self.angle_cutoff) and (90+self.angle_cutoff) < alpha:
            p = 'MONOCLINIC'
        else:
            p = 'NONE'

    elif self.ty == 'TRICLINIC': 
        if abs(a-b) > self.dist_cutoff and abs(a-c) > self.dist_cutoff and abs(b-c) > self.dist_cutoff and abs(alpha-beta) > self.angle_cutoff and abs(alpha-gamma) > self.angle_cutoff and abs(gamma-beta) > self.angle_cutoff:
            p = 'TRICLINIC'
        else:
            p = 'NONE'

    return p