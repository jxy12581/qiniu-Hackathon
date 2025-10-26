#!/usr/bin/env python3
import time
import psutil
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass, asdict
from collections import deque
import threading
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_percent: float
    request_count: int
    error_count: int
    avg_response_time_ms: float
    active_connections: int

@dataclass
class Alert:
    timestamp: str
    severity: Literal["warning", "error", "critical"]
    metric_type: str
    metric_value: float
    threshold: float
    message: str
    resolved: bool = False

class PerformanceMonitor:
    def __init__(self, 
                 cpu_threshold: float = 80.0,
                 memory_threshold: float = 85.0,
                 disk_threshold: float = 90.0,
                 error_rate_threshold: float = 0.05,
                 response_time_threshold_ms: float = 1000.0,
                 metrics_retention_minutes: int = 60):
        
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.disk_threshold = disk_threshold
        self.error_rate_threshold = error_rate_threshold
        self.response_time_threshold_ms = response_time_threshold_ms
        self.metrics_retention_minutes = metrics_retention_minutes
        
        self.metrics_history: deque = deque(maxlen=1000)
        self.alerts: List[Alert] = []
        self.request_count = 0
        self.error_count = 0
        self.response_times: deque = deque(maxlen=100)
        self.active_connections = 0
        
        self._lock = threading.Lock()
        self._monitoring = False
        self._monitor_thread = None
        
        logger.info(f"Performance monitor initialized with thresholds: CPU={cpu_threshold}%, Memory={memory_threshold}%, Disk={disk_threshold}%")

    def start_monitoring(self, interval_seconds: int = 30):
        if self._monitoring:
            logger.warning("Monitoring is already running")
            return
        
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval_seconds,), daemon=True)
        self._monitor_thread.start()
        logger.info(f"Started performance monitoring with {interval_seconds}s interval")

    def stop_monitoring(self):
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
        logger.info("Stopped performance monitoring")

    def _monitor_loop(self, interval_seconds: int):
        while self._monitoring:
            try:
                metrics = self.collect_metrics()
                self._check_thresholds(metrics)
                time.sleep(interval_seconds)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval_seconds)

    def collect_metrics(self) -> PerformanceMetrics:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        with self._lock:
            avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0.0
            
            metrics = PerformanceMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / (1024 * 1024),
                memory_available_mb=memory.available / (1024 * 1024),
                disk_percent=disk.percent,
                request_count=self.request_count,
                error_count=self.error_count,
                avg_response_time_ms=avg_response_time,
                active_connections=self.active_connections
            )
            
            self.metrics_history.append(metrics)
        
        return metrics

    def _check_thresholds(self, metrics: PerformanceMetrics):
        if metrics.cpu_percent > self.cpu_threshold:
            self._create_alert(
                severity="critical" if metrics.cpu_percent > 95 else "warning",
                metric_type="cpu",
                metric_value=metrics.cpu_percent,
                threshold=self.cpu_threshold,
                message=f"CPU使用率过高: {metrics.cpu_percent:.1f}%"
            )
        
        if metrics.memory_percent > self.memory_threshold:
            self._create_alert(
                severity="critical" if metrics.memory_percent > 95 else "warning",
                metric_type="memory",
                metric_value=metrics.memory_percent,
                threshold=self.memory_threshold,
                message=f"内存使用率过高: {metrics.memory_percent:.1f}%"
            )
        
        if metrics.disk_percent > self.disk_threshold:
            self._create_alert(
                severity="error",
                metric_type="disk",
                metric_value=metrics.disk_percent,
                threshold=self.disk_threshold,
                message=f"磁盘使用率过高: {metrics.disk_percent:.1f}%"
            )
        
        if metrics.request_count > 0:
            error_rate = metrics.error_count / metrics.request_count
            if error_rate > self.error_rate_threshold:
                self._create_alert(
                    severity="error",
                    metric_type="error_rate",
                    metric_value=error_rate,
                    threshold=self.error_rate_threshold,
                    message=f"错误率过高: {error_rate:.2%} ({metrics.error_count}/{metrics.request_count})"
                )
        
        if metrics.avg_response_time_ms > self.response_time_threshold_ms:
            self._create_alert(
                severity="warning",
                metric_type="response_time",
                metric_value=metrics.avg_response_time_ms,
                threshold=self.response_time_threshold_ms,
                message=f"平均响应时间过长: {metrics.avg_response_time_ms:.1f}ms"
            )

    def _create_alert(self, severity: str, metric_type: str, metric_value: float, threshold: float, message: str):
        alert = Alert(
            timestamp=datetime.now().isoformat(),
            severity=severity,
            metric_type=metric_type,
            metric_value=metric_value,
            threshold=threshold,
            message=message
        )
        
        with self._lock:
            existing_unresolved = [a for a in self.alerts if not a.resolved and a.metric_type == metric_type]
            if not existing_unresolved:
                self.alerts.append(alert)
                logger.warning(f"Alert created: {message}")

    def record_request(self, response_time_ms: float, is_error: bool = False):
        with self._lock:
            self.request_count += 1
            if is_error:
                self.error_count += 1
            self.response_times.append(response_time_ms)

    def increment_connections(self):
        with self._lock:
            self.active_connections += 1

    def decrement_connections(self):
        with self._lock:
            self.active_connections = max(0, self.active_connections - 1)

    def get_current_status(self) -> Dict:
        metrics = self.collect_metrics()
        
        with self._lock:
            unresolved_alerts = [a for a in self.alerts if not a.resolved]
            
            error_rate = (metrics.error_count / metrics.request_count) if metrics.request_count > 0 else 0.0
            
            status = {
                "timestamp": metrics.timestamp,
                "status": "critical" if any(a.severity == "critical" for a in unresolved_alerts) else 
                         "warning" if unresolved_alerts else "healthy",
                "metrics": {
                    "cpu_percent": metrics.cpu_percent,
                    "memory_percent": metrics.memory_percent,
                    "memory_used_mb": round(metrics.memory_used_mb, 2),
                    "memory_available_mb": round(metrics.memory_available_mb, 2),
                    "disk_percent": metrics.disk_percent,
                    "request_count": metrics.request_count,
                    "error_count": metrics.error_count,
                    "error_rate": round(error_rate, 4),
                    "avg_response_time_ms": round(metrics.avg_response_time_ms, 2),
                    "active_connections": metrics.active_connections
                },
                "alerts": {
                    "total": len(unresolved_alerts),
                    "critical": sum(1 for a in unresolved_alerts if a.severity == "critical"),
                    "error": sum(1 for a in unresolved_alerts if a.severity == "error"),
                    "warning": sum(1 for a in unresolved_alerts if a.severity == "warning"),
                    "recent": [asdict(a) for a in unresolved_alerts[-5:]]
                },
                "thresholds": {
                    "cpu": self.cpu_threshold,
                    "memory": self.memory_threshold,
                    "disk": self.disk_threshold,
                    "error_rate": self.error_rate_threshold,
                    "response_time_ms": self.response_time_threshold_ms
                }
            }
        
        return status

    def get_metrics_history(self, minutes: Optional[int] = None) -> List[Dict]:
        if minutes is None:
            minutes = self.metrics_retention_minutes
        
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        with self._lock:
            filtered_metrics = [
                asdict(m) for m in self.metrics_history
                if datetime.fromisoformat(m.timestamp) >= cutoff_time
            ]
        
        return filtered_metrics

    def get_all_alerts(self, include_resolved: bool = False) -> List[Dict]:
        with self._lock:
            if include_resolved:
                return [asdict(a) for a in self.alerts]
            else:
                return [asdict(a) for a in self.alerts if not a.resolved]

    def resolve_alert(self, metric_type: str):
        with self._lock:
            for alert in self.alerts:
                if alert.metric_type == metric_type and not alert.resolved:
                    alert.resolved = True
                    logger.info(f"Alert resolved: {alert.message}")

    def reset_counters(self):
        with self._lock:
            self.request_count = 0
            self.error_count = 0
            self.response_times.clear()
        logger.info("Performance counters reset")

    def get_scaling_recommendation(self) -> Dict:
        metrics = self.collect_metrics()
        
        should_scale_up = (
            metrics.cpu_percent > 70 or 
            metrics.memory_percent > 75 or
            metrics.avg_response_time_ms > self.response_time_threshold_ms * 0.8
        )
        
        should_scale_down = (
            metrics.cpu_percent < 30 and 
            metrics.memory_percent < 40 and
            metrics.avg_response_time_ms < self.response_time_threshold_ms * 0.3 and
            metrics.request_count < 100
        )
        
        recommendation = {
            "timestamp": datetime.now().isoformat(),
            "should_scale_up": should_scale_up,
            "should_scale_down": should_scale_down,
            "current_metrics": {
                "cpu_percent": metrics.cpu_percent,
                "memory_percent": metrics.memory_percent,
                "avg_response_time_ms": metrics.avg_response_time_ms,
                "request_count": metrics.request_count
            },
            "reason": []
        }
        
        if should_scale_up:
            if metrics.cpu_percent > 70:
                recommendation["reason"].append(f"CPU使用率高: {metrics.cpu_percent:.1f}%")
            if metrics.memory_percent > 75:
                recommendation["reason"].append(f"内存使用率高: {metrics.memory_percent:.1f}%")
            if metrics.avg_response_time_ms > self.response_time_threshold_ms * 0.8:
                recommendation["reason"].append(f"响应时间较长: {metrics.avg_response_time_ms:.1f}ms")
        
        if should_scale_down:
            recommendation["reason"].append("资源使用率低,可以缩容以节省成本")
        
        if not should_scale_up and not should_scale_down:
            recommendation["reason"].append("当前资源使用正常,无需调整")
        
        return recommendation
