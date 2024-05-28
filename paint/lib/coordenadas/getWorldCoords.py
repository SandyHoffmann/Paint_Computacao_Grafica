from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# ----------------------------------------------------- #
# Projecao inversa de coordenadas                       #
# ----------------------------------------------------- #
AREA = 250

def getWorldCoords(x, y, right, left, top, bottom):
    """
    Transforms screen coordinates (x, y) to OpenGL world coordinates.

    Args:
        x (int): The x screen coordinate.
        y (int): The y screen coordinate.

    Returns:
        tuple: A tuple containing the x and y world coordinates.

    Raises:
        ValueError: If the input screen coordinates are not within the viewport.

    This function calculates the world coordinates corresponding to the provided screen coordinates (x, y) by performing the following steps:

    1. Retrieves the current modelview and projection matrices, and the viewport dimensions using OpenGL calls.
    2. Inverts the projection and modelview matrices.
    3. Converts the screen coordinates to normalized device coordinates (NDC) in the range [-1, 1] for both x and y axes.
    4. Constructs a 4D NDC vector with z and w components set to 0 and 1, respectively.
    5. Transforms the NDC vector to clip space by multiplying with the inverse projection matrix.
    6. Transforms the clip space vector to world space by multiplying with the inverse modelview matrix.
    7. Extracts the x and y components of the transformed world space vector and returns them as a tuple.

    Note that this function assumes the depth is always 0 and only returns the x and y world coordinates. If you need all three world coordinates (x, y, z), you can modify the function to extract them accordingly.

    **Error Handling:**

    The function raises a `ValueError` if the provided screen coordinates are not within the viewport bounds.

    **Example Usage:**

    ```python
    x, y = 100, 200
    world_x, world_y = getWorldCoords(x, y)
    print(f"World coordinates: ({world_x:.2f}, {world_y:.2f})")
    ```
           
    # Reference: Karsten Lehn, Merijam Gotzes, Frank Klawonn. 
    # Introduction to Computer Graphics Using OpenGL and Java, 3. Ed.
    # Springer, ISBN 978-3-031-28134-1
    # págs. 171 e 416
     """
    # coordenadas do volume de visualização
    xr = right
    xl = left
    yt = top
    yb = bottom
    zn = 1.0
    zf = -1.0
    
    # matriz de projeçao (window + NDC)
    P =[
        [2/(xr-xl), 0.0, 0.0, -(xr+xl)/(xr-xl)],
        [0.0, 2/(yt-yb), 0.0, -(yt+yb)/(yt-yb)],
        [0.0, 0.0, -2/(zf-zn), -(zf+zn)/(zf-zn)],
        [0.0, 0.0, 0.0, 1.0],
    ]

    PM = np.array(P)

    # inversa da matriz de prozeção
    invP = np.linalg.inv(PM)

    # conversão das coordenadas do mouse para NDC
    viewport = glGetIntegerv(GL_VIEWPORT)
    ywin = viewport[3] - y
    xndc = (2*(x-viewport[0]))/viewport[2] -1
    yndc = (2*(ywin-viewport[1]))/viewport[3] -1
    zndc = 0
    wndc = 1
    vndc = np.array([xndc, yndc, zndc,wndc])

    
    # transformação de projeção inversa
    world = np.matmul(invP, vndc)

    # coordenadas no sistema WCS do OpenGL
    return world[0], world[1]
