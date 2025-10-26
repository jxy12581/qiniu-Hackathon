#!/usr/bin/env python3
import logging
import subprocess
import json
from datetime import datetime
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class ScalingEvent:
    timestamp: str
    action: Literal["scale_up", "scale_down", "no_action"]
    reason: List[str]
    before: Dict
    after: Dict
    success: bool
    error_message: Optional[str] = None

class AutoScaler:
    def __init__(self, 
                 deployment_type: Literal["kubernetes", "docker-compose", "systemd"] = "kubernetes",
                 min_replicas: int = 3,
                 max_replicas: int = 10,
                 deployment_name: str = "ai-navigator"):
        
        self.deployment_type = deployment_type
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.deployment_name = deployment_name
        
        self.scaling_history: List[ScalingEvent] = []
        self.current_replicas = min_replicas
        
        logger.info(f"Auto-scaler initialized: type={deployment_type}, replicas={min_replicas}-{max_replicas}")

    def evaluate_scaling(self, recommendation: Dict) -> Optional[ScalingEvent]:
        should_scale_up = recommendation.get("should_scale_up", False)
        should_scale_down = recommendation.get("should_scale_down", False)
        current_metrics = recommendation.get("current_metrics", {})
        reason = recommendation.get("reason", [])
        
        current_status = self._get_current_status()
        
        if should_scale_up and self.current_replicas < self.max_replicas:
            return self._scale_up(reason, current_metrics, current_status)
        
        elif should_scale_down and self.current_replicas > self.min_replicas:
            return self._scale_down(reason, current_metrics, current_status)
        
        else:
            logger.info("No scaling action needed")
            event = ScalingEvent(
                timestamp=datetime.now().isoformat(),
                action="no_action",
                reason=reason or ["资源使用正常"],
                before=current_status,
                after=current_status,
                success=True
            )
            return event

    def _scale_up(self, reason: List[str], metrics: Dict, current_status: Dict) -> ScalingEvent:
        target_replicas = min(self.current_replicas + 2, self.max_replicas)
        
        logger.info(f"Scaling UP from {self.current_replicas} to {target_replicas} replicas")
        
        success = self._execute_scaling(target_replicas)
        
        if success:
            new_status = self._get_current_status()
            self.current_replicas = target_replicas
        else:
            new_status = current_status
        
        event = ScalingEvent(
            timestamp=datetime.now().isoformat(),
            action="scale_up",
            reason=reason,
            before=current_status,
            after=new_status,
            success=success,
            error_message=None if success else "Failed to scale deployment"
        )
        
        self.scaling_history.append(event)
        return event

    def _scale_down(self, reason: List[str], metrics: Dict, current_status: Dict) -> ScalingEvent:
        target_replicas = max(self.current_replicas - 1, self.min_replicas)
        
        logger.info(f"Scaling DOWN from {self.current_replicas} to {target_replicas} replicas")
        
        success = self._execute_scaling(target_replicas)
        
        if success:
            new_status = self._get_current_status()
            self.current_replicas = target_replicas
        else:
            new_status = current_status
        
        event = ScalingEvent(
            timestamp=datetime.now().isoformat(),
            action="scale_down",
            reason=reason,
            before=current_status,
            after=new_status,
            success=success,
            error_message=None if success else "Failed to scale deployment"
        )
        
        self.scaling_history.append(event)
        return event

    def _execute_scaling(self, target_replicas: int) -> bool:
        try:
            if self.deployment_type == "kubernetes":
                return self._scale_kubernetes(target_replicas)
            elif self.deployment_type == "docker-compose":
                return self._scale_docker_compose(target_replicas)
            elif self.deployment_type == "systemd":
                return self._scale_systemd(target_replicas)
            else:
                logger.warning(f"Unsupported deployment type: {self.deployment_type}")
                return False
        
        except Exception as e:
            logger.error(f"Failed to execute scaling: {e}")
            return False

    def _scale_kubernetes(self, target_replicas: int) -> bool:
        try:
            cmd = [
                "kubectl", "scale", 
                f"deployment/{self.deployment_name}",
                f"--replicas={target_replicas}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info(f"Kubernetes scaling successful: {result.stdout}")
                return True
            else:
                logger.error(f"Kubernetes scaling failed: {result.stderr}")
                return False
        
        except subprocess.TimeoutExpired:
            logger.error("Kubernetes scaling command timed out")
            return False
        except FileNotFoundError:
            logger.error("kubectl command not found. Is kubectl installed?")
            return False
        except Exception as e:
            logger.error(f"Kubernetes scaling error: {e}")
            return False

    def _scale_docker_compose(self, target_replicas: int) -> bool:
        try:
            cmd = [
                "docker-compose", "up", "-d",
                "--scale", f"{self.deployment_name}={target_replicas}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info(f"Docker Compose scaling successful")
                return True
            else:
                logger.error(f"Docker Compose scaling failed: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"Docker Compose scaling error: {e}")
            return False

    def _scale_systemd(self, target_replicas: int) -> bool:
        logger.warning("Systemd auto-scaling not fully implemented. Manual intervention required.")
        logger.info(f"Recommended action: Start/stop systemd services to reach {target_replicas} replicas")
        return False

    def _get_current_status(self) -> Dict:
        status = {
            "replicas": self.current_replicas,
            "deployment_type": self.deployment_type,
            "deployment_name": self.deployment_name,
            "timestamp": datetime.now().isoformat()
        }
        
        if self.deployment_type == "kubernetes":
            try:
                cmd = ["kubectl", "get", "deployment", self.deployment_name, "-o", "json"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    deployment_info = json.loads(result.stdout)
                    status["replicas"] = deployment_info.get("spec", {}).get("replicas", self.current_replicas)
                    status["ready_replicas"] = deployment_info.get("status", {}).get("readyReplicas", 0)
                    status["available_replicas"] = deployment_info.get("status", {}).get("availableReplicas", 0)
            
            except Exception as e:
                logger.warning(f"Failed to get K8S deployment status: {e}")
        
        return status

    def manual_scale(self, target_replicas: int, reason: str = "Manual scaling") -> ScalingEvent:
        if target_replicas < self.min_replicas or target_replicas > self.max_replicas:
            raise ValueError(f"Target replicas must be between {self.min_replicas} and {self.max_replicas}")
        
        current_status = self._get_current_status()
        
        success = self._execute_scaling(target_replicas)
        
        if success:
            new_status = self._get_current_status()
            self.current_replicas = target_replicas
            action = "scale_up" if target_replicas > current_status["replicas"] else "scale_down"
        else:
            new_status = current_status
            action = "no_action"
        
        event = ScalingEvent(
            timestamp=datetime.now().isoformat(),
            action=action,
            reason=[reason],
            before=current_status,
            after=new_status,
            success=success,
            error_message=None if success else "Manual scaling failed"
        )
        
        self.scaling_history.append(event)
        return event

    def get_scaling_history(self, limit: int = 20) -> List[Dict]:
        return [asdict(event) for event in self.scaling_history[-limit:]]

    def get_scaling_summary(self) -> Dict:
        total_events = len(self.scaling_history)
        scale_up_count = sum(1 for e in self.scaling_history if e.action == "scale_up")
        scale_down_count = sum(1 for e in self.scaling_history if e.action == "scale_down")
        successful = sum(1 for e in self.scaling_history if e.success)
        
        last_scaling = self.scaling_history[-1] if self.scaling_history else None
        
        return {
            "current_replicas": self.current_replicas,
            "min_replicas": self.min_replicas,
            "max_replicas": self.max_replicas,
            "deployment_type": self.deployment_type,
            "total_scaling_events": total_events,
            "scale_up_count": scale_up_count,
            "scale_down_count": scale_down_count,
            "successful_events": successful,
            "success_rate": successful / total_events if total_events > 0 else 0,
            "last_scaling": asdict(last_scaling) if last_scaling else None
        }

    def generate_scaling_report(self, event: ScalingEvent) -> Dict:
        report = {
            "title": f"自动扩容报告 - {event.action}",
            "timestamp": event.timestamp,
            "action": event.action,
            "reason": event.reason,
            "before": event.before,
            "after": event.after,
            "success": event.success,
            "error_message": event.error_message,
            "recommendation": self._generate_recommendation(event)
        }
        
        return report

    def _generate_recommendation(self, event: ScalingEvent) -> str:
        if event.action == "scale_up":
            return "系统已自动扩容以应对高负载。请持续监控应用性能,确保扩容效果。如果负载持续增加,考虑进一步优化应用或增加资源上限。"
        elif event.action == "scale_down":
            return "系统资源利用率较低,已自动缩容以节省成本。继续监控以确保服务质量不受影响。"
        else:
            return "当前资源使用正常,无需调整副本数。继续监控系统指标。"
