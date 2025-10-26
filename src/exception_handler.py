#!/usr/bin/env python3
import logging
import traceback
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from enum import Enum
import time

logger = logging.getLogger(__name__)

class ExceptionSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ExceptionRecord:
    timestamp: str
    exception_type: str
    exception_message: str
    traceback: str
    severity: str
    context: Dict
    retry_count: int
    resolved: bool
    resolution_time: Optional[str] = None

class ExceptionHandler:
    def __init__(self, 
                 max_retry_attempts: int = 3,
                 retry_delay_seconds: float = 1.0,
                 circuit_breaker_threshold: int = 5,
                 circuit_breaker_timeout_seconds: int = 60):
        
        self.max_retry_attempts = max_retry_attempts
        self.retry_delay_seconds = retry_delay_seconds
        self.circuit_breaker_threshold = circuit_breaker_threshold
        self.circuit_breaker_timeout_seconds = circuit_breaker_timeout_seconds
        
        self.exception_history: List[ExceptionRecord] = []
        self.circuit_breaker_state: Dict[str, Dict] = {}
        
        logger.info("Exception handler initialized with auto-retry and circuit breaker")

    async def handle_with_retry(self, 
                                 func: Callable, 
                                 *args, 
                                 context: Optional[Dict] = None,
                                 **kwargs) -> Any:
        context = context or {}
        func_name = func.__name__
        
        for attempt in range(self.max_retry_attempts):
            try:
                if self._is_circuit_open(func_name):
                    raise Exception(f"Circuit breaker open for {func_name}")
                
                result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
                
                self._record_success(func_name)
                
                return result
                
            except Exception as e:
                severity = self._classify_exception(e)
                
                exc_record = ExceptionRecord(
                    timestamp=datetime.now().isoformat(),
                    exception_type=type(e).__name__,
                    exception_message=str(e),
                    traceback=traceback.format_exc(),
                    severity=severity.value,
                    context={**context, "function": func_name, "attempt": attempt + 1},
                    retry_count=attempt + 1,
                    resolved=False
                )
                
                self.exception_history.append(exc_record)
                
                self._update_circuit_breaker(func_name)
                
                if attempt < self.max_retry_attempts - 1:
                    logger.warning(f"Attempt {attempt + 1} failed for {func_name}: {str(e)}. Retrying in {self.retry_delay_seconds}s...")
                    await asyncio.sleep(self.retry_delay_seconds)
                else:
                    logger.error(f"All {self.max_retry_attempts} attempts failed for {func_name}: {str(e)}")
                    raise

    def handle_sync_with_retry(self, 
                               func: Callable, 
                               *args, 
                               context: Optional[Dict] = None,
                               **kwargs) -> Any:
        context = context or {}
        func_name = func.__name__
        
        for attempt in range(self.max_retry_attempts):
            try:
                if self._is_circuit_open(func_name):
                    raise Exception(f"Circuit breaker open for {func_name}")
                
                result = func(*args, **kwargs)
                
                self._record_success(func_name)
                
                return result
                
            except Exception as e:
                severity = self._classify_exception(e)
                
                exc_record = ExceptionRecord(
                    timestamp=datetime.now().isoformat(),
                    exception_type=type(e).__name__,
                    exception_message=str(e),
                    traceback=traceback.format_exc(),
                    severity=severity.value,
                    context={**context, "function": func_name, "attempt": attempt + 1},
                    retry_count=attempt + 1,
                    resolved=False
                )
                
                self.exception_history.append(exc_record)
                
                self._update_circuit_breaker(func_name)
                
                if attempt < self.max_retry_attempts - 1:
                    logger.warning(f"Attempt {attempt + 1} failed for {func_name}: {str(e)}. Retrying in {self.retry_delay_seconds}s...")
                    time.sleep(self.retry_delay_seconds)
                else:
                    logger.error(f"All {self.max_retry_attempts} attempts failed for {func_name}: {str(e)}")
                    raise

    def _classify_exception(self, exception: Exception) -> ExceptionSeverity:
        exc_type = type(exception).__name__
        exc_msg = str(exception).lower()
        
        critical_keywords = ["database", "connection", "timeout", "memory", "disk"]
        high_keywords = ["permission", "authentication", "authorization", "not found"]
        
        if any(keyword in exc_msg for keyword in critical_keywords):
            return ExceptionSeverity.CRITICAL
        elif any(keyword in exc_msg for keyword in high_keywords):
            return ExceptionSeverity.HIGH
        elif exc_type in ["ValueError", "KeyError", "TypeError"]:
            return ExceptionSeverity.MEDIUM
        else:
            return ExceptionSeverity.LOW

    def _is_circuit_open(self, func_name: str) -> bool:
        if func_name not in self.circuit_breaker_state:
            return False
        
        state = self.circuit_breaker_state[func_name]
        
        if state.get("is_open", False):
            time_since_open = time.time() - state.get("opened_at", 0)
            
            if time_since_open > self.circuit_breaker_timeout_seconds:
                state["is_open"] = False
                state["failure_count"] = 0
                logger.info(f"Circuit breaker for {func_name} moved to half-open state")
                return False
            else:
                logger.warning(f"Circuit breaker for {func_name} is OPEN (failures: {state.get('failure_count', 0)})")
                return True
        
        return False

    def _update_circuit_breaker(self, func_name: str):
        if func_name not in self.circuit_breaker_state:
            self.circuit_breaker_state[func_name] = {
                "failure_count": 0,
                "is_open": False,
                "opened_at": None
            }
        
        state = self.circuit_breaker_state[func_name]
        state["failure_count"] += 1
        
        if state["failure_count"] >= self.circuit_breaker_threshold:
            state["is_open"] = True
            state["opened_at"] = time.time()
            logger.error(f"Circuit breaker OPENED for {func_name} after {state['failure_count']} failures")

    def _record_success(self, func_name: str):
        if func_name in self.circuit_breaker_state:
            state = self.circuit_breaker_state[func_name]
            if state.get("is_open", False):
                logger.info(f"Circuit breaker for {func_name} recovered and CLOSED")
            state["failure_count"] = 0
            state["is_open"] = False

    def get_exception_summary(self) -> Dict:
        total = len(self.exception_history)
        unresolved = sum(1 for e in self.exception_history if not e.resolved)
        
        severity_counts = {
            "critical": sum(1 for e in self.exception_history if e.severity == "critical"),
            "high": sum(1 for e in self.exception_history if e.severity == "high"),
            "medium": sum(1 for e in self.exception_history if e.severity == "medium"),
            "low": sum(1 for e in self.exception_history if e.severity == "low")
        }
        
        exception_types = {}
        for exc in self.exception_history:
            exc_type = exc.exception_type
            exception_types[exc_type] = exception_types.get(exc_type, 0) + 1
        
        recent_exceptions = [asdict(e) for e in self.exception_history[-10:]]
        
        circuit_breakers = {
            func_name: {
                "failure_count": state["failure_count"],
                "is_open": state.get("is_open", False),
                "status": "OPEN" if state.get("is_open", False) else "CLOSED"
            }
            for func_name, state in self.circuit_breaker_state.items()
        }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_exceptions": total,
            "unresolved_exceptions": unresolved,
            "severity_distribution": severity_counts,
            "exception_types": exception_types,
            "recent_exceptions": recent_exceptions,
            "circuit_breakers": circuit_breakers,
            "config": {
                "max_retry_attempts": self.max_retry_attempts,
                "retry_delay_seconds": self.retry_delay_seconds,
                "circuit_breaker_threshold": self.circuit_breaker_threshold,
                "circuit_breaker_timeout_seconds": self.circuit_breaker_timeout_seconds
            }
        }

    def get_unresolved_exceptions(self) -> List[Dict]:
        return [asdict(e) for e in self.exception_history if not e.resolved]

    def mark_resolved(self, exception_type: str):
        resolved_count = 0
        for exc in self.exception_history:
            if exc.exception_type == exception_type and not exc.resolved:
                exc.resolved = True
                exc.resolution_time = datetime.now().isoformat()
                resolved_count += 1
        
        if resolved_count > 0:
            logger.info(f"Marked {resolved_count} {exception_type} exceptions as resolved")
        
        return resolved_count

    def clear_history(self):
        self.exception_history.clear()
        self.circuit_breaker_state.clear()
        logger.info("Exception history and circuit breaker state cleared")

    def get_degraded_services(self) -> List[str]:
        return [
            func_name 
            for func_name, state in self.circuit_breaker_state.items() 
            if state.get("is_open", False)
        ]
