import numpy as np

# 6 landmark points around each eye
LEFT_EYE  = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

def get_ear(landmarks, eye_indexes, w, h):
    """
    Calculate Eye Aspect Ratio (EAR)
    EAR < 0.25 means eye is closing
    """
    # Convert landmark positions to pixel coordinates
    points = []
    for idx in eye_indexes:
        x = int(landmarks[idx].x * w)
        y = int(landmarks[idx].y * h)
        points.append((x, y))

    # Vertical distances (how tall the eye is)
    A = np.linalg.norm(np.array(points[1]) - np.array(points[5]))
    B = np.linalg.norm(np.array(points[2]) - np.array(points[4]))

    # Horizontal distance (how wide the eye is)
    C = np.linalg.norm(np.array(points[0]) - np.array(points[3]))

    # EAR formula
    ear = (A + B) / (2.0 * C)
    return round(ear, 3)

def get_average_ear(landmarks, w, h):
    """
    Returns average EAR of both eyes
    More reliable than single eye
    """
    left  = get_ear(landmarks, LEFT_EYE, w, h)
    right = get_ear(landmarks, RIGHT_EYE, w, h)
    return round((left + right) / 2.0, 3)