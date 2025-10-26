#!/usr/bin/env python3
import logging
import json
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class NotificationConfig:
    enabled: bool = False
    channels: List[Literal["email", "webhook", "dingtalk", "wechat", "slack"]] = None
    email_config: Optional[Dict] = None
    webhook_url: Optional[str] = None
    dingtalk_webhook: Optional[str] = None
    wechat_webhook: Optional[str] = None
    slack_webhook: Optional[str] = None

@dataclass
class NotificationRecord:
    timestamp: str
    channel: str
    notification_type: str
    subject: str
    message: str
    success: bool
    error_message: Optional[str] = None

class SRENotifier:
    def __init__(self, config: Optional[NotificationConfig] = None):
        self.config = config or NotificationConfig()
        self.notification_history: List[NotificationRecord] = []
        
        if not self.config.enabled:
            logger.warning("SRE Notifier is DISABLED. Notifications will not be sent.")
        else:
            logger.info(f"SRE Notifier initialized with channels: {self.config.channels}")

    def send_alert(self, 
                   subject: str, 
                   message: str, 
                   severity: Literal["info", "warning", "error", "critical"] = "warning",
                   data: Optional[Dict] = None):
        if not self.config.enabled:
            logger.info(f"[MOCK] Alert: {subject} - {message}")
            return
        
        notification_type = f"alert_{severity}"
        formatted_message = self._format_alert_message(subject, message, severity, data)
        
        for channel in (self.config.channels or []):
            try:
                if channel == "email":
                    self._send_email(subject, formatted_message)
                elif channel == "webhook":
                    self._send_webhook(notification_type, formatted_message, data)
                elif channel == "dingtalk":
                    self._send_dingtalk(subject, formatted_message, severity)
                elif channel == "wechat":
                    self._send_wechat(subject, formatted_message, severity)
                elif channel == "slack":
                    self._send_slack(subject, formatted_message, severity)
                
                self._record_notification(channel, notification_type, subject, formatted_message, True)
                
            except Exception as e:
                logger.error(f"Failed to send notification via {channel}: {e}")
                self._record_notification(channel, notification_type, subject, formatted_message, False, str(e))

    def send_scaling_report(self, report: Dict):
        subject = f"自动扩容报告 - {report.get('action', 'unknown')}"
        message = self._format_scaling_report(report)
        
        self.send_alert(subject, message, severity="info", data=report)

    def send_exception_alert(self, exception_summary: Dict):
        critical_count = exception_summary.get("severity_distribution", {}).get("critical", 0)
        unresolved_count = exception_summary.get("unresolved_exceptions", 0)
        
        severity = "critical" if critical_count > 0 else "error"
        subject = f"应用异常告警 - {unresolved_count}个未解决异常"
        message = self._format_exception_alert(exception_summary)
        
        self.send_alert(subject, message, severity=severity, data=exception_summary)

    def send_performance_alert(self, status: Dict):
        alert_count = status.get("alerts", {}).get("total", 0)
        critical_count = status.get("alerts", {}).get("critical", 0)
        
        severity = "critical" if critical_count > 0 else "warning"
        subject = f"性能监控告警 - {alert_count}个活跃告警"
        message = self._format_performance_alert(status)
        
        self.send_alert(subject, message, severity=severity, data=status)

    def _format_alert_message(self, subject: str, message: str, severity: str, data: Optional[Dict]) -> str:
        severity_emoji = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "critical": "🚨"
        }
        
        formatted = f"{severity_emoji.get(severity, '')} {subject}\n\n"
        formatted += f"{message}\n\n"
        formatted += f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        formatted += f"严重级别: {severity.upper()}\n"
        
        return formatted

    def _format_scaling_report(self, report: Dict) -> str:
        message = "## 自动扩容报告\n\n"
        message += f"**操作类型**: {report.get('action', 'N/A')}\n"
        message += f"**时间**: {report.get('timestamp', 'N/A')}\n"
        message += f"**原因**: {', '.join(report.get('reason', []))}\n\n"
        
        message += "### 扩容前状态\n"
        before = report.get("before", {})
        message += f"- 副本数: {before.get('replicas', 'N/A')}\n"
        message += f"- CPU使用率: {before.get('cpu_percent', 'N/A')}%\n"
        message += f"- 内存使用率: {before.get('memory_percent', 'N/A')}%\n\n"
        
        message += "### 扩容后状态\n"
        after = report.get("after", {})
        message += f"- 副本数: {after.get('replicas', 'N/A')}\n"
        message += f"- 预期改善: CPU和内存负载将分散到更多实例\n\n"
        
        message += f"**建议**: {report.get('recommendation', '持续监控系统性能')}\n"
        
        return message

    def _format_exception_alert(self, summary: Dict) -> str:
        message = "## 应用异常统计\n\n"
        message += f"**总异常数**: {summary.get('total_exceptions', 0)}\n"
        message += f"**未解决**: {summary.get('unresolved_exceptions', 0)}\n\n"
        
        message += "### 严重级别分布\n"
        severity_dist = summary.get("severity_distribution", {})
        message += f"- 🚨 Critical: {severity_dist.get('critical', 0)}\n"
        message += f"- ❌ High: {severity_dist.get('high', 0)}\n"
        message += f"- ⚠️ Medium: {severity_dist.get('medium', 0)}\n"
        message += f"- ℹ️ Low: {severity_dist.get('low', 0)}\n\n"
        
        message += "### 异常类型Top 3\n"
        exception_types = summary.get("exception_types", {})
        sorted_types = sorted(exception_types.items(), key=lambda x: x[1], reverse=True)[:3]
        for exc_type, count in sorted_types:
            message += f"- {exc_type}: {count}次\n"
        
        message += "\n### 熔断器状态\n"
        circuit_breakers = summary.get("circuit_breakers", {})
        if circuit_breakers:
            for func_name, state in circuit_breakers.items():
                status = state.get("status", "UNKNOWN")
                message += f"- {func_name}: {status} (失败次数: {state.get('failure_count', 0)})\n"
        else:
            message += "- 所有服务正常\n"
        
        return message

    def _format_performance_alert(self, status: Dict) -> str:
        message = "## 性能监控告警\n\n"
        message += f"**系统状态**: {status.get('status', 'unknown').upper()}\n"
        message += f"**时间**: {status.get('timestamp', 'N/A')}\n\n"
        
        metrics = status.get("metrics", {})
        message += "### 当前指标\n"
        message += f"- CPU使用率: {metrics.get('cpu_percent', 'N/A')}%\n"
        message += f"- 内存使用率: {metrics.get('memory_percent', 'N/A')}%\n"
        message += f"- 磁盘使用率: {metrics.get('disk_percent', 'N/A')}%\n"
        message += f"- 请求总数: {metrics.get('request_count', 0)}\n"
        message += f"- 错误数: {metrics.get('error_count', 0)}\n"
        message += f"- 错误率: {metrics.get('error_rate', 0):.2%}\n"
        message += f"- 平均响应时间: {metrics.get('avg_response_time_ms', 'N/A')}ms\n"
        message += f"- 活跃连接: {metrics.get('active_connections', 0)}\n\n"
        
        alerts = status.get("alerts", {})
        message += "### 活跃告警\n"
        message += f"- 🚨 Critical: {alerts.get('critical', 0)}\n"
        message += f"- ❌ Error: {alerts.get('error', 0)}\n"
        message += f"- ⚠️ Warning: {alerts.get('warning', 0)}\n\n"
        
        recent_alerts = alerts.get("recent", [])
        if recent_alerts:
            message += "### 最近告警\n"
            for alert in recent_alerts[:3]:
                message += f"- [{alert.get('severity', '').upper()}] {alert.get('message', 'N/A')}\n"
        
        return message

    def _send_email(self, subject: str, message: str):
        if not self.config.email_config:
            raise ValueError("Email configuration not provided")
        
        smtp_server = self.config.email_config.get("smtp_server")
        smtp_port = self.config.email_config.get("smtp_port", 587)
        sender = self.config.email_config.get("sender")
        password = self.config.email_config.get("password")
        recipients = self.config.email_config.get("recipients", [])
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = f"[SRE Alert] {subject}"
        
        msg.attach(MIMEText(message, 'plain', 'utf-8'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        
        logger.info(f"Email sent to {len(recipients)} recipients")

    def _send_webhook(self, notification_type: str, message: str, data: Optional[Dict]):
        if not self.config.webhook_url:
            raise ValueError("Webhook URL not configured")
        
        payload = {
            "type": notification_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        
        response = requests.post(
            self.config.webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        
        logger.info(f"Webhook notification sent successfully")

    def _send_dingtalk(self, subject: str, message: str, severity: str):
        if not self.config.dingtalk_webhook:
            raise ValueError("DingTalk webhook not configured")
        
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": subject,
                "text": f"### {subject}\n\n{message}"
            },
            "at": {
                "isAtAll": severity in ["error", "critical"]
            }
        }
        
        response = requests.post(
            self.config.dingtalk_webhook,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        
        logger.info("DingTalk notification sent successfully")

    def _send_wechat(self, subject: str, message: str, severity: str):
        if not self.config.wechat_webhook:
            raise ValueError("WeChat webhook not configured")
        
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"### {subject}\n\n{message}"
            }
        }
        
        response = requests.post(
            self.config.wechat_webhook,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        
        logger.info("WeChat notification sent successfully")

    def _send_slack(self, subject: str, message: str, severity: str):
        if not self.config.slack_webhook:
            raise ValueError("Slack webhook not configured")
        
        color_map = {
            "info": "#36a64f",
            "warning": "#ff9900",
            "error": "#ff0000",
            "critical": "#8b0000"
        }
        
        payload = {
            "attachments": [
                {
                    "color": color_map.get(severity, "#808080"),
                    "title": subject,
                    "text": message,
                    "footer": "AI Navigator SRE",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        }
        
        response = requests.post(
            self.config.slack_webhook,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        
        logger.info("Slack notification sent successfully")

    def _record_notification(self, channel: str, notification_type: str, subject: str, 
                            message: str, success: bool, error_message: Optional[str] = None):
        record = NotificationRecord(
            timestamp=datetime.now().isoformat(),
            channel=channel,
            notification_type=notification_type,
            subject=subject,
            message=message[:200],
            success=success,
            error_message=error_message
        )
        
        self.notification_history.append(record)

    def get_notification_history(self, limit: int = 50) -> List[Dict]:
        return [asdict(record) for record in self.notification_history[-limit:]]

    def get_notification_stats(self) -> Dict:
        total = len(self.notification_history)
        successful = sum(1 for n in self.notification_history if n.success)
        failed = total - successful
        
        by_channel = {}
        for record in self.notification_history:
            channel = record.channel
            by_channel[channel] = by_channel.get(channel, 0) + 1
        
        return {
            "total_notifications": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0,
            "by_channel": by_channel,
            "enabled": self.config.enabled,
            "configured_channels": self.config.channels or []
        }
