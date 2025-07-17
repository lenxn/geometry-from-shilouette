# -*- coding: utf-8 -*-
"""
This module contains everything for creating a triangle mesh of a solid
of revolution, described by a given silhouette. 
"""
import argparse
from math import pi
from os import path
from enum import IntEnum
import numpy as np
import numpy.typing as npt


DEFAULT_NUM_R_SEGMENTS = 10

class UV(IntEnum):
    """IntEnum class referring to the indices of U and V coordinates."""
    U = 0
    V = 1


def export_ply(out_path: str, texture_file: str, vertices: npt.NDArray[np.float64], uvs: npt.NDArray[np.float64], faces: npt.NDArray[np.int_]):
    """Exports the given triangle mesh as PLY file with ASCII encoding.

    The mesh is fully described by its list of vertices, UV-coordinates,
    and faces. 
    The export fails if those lists are empty or do not match.

    Args:
        out_path (str): The file path of the output PLY file.
        texture_file (str): The file path of the texture to map.
        vertices (npt.NDArray[np.float64]): The mesh's vertices.
        uvs (npt.NDArray[np.float64]): The mesh's UV-coordinates.
        faces (npt.NDArray[np.int_]): The mesh's faces.
    """
    header = f"""ply
format ascii 1.0
comment TextureFile {texture_file}
element vertex {len(vertices)}
property float x
property float y
property float z
element face {len(faces)}
property list uchar int vertex_indices
property list uchar float texcoord
end_header
"""
    assert len(vertices) and len(uvs) and len(faces)
    assert len(vertices)==len(uvs)

    faces_strings = faces.astype(str)
    uvs_strings = uvs.astype(str)
    vertices_ply: str = '\n'.join([' '.join(v) for v in vertices.astype(str)])+'\n'
    faces_ply_strings: list[str] = []
    for i,_ in enumerate(faces):
        faces_ply_strings.append(f"{len(faces[i])} {' '.join(faces_strings[i])} {2*len(faces[i])} {' '.join([uvs_strings[v_idx,0]+' '+uvs_strings[v_idx,1] for v_idx in faces[i]])}\n")
    faces_ply: str = '\n'.join(faces_ply_strings)+'\n'

    with open(out_path, "w", encoding='utf-8') as f:
        f.write(header+vertices_ply+faces_ply)
        f.close()


def generate_mesh(silhouette: npt.NDArray[np.float64],
                  r_segments: int
                  ) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64], npt.NDArray[np.int_]]:
    """
    Generates a solid of revolution triangle mesh from a silhouette.

    The silhouette points describe the shape of the resulting solid of
    revolution and should be in the interval [0,1).
    Fails if the given number of radial segments is below 3.
    
    Args:
        silhouette (npt.NDArray[np.float64]): The silhouette points.
        r_segments (int): The number of radial segments.

    Returns:
        tuple[npt.NDArray[np.float64], npt.NDArray[np.float64], npt.NDArray[np.int_]]:
            The tuple of vertices, uv-coordinates and faces.
    """
    assert np.all(silhouette >= 0) and np.all(silhouette <= 1)
    v_segments = len(silhouette)
    assert r_segments >= 3
    assert v_segments >= 1

    vertices: list[list[float]] = []
    uvs: list[list[float]] = []
    faces: list[list[int]] = []
    for j in range(r_segments+1):
        angle = 2*pi/r_segments*j
        for i in range(v_segments):
            curr_v_idx = len(vertices)
            vertices.append([np.cos(angle)*silhouette[i], np.sin(angle)*silhouette[i], i/v_segments])
            uvs.append([j/r_segments,i/v_segments])
            if j > 0 and i > 0:
                faces.append([curr_v_idx-v_segments-1, curr_v_idx-1, curr_v_idx])
                faces.append([curr_v_idx, curr_v_idx-v_segments, curr_v_idx-v_segments-1])
    return np.array(vertices), np.array(uvs), np.array(faces)


def main():
    parser = argparse.ArgumentParser(description="Generates a triangle mesh of a solid of revolution, described by a given silhouette.")
    parser.add_argument('-c', '--contour',
                        help='Path to the input file containing the contour [0,1] as list (*.lst)',
                        required=True)
    parser.add_argument('-t', '--texture',
                        help='Path to texture file (*.[png|jpg])',
                        required=True)
    parser.add_argument('-o', '--output-mesh',
                        help='The path for the generated Proxy Geometry (*.ply)',
                        required=True)
    parser.add_argument('--radial-segments',
                        help=f"Number of radial segments of the generated mesh, default={DEFAULT_NUM_R_SEGMENTS}",
                        default=DEFAULT_NUM_R_SEGMENTS)
    args = parser.parse_args()

    assert path.isfile(args.contour)
    assert path.isfile(args.texture)
    with open(args.contour, 'r', encoding='utf-8') as f:
        contour = np.array([float(l) for l in f.readlines()])
        f.close()

    vertices,uvs,faces = generate_mesh(contour, int(args.radial_segments))
    export_ply(args.output_mesh, args.texture, vertices,uvs,faces)


if __name__ == "__main__":
    main()
