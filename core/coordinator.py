"""
CrownFull v2.1 - Adaptive Quorum Coordinator
Manages stateful tracking, relative kinematics, and tier logic.
"""
import numpy as np
from typing import Dict
from collections import deque
from core.interception import CleansingProtocols

class RelativeQuorumCoordinator:
    def __init__(self, k_blind: int = 5, phi_firewall: float = 1.18):
        self.k_blind = k_blind
        self.phi_firewall = phi_firewall
        self.recent_phi = deque(maxlen=3) 
        self.abs_velocity_history = [] 
        self.debrief = CleansingProtocols.DEFAULT_DEBRIEF

    def decide(self, v_t: float, phi: float, turn_idx: int) -> Dict[str, object]:
        """Evaluates telemetry against adaptive high-dimensional thresholds."""
        abs_v = abs(v_t)
        self.recent_phi.append(phi)
        in_blind = turn_idx < self.k_blind
        
        if in_blind:
            if abs_v > 0: 
                self.abs_velocity_history.append(abs_v)
            return {"tier": 0, "intercept": False, "msg": "", "threshold": 0.0, "path": "blind_window"}
            
        # Adaptive Kinematics: 3x historical average (Floor: 50.0)
        mean_v = np.mean(self.abs_velocity_history) if self.abs_velocity_history else 50.0
        adaptive_threshold = max(50.0, 3.0 * mean_v)
        
        # Tier 3: Overt Breach
        if abs_v >= adaptive_threshold:
            return {"tier": 3, "intercept": True, "msg": self.debrief, "threshold": adaptive_threshold, "path": "relative_velocity_breach"}

        # Tier 2: Temporal Gate (Patient Poisoner)
        if len(self.recent_phi) == 3 and all(p <= self.phi_firewall for p in self.recent_phi):
            return {"tier": 2, "intercept": True, "msg": self.debrief, "threshold": adaptive_threshold, "path": "temporal_phi_trench"}

        # Safe turn
        self.abs_velocity_history.append(abs_v)
        return {"tier": 0, "intercept": False, "msg": "", "threshold": adaptive_threshold, "path": "clean"}
