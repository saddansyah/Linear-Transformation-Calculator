import numpy as np

class Transform:
    def __init__(self):
        pass

    def translation(point: np.ndarray, tx, ty, tz):

        if(len(point) < 4):
            point = np.append(point, 1)

        translation_matrix = np.array([[1, 0, 0, tx],
                                        [0, 1, 0, ty],
                                        [0, 0, 1, tz],
                                        [0, 0, 0, 1]])
        # print(translation_matrix)
        return (translation_matrix @ point)

    def scaling(point: np.ndarray, sx, sy, sz):
        if(len(point) < 4):
            point = np.append(point, 1)

        scaling_matrix = np.array([[sx, 0, 0, 0],
                                    [0, sy, 0, 0],
                                    [0, 0, sz, 0],
                                    [0, 0, 0, 1]])

        # print(scaling_matrix)
        # slicing index terakhir biar hasilnya [x,y,z] instead of [x,y,z,1]
        return (scaling_matrix @ point)

    def shearxy(point: np.ndarray, shx, shy):
        if(len(point) < 4):
            point = np.append(point, 1)

        shearxy_matrix = np.array([[1, 0, shx, 0],
                                    [0, 1, shy, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]])

        # print(shearxy_matrix)
        # slicing index terakhir biar hasilnya [x,y,z] instead of [x,y,z,1]
        return (shearxy_matrix @ point)

    def shearyz(point: np.ndarray, shy, shz):
        if(len(point) < 4):
            point = np.append(point, 1)

        shearyz_matrix = np.array([[1, 0, 0, 0],
                                    [shy, 1, 0, 0],
                                    [shz, 0, 1, 0],
                                    [0, 0, 0, 1]])

        # print(shearyz_matrix)
        # slicing index terakhir biar hasilnya [x,y,z] instead of [x,y,z,1]
        return (shearyz_matrix @ point)

    def shearxz(point: np.ndarray, shx, shz):
        if(len(point) < 4):
            point = np.append(point, 1)

        shearxz_matrix = np.array([[1, shx, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, shz, 1, 0],
                                    [0, 0, 0, 1]])

        # print(shearxz_matrix)
        # slicing index terakhir biar hasilnya [x,y,z] instead of [x,y,z,1]
        return (shearxz_matrix @ point)

    def rotationx(point: np.ndarray, rot_cos, rot_sin):
        if(len(point) < 4):
            point = np.append(point, 1)

        rotatex_matrix = np.array([[1, 0, 0, 0],
                                    [0, np.cos(np.radians(rot_cos)), -np.sin(np.radians(rot_sin)), 0],
                                    [0, np.sin(np.radians(rot_sin)), np.cos(np.radians(rot_cos)), 0],
                                    [0, 0, 0, 1]])

        # print(rotatex_matrix)
        return (rotatex_matrix @ point)

    def rotationy(point: np.ndarray, rot_cos, rot_sin):
        if(len(point) < 4):
            point = np.append(point, 1)

        rotatey_matrix = np.array([[np.cos(np.radians(rot_cos)), 0, np.sin(np.radians(rot_sin)), 0],
                                    [0, 1, 0, 0],
                                    [-np.sin(np.radians(rot_sin)), 0, np.cos(np.radians(rot_cos)), 0],
                                    [0, 0, 0, 1]])
        
        # print(rotatey_matrix)
        return (rotatey_matrix @ point)

    def rotationz(point: np.ndarray, rot_cos, rot_sin):
        if(len(point) < 4):
            point = np.append(point, 1)

        rotatez_matrix = np.array([[np.cos(np.radians(rot_cos)), -np.sin(np.radians(rot_sin)), 0, 0],
                                    [np.sin(np.radians(rot_sin)), np.cos(np.radians(rot_cos)), 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]])

        # print(rotatez_matrix)
        return (rotatez_matrix @ point)

    def arb_rotation(point: np.ndarray, M: np.ndarray, N: np.ndarray, angle):
        if(len(point) < 4):
            point = np.append(point, 1)
        
        # M > N
        axis = M - N

        L = np.linalg.norm(axis)
        V = np.linalg.norm(axis[1:])
        A, B, C = axis

        print(f"L: {L}\nV: {V}\nA: {A}\nB: {B}\nC: {C}\nPoint: {point}")
        arb_rotate_matrix = Transform.rotationy(Transform.rotationx(Transform.translation(point, -N[0], -N[1], -N[2]), np.degrees(np.arccos(C/V)), np.degrees(np.arcsin(B/V))), np.degrees(np.arccos(V/L)), np.degrees(np.arcsin(-A/L))) 
        arb_rotate_matrix = Transform.rotationz(arb_rotate_matrix, angle, angle)
        arb_rotate_matrix = Transform.translation(Transform.rotationx(Transform.rotationy(arb_rotate_matrix, -np.degrees(np.arccos(V/L)), -np.degrees(np.arcsin(-A/L))) ,-np.degrees(np.arccos(C/V)), -np.degrees(np.arcsin(B/V))) ,N[0], N[1], N[2]) 

        return arb_rotate_matrix
