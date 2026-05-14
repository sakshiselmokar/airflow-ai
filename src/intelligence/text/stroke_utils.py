# import numpy as np

# CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# char_to_idx = {c: i for i, c in enumerate(CHARS)}
# idx_to_char = {i: c for i, c in enumerate(CHARS)}


# def stroke_to_sequence(points, max_len=100):
#     """
#     Convert [(x,y)...] → [(x,y,dx,dy)...]
#     """
#     if len(points) < 5:
#         return None

#     pts = np.array(points, dtype=np.float32)

#     # normalize
#     pts = pts - np.mean(pts, axis=0)
#     pts = pts / (np.std(pts) + 1e-6)

#     seq = []

#     for i in range(1, len(pts)):
#         x, y = pts[i]
#         dx = pts[i][0] - pts[i - 1][0]
#         dy = pts[i][1] - pts[i - 1][1]

#         seq.append([x, y, dx, dy])

#     # pad / trim
#     if len(seq) > max_len:
#         seq = seq[:max_len]
#     else:
#         seq += [[0, 0, 0, 0]] * (max_len - len(seq))

#     return np.array(seq, dtype=np.float32)

import numpy as np


CHARS="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

char_to_idx={c:i for i,c in enumerate(CHARS)}
idx_to_char={i:c for i,c in enumerate(CHARS)}


def stroke_to_sequence(
        points,
        max_len=100
):

    if len(points)<10:
        return None


    pts=np.array(
        points,
        dtype=np.float32
    )


    # center

    pts[:,0]-=np.mean(pts[:,0])
    pts[:,1]-=np.mean(pts[:,1])


    # scale independently

    xstd=np.std(pts[:,0])+1e-6
    ystd=np.std(pts[:,1])+1e-6

    pts[:,0]/=xstd
    pts[:,1]/=ystd


    seq=[]


    for i in range(
            1,
            len(pts)
    ):

        x,y=pts[i]

        dx=pts[i][0]-pts[i-1][0]
        dy=pts[i][1]-pts[i-1][1]

        seq.append(
            [
                x,
                y,
                dx,
                dy
            ]
        )


    if len(seq)>max_len:

        seq=seq[:max_len]

    else:

        seq += (
            [[0,0,0,0]]
            *
            (
                max_len-len(seq)
            )
        )

    return np.array(
        seq,
        dtype=np.float32
    )