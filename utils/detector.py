from utils.ear_calculator import get_average_ear
from utils.mar_calculator import is_yawning


EAR_THRESHOLD    = 0.25   
CONSEC_FRAMES    = 20     
YAWN_THRESHOLD   = 0.6    
YAWN_MAX_COUNT   = 3      

class DrowsinessDetector:
    def __init__(self):
        self.ear_frame_counter = 0   
        self.yawn_counter      = 0   
        self.is_yawning_now    = False  

    def reset(self):
        self.ear_frame_counter = 0
        self.yawn_counter      = 0
        self.is_yawning_now    = False

    def update(self, landmarks, w, h):
        """
        Call this every frame.
        Returns alert_level and status info.

        Alert levels:
        0 = AWAKE
        1 = WARNING  (eyes closing)
        2 = DANGER   (eyes closed too long)
        3 = CRITICAL (eyes closed + yawning)
        """

        # ── Step 1: Calculate EAR ──
        ear = get_average_ear(landmarks, w, h)

        # ── Step 2: Calculate MAR ──
        yawning, mar = is_yawning(landmarks, w, h, YAWN_THRESHOLD)

        # ── Step 3: Count yawns ──
        # Only count once per yawn (not every frame)
        if yawning and not self.is_yawning_now:
            self.yawn_counter += 1
            self.is_yawning_now = True
        elif not yawning:
            self.is_yawning_now = False

        # ── Step 4: Count drowsy frames ──
        if ear < EAR_THRESHOLD:
            self.ear_frame_counter += 1
        else:
            self.ear_frame_counter = 0

        # ── Step 5: Determine alert level ──
        alert_level = self._get_alert_level(ear, yawning)

        # ── Step 6: Return everything ──
        return {
            "alert_level"   : alert_level,
            "ear"           : ear,
            "mar"           : mar,
            "yawn_count"    : self.yawn_counter,
            "frame_counter" : self.ear_frame_counter,
            "is_yawning"    : yawning,
            "status"        : self._get_status(alert_level)
        }

    def _get_alert_level(self, ear, yawning):
        # CRITICAL — eyes closed long + yawning
        if self.ear_frame_counter >= CONSEC_FRAMES and yawning:
            return 3

        # DANGER — eyes closed too long
        elif self.ear_frame_counter >= CONSEC_FRAMES:
            return 2

        # WARNING — eyes starting to close or yawning too much
        elif self.ear_frame_counter >= 10 or self.yawn_counter >= YAWN_MAX_COUNT:
            return 1

        # AWAKE — all good
        else:
            return 0

    def _get_status(self, alert_level):
        statuses = {
            0: "AWAKE",
            1: "WARNING",
            2: "DANGER",
            3: "CRITICAL"
        }
        return statuses[alert_level]