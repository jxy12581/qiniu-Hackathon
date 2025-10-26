#!/usr/bin/env python3
import logging
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional

class StructuredLogger:
    def __init__(self, name: str, log_level: str = "INFO", json_format: bool = True):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        self.json_format = json_format
        
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(getattr(logging, log_level.upper()))
            
            if json_format:
                formatter = JSONFormatter()
            else:
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
            
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _log(self, level: str, message: str, extra: Optional[Dict[str, Any]] = None):
        log_func = getattr(self.logger, level.lower())
        
        if self.json_format:
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "level": level.upper(),
                "message": message,
                "service": "ai-navigator"
            }
            
            if extra:
                log_data.update(extra)
            
            log_func(json.dumps(log_data, ensure_ascii=False))
        else:
            log_func(message, extra=extra or {})
    
    def info(self, message: str, **kwargs):
        self._log("info", message, kwargs)
    
    def warning(self, message: str, **kwargs):
        self._log("warning", message, kwargs)
    
    def error(self, message: str, **kwargs):
        self._log("error", message, kwargs)
    
    def critical(self, message: str, **kwargs):
        self._log("critical", message, kwargs)
    
    def debug(self, message: str, **kwargs):
        self._log("debug", message, kwargs)

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        
        return json.dumps(log_data, ensure_ascii=False)
