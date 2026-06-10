import numpy as np

# 8 landmark points around the mouth
MOUTH = [61, 291, 39, 181, 0, 17, 269, 405]

def get_mar(landmarks, w, h):
    """
    Calculate Mouth Aspect Ratio (MAR)
    MAR > 0.6 means mouth is open = yawning
    """
    # Convert landmark positions to pixel coordinates
    points = []
    for idx in MOUTH:
        x = int(landmarks[idx].x * w)
        y = int(landmarks[idx].y * h)
        points.append((x, y))

    # Vertical distances (how tall the mouth opening is)
    A = np.linalg.norm(np.array(points[2]) - np.array(points[6]))
    B = np.linalg.norm(np.array(points[3]) - np.array(points[5]))

    # Horizontal distance (how wide the mouth is)
    C = np.linalg.norm(np.array(points[0]) - np.array(points[1]))

    # MAR formula
    mar = (A + B) / (2.0 * C)
    return round(mar, 3)

def is_yawning(landmarks, w, h, threshold=0.6):
    """
    Returns True if person is yawning
    """
    mar = get_mar(landmarks, w, h)
    return mar > threshold, mar
