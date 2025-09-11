"""
Performance Optimizer for BillGenerator Optimized
Implements comprehensive caching, memory optimization, and performance enhancements
"""

import streamlit as st
import functools
import uuid
import hashlib
import pickle
import time
import os
import gc

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime, timedelta
import logging
from pathlib import Path
import threading
import weakref
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """
    Comprehensive performance optimization system with advanced caching and memory management
    """
    
    def __init__(self):
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'memory_saved_mb': 0.0
        }
        self.memory_threshold_mb = 500  # Maximum memory usage before optimization
        self.cache_cleanup_interval = 300  # 5 minutes
        self.last_cleanup = time.time()
        self._setup_streamlit_caching()
        
    def _setup_streamlit_caching(self):
        """Setup Streamlit caching configuration"""
        try:
            # Configure Streamlit caching for maximum performance
            st.set_page_config(
                page_title="BillGenerator Optimized",
                page_icon="💰",
                layout="wide",
                initial_sidebar_state="expanded",
                menu_items={
                    'Get Help': 'https://github.com/crajkumarsingh/BillGenerator',
                    'Report a bug': "mailto:crajkumarsingh@hotmail.com",
                    'About': "Professional Infrastructure Billing System v1.0"
                }
            )
        except:
            # Ignore if already configured
            pass
    
    @contextmanager
    def performance_monitor(self, operation_name: str):
        """Context manager for monitoring operation performance"""
        start_time = time.time()
        start_memory = self.get_memory_usage()
        
        try:
            yield
        finally:
            end_time = time.time()
            end_memory = self.get_memory_usage()
            duration = end_time - start_time
            memory_delta = end_memory - start_memory
            
            logger.info(f"Performance: {operation_name} took {duration:.3f}s, "
                       f"memory change: {memory_delta:.1f}MB")
            
            # Show performance info in Streamlit if available
            try:
                if duration > 1.0:  # Show only for operations > 1 second
                    st.info(f"⏱️ {operation_name}: {duration:.1f}s")
            except:
                pass

    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        if not PSUTIL_AVAILABLE:
            return 0.0
        try:
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024
        except:
            return 0.0

    def optimize_memory(self):
        """Perform memory optimization"""
        current_memory = self.get_memory_usage()
        
        if current_memory > self.memory_threshold_mb:
            logger.warning(f"High memory usage detected: {current_memory:.1f}MB")
            
            # Force garbage collection
            collected = gc.collect()
            
            # Clear Streamlit cache if memory is still high
            new_memory = self.get_memory_usage()
            if new_memory > self.memory_threshold_mb * 0.8:
                try:
                    st.cache_data.clear()
                    st.cache_resource.clear()
                    logger.info("Streamlit cache cleared due to high memory usage")
                except:
                    pass
            
            final_memory = self.get_memory_usage()
            memory_freed = current_memory - final_memory
            
            logger.info(f"Memory optimization: freed {memory_freed:.1f}MB, "
                       f"collected {collected} objects")
            
            return memory_freed
        
        return 0.0

    def create_cache_key(self, *args, **kwargs) -> str:
        """Create a unique cache key from arguments"""
        key_data = {
            'args': args,
            'kwargs': kwargs,
            'timestamp': int(time.time() / 3600)  # Hour-based for cache expiry
        }
        
        # Create hash of the data
        key_string = pickle.dumps(key_data, protocol=pickle.HIGHEST_PROTOCOL)
        return hashlib.md5(key_string).hexdigest()

    def cached_file_operation(self, operation_name: str, ttl_hours: int = 1):
        """Decorator for caching file operations"""
        def decorator(func):
            instance_token = uuid.uuid4().hex  # ensure unique cache namespace per wrapper instance
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key
                func_id = f"{func.__module__}.{getattr(func, '__qualname__', func.__name__)}"
                cache_key = f"{operation_name}:{instance_token}:{func_id}:{self.create_cache_key(*args, **kwargs)}"
                
                # Check if result is cached
                try:
                    if cache_key in st.session_state:
                        cached_result, cached_time = st.session_state[cache_key]
                        if time.time() - cached_time < ttl_hours * 3600:
                            self.cache_stats['hits'] += 1
                            logger.debug(f"Cache hit for {operation_name}")
                            return cached_result
                        else:
                            # Cache expired
                            del st.session_state[cache_key]
                            self.cache_stats['evictions'] += 1
                except:
                    pass
                
                # Execute function and cache result
                with self.performance_monitor(f"Cached {operation_name}"):
                    result = func(*args, **kwargs)
                
                try:
                    st.session_state[cache_key] = (result, time.time())
                    self.cache_stats['misses'] += 1
                    logger.debug(f"Cache miss for {operation_name}, result cached")
                except:
                    logger.warning(f"Failed to cache result for {operation_name}")
                
                return result
            return wrapper
        return decorator

    @st.cache_data(ttl=3600, max_entries=50)
    def cached_excel_processing(file_content: bytes, filename: str) -> Dict[str, Any]:
        """Cache Excel processing results"""
        # This will be implemented by the actual processing function
        pass

    @st.cache_data(ttl=1800, max_entries=20)
    def cached_pdf_generation(content: str, template_type: str) -> bytes:
        """Cache PDF generation results"""
        # This will be implemented by the actual PDF generation function
        pass

    @st.cache_resource(ttl=7200)
    def get_template_engine():
        """Cache template engine initialization"""
        from latex_generator import LaTeXGenerator
        return LaTeXGenerator()

    def optimize_dataframe_operations(self, df):
        """Optimize pandas DataFrame operations"""
        if df.empty:
            return df
        
        optimizations_applied = []
        
        # Convert object columns to category where appropriate
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].nunique() / len(df) < 0.5:  # Less than 50% unique values
                df[col] = df[col].astype('category')
                optimizations_applied.append(f"Converted {col} to category")
        
        # Optimize numeric columns
        for col in df.select_dtypes(include=['int64']).columns:
            if df[col].min() >= 0 and df[col].max() <= 255:
                df[col] = df[col].astype('uint8')
                optimizations_applied.append(f"Optimized {col} to uint8")
            elif df[col].min() >= -32768 and df[col].max() <= 32767:
                df[col] = df[col].astype('int16')
                optimizations_applied.append(f"Optimized {col} to int16")
        
        try:
            import pandas as pd
            for col in df.select_dtypes(include=['float64']).columns:
                if df[col].dtype == 'float64':
                    df[col] = pd.to_numeric(df[col], downcast='float')
                    optimizations_applied.append(f"Downcasted {col} float precision")
        except ImportError:
            pass
        
        if optimizations_applied:
            logger.info(f"DataFrame optimizations: {', '.join(optimizations_applied)}")
        
        return df

    def lazy_load_modules(self):
        """Implement lazy loading for heavy modules"""
        @st.cache_resource
        def load_weasyprint():
            try:
                import weasyprint
                return weasyprint
            except ImportError:
                return None
        
        @st.cache_resource  
        def load_latex_engine():
            try:
                from latex_generator import LaTeXGenerator
                return LaTeXGenerator()
            except ImportError:
                return None
        
        @st.cache_resource
        def load_pdf_tools():
            try:
                from reportlab.pdfgen import canvas
                from reportlab.lib.pagesizes import A4
                return {'canvas': canvas, 'A4': A4}
            except ImportError:
                return None
        
        return {
            'weasyprint': load_weasyprint,
            'latex': load_latex_engine,
            'pdf_tools': load_pdf_tools
        }

    def batch_process_items(self, items: List[Any], batch_size: int = 50, 
                          processor_func: Callable = None) -> List[Any]:
        """Process items in batches to optimize memory usage"""
        if not items or not processor_func:
            return []
        
        results = []
        total_batches = (len(items) + batch_size - 1) // batch_size
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_number = i // batch_size + 1
            
            with self.performance_monitor(f"Batch {batch_number}/{total_batches}"):
                batch_results = processor_func(batch)
                results.extend(batch_results)
            
            # Memory cleanup after each batch
            if batch_number % 5 == 0:  # Every 5 batches
                self.optimize_memory()
        
        return results

    def implement_progress_cache(self, operation_key: str, total_steps: int):
        """Implement progress caching for long operations"""
        progress_key = f"progress_{operation_key}"
        
        if progress_key not in st.session_state:
            st.session_state[progress_key] = {
                'current_step': 0,
                'total_steps': total_steps,
                'start_time': time.time(),
                'completed_items': []
            }
        
        return st.session_state[progress_key]

    def update_progress_cache(self, operation_key: str, step: int, item_result: Any = None):
        """Update progress cache"""
        progress_key = f"progress_{operation_key}"
        
        if progress_key in st.session_state:
            progress_data = st.session_state[progress_key]
            progress_data['current_step'] = step
            
            if item_result is not None:
                progress_data['completed_items'].append(item_result)
            
            # Calculate and display progress
            percentage = (step / progress_data['total_steps']) * 100
            elapsed_time = time.time() - progress_data['start_time']
            
            try:
                # Update Streamlit progress bar
                if 'progress_bar' not in st.session_state:
                    st.session_state['progress_bar'] = st.progress(0)
                
                st.session_state['progress_bar'].progress(percentage / 100)
                
                if percentage > 0:
                    eta = (elapsed_time / percentage) * (100 - percentage)
                    st.info(f"Progress: {percentage:.1f}% - ETA: {eta:.1f}s")
                
            except:
                pass  # Ignore if Streamlit context not available

    def cleanup_expired_cache(self):
        """Clean up expired cache entries"""
        current_time = time.time()
        
        if current_time - self.last_cleanup < self.cache_cleanup_interval:
            return
        
        keys_to_remove = []
        
        for key in st.session_state.keys():
            if key.startswith(('cached_', 'progress_')):
                try:
                    cached_data = st.session_state[key]
                    if isinstance(cached_data, tuple) and len(cached_data) >= 2:
                        cached_time = cached_data[1]
                        if current_time - cached_time > 3600:  # 1 hour expiry
                            keys_to_remove.append(key)
                except:
                    keys_to_remove.append(key)  # Remove corrupted entries
        
        # Remove expired entries
        for key in keys_to_remove:
            try:
                del st.session_state[key]
                self.cache_stats['evictions'] += 1
            except:
                pass
        
        self.last_cleanup = current_time
        
        if keys_to_remove:
            logger.info(f"Cache cleanup: removed {len(keys_to_remove)} expired entries")

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        memory_usage = self.get_memory_usage()
        cache_hit_rate = 0
        
        total_cache_operations = self.cache_stats['hits'] + self.cache_stats['misses']
        if total_cache_operations > 0:
            cache_hit_rate = (self.cache_stats['hits'] / total_cache_operations) * 100
        
        return {
            'memory_usage_mb': memory_usage,
            'cache_hit_rate': cache_hit_rate,
            'cache_stats': self.cache_stats.copy(),
            'system_info': {
                'cpu_percent': psutil.cpu_percent(interval=1) if PSUTIL_AVAILABLE else 0.0,
                'memory_percent': psutil.virtual_memory().percent if PSUTIL_AVAILABLE else 0.0,
                'disk_usage_percent': (psutil.disk_usage('/').percent if os.name != 'nt' 
                                    else psutil.disk_usage('C:\\').percent) if PSUTIL_AVAILABLE else 0.0
            },
            'optimization_recommendations': self._get_optimization_recommendations(memory_usage)
        }

    def _get_optimization_recommendations(self, memory_usage: float) -> List[str]:
        """Get optimization recommendations based on current performance"""
        recommendations = []
        
        if memory_usage > 400:
            recommendations.append("Consider processing files in smaller batches")
        
        if self.cache_stats['misses'] > self.cache_stats['hits'] * 2:
            recommendations.append("Cache miss rate is high - consider adjusting cache TTL")
        
        if PSUTIL_AVAILABLE and psutil.cpu_percent(interval=1) > 80:
            recommendations.append("High CPU usage detected - consider parallel processing")
        
        if not recommendations:
            recommendations.append("System performance is optimal")
        
        return recommendations

    def display_performance_dashboard(self):
        """Display performance dashboard in Streamlit"""
        try:
            stats = self.get_performance_stats()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Memory Usage",
                    value=f"{stats['memory_usage_mb']:.1f} MB",
                    delta=f"{stats['cache_stats']['memory_saved_mb']:.1f} MB saved"
                )
            
            with col2:
                st.metric(
                    label="Cache Hit Rate",
                    value=f"{stats['cache_hit_rate']:.1f}%",
                    delta=f"{stats['cache_stats']['hits']} hits"
                )
            
            with col3:
                st.metric(
                    label="CPU Usage",
                    value=f"{stats['system_info']['cpu_percent']:.1f}%"
                )
            
            # Performance recommendations
            if stats['optimization_recommendations']:
                st.subheader("🔧 Performance Recommendations")
                for rec in stats['optimization_recommendations']:
                    st.info(rec)
                    
        except Exception as e:
            logger.error(f"Error displaying performance dashboard: {e}")

# Global performance optimizer instance
performance_optimizer = PerformanceOptimizer()

# Decorators for easy use
def cached_operation(operation_name: str, ttl_hours: int = 1):
    """Decorator for caching operations"""
    return performance_optimizer.cached_file_operation(operation_name, ttl_hours)

def monitor_performance(operation_name: str):
    """Decorator for monitoring performance"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with performance_optimizer.performance_monitor(operation_name):
                return func(*args, **kwargs)
        return wrapper
    return decorator

def optimize_dataframe(func):
    """Decorator to automatically optimize DataFrames returned by functions"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if hasattr(result, 'iloc'):  # Check if it's a DataFrame
            result = performance_optimizer.optimize_dataframe_operations(result)
        return result
    return wrapper
