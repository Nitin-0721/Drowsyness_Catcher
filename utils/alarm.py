import pygame
import os

# Initialize pygame mixer for sound
pygame.mixer.init()


COLORS = {
    0: (0, 255, 0),    
    1: (0, 165, 255),  
    2: (0, 0, 255),    
    3: (0, 0, 180),    
}


def load_alarm(path="alerts/alarm.wav"):
    """
    Load alarm sound file.
    If file doesn't exist, alarm will be skipped silently.
    """
    if os.path.exists(path):
        pygame.mixer.music.load(path)
        return True
    else:
        print(f"Warning: Alarm file not found at {path}")
        print("Continuing without sound...")
        return False

def play_alarm():
    """Play alarm on loop"""
    try:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1) 
    except:
        pass

def stop_alarm():
    """Stop alarm"""
    try:
        pygame.mixer.music.stop()
    except:
        pass


class AlertManager:
    def __init__(self):
        self.alarm_loaded = load_alarm()
        self.last_level   = 0

    def update(self, alert_level):
        """
        Call this every frame with current alert level.
        Handles sound automatically.
        """
        if alert_level >= 2:
            if self.alarm_loaded:
                play_alarm()

        else:
            stop_alarm()

        self.last_level = alert_level

    def get_color(self, alert_level):
        """Returns BGR color for current alert level"""
        return COLORS.get(alert_level, (0, 255, 0))

    def get_border_color(self, alert_level):
        """Returns border color — only shows on danger/critical"""
        if alert_level >= 2:
            return COLORS[alert_level]
        return None