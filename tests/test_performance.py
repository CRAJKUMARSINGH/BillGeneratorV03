"""
Comprehensive Performance Testing Suite for BillGenerator Optimized
Tests performance optimization, caching, memory management, and speed improvements
"""

import pytest
import time
import hashlib
import pandas as pd
import tempfile
import os
from unittest.mock import Mock, patch
import threading
from concurrent.futures import ThreadPoolExecutor
import psutil
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from performance_optimizer import PerformanceOptimizer, performance_optimizer, monitor_performance, cached_operation
from enhanced_cache import EnhancedCache, enhanced_cache, CacheEntry, cached_excel_operation
from utils import sanitize_filename

class TestPerformanceOptimizer:
    """Test suite for PerformanceOptimizer class"""
    
    def setup_method(self):
        """Setup method for each test"""
        self.optimizer = PerformanceOptimizer()
    
    def test_memory_monitoring(self):
        """Test memory usage monitoring"""
        memory_usage = self.optimizer.get_memory_usage()
        assert isinstance(memory_usage, float)
        assert memory_usage > 0
        print(f"✅ Current memory usage: {memory_usage:.1f} MB")
    
    def test_performance_monitoring_context(self):
        """Test performance monitoring context manager"""
        start_time = time.time()
        
        with self.optimizer.performance_monitor("Test Operation"):
            # Simulate work
            time.sleep(0.1)
            test_data = list(range(1000))
            processed = [x * 2 for x in test_data]
        
        duration = time.time() - start_time
        assert duration >= 0.1
        print(f"✅ Performance monitoring captured {duration:.3f}s operation")
    
    def test_memory_optimization(self):
        """Test memory optimization functionality"""
        initial_memory = self.optimizer.get_memory_usage()
        
        # Create some memory load
        large_data = []
        for i in range(1000):
            large_data.append([j for j in range(100)])
        
        current_memory = self.optimizer.get_memory_usage()
        assert current_memory >= initial_memory
        
        # Optimize memory
        freed_memory = self.optimizer.optimize_memory()
        
        final_memory = self.optimizer.get_memory_usage()
        print(f"✅ Memory optimization: freed {freed_memory:.1f} MB")
        print(f"   Initial: {initial_memory:.1f} MB, Current: {current_memory:.1f} MB, Final: {final_memory:.1f} MB")
    
    def test_cache_key_generation(self):
        """Test cache key generation"""
        key1 = self.optimizer.create_cache_key("test", "value", param=123)
        key2 = self.optimizer.create_cache_key("test", "value", param=123)
        key3 = self.optimizer.create_cache_key("test", "different", param=123)
        
        assert key1 == key2  # Same inputs should produce same key
        assert key1 != key3  # Different inputs should produce different keys
        assert len(key1) == 32  # MD5 hash length
        print(f"✅ Cache key generation working: {key1}")
    
    def test_dataframe_optimization(self):
        """Test DataFrame memory optimization"""
        # Create test DataFrame
        test_data = {
            'category': ['A'] * 500 + ['B'] * 300 + ['C'] * 200,  # Good for category conversion
            'large_int': range(1000),  # Can be optimized to smaller int type
            'small_int': [i % 100 for i in range(1000)],  # Can be optimized to uint8
            'float_data': [float(i) for i in range(1000)]  # Can be downcasted
        }
        df = pd.DataFrame(test_data)
        
        original_memory = df.memory_usage(deep=True).sum()
        
        # Optimize DataFrame
        optimized_df = self.optimizer.optimize_dataframe_operations(df)
        
        optimized_memory = optimized_df.memory_usage(deep=True).sum()
        
        assert optimized_memory <= original_memory
        memory_saved = (original_memory - optimized_memory) / original_memory * 100
        
        print(f"✅ DataFrame optimization: {memory_saved:.1f}% memory saved")
        print(f"   Original: {original_memory} bytes, Optimized: {optimized_memory} bytes")
    
    def test_batch_processing(self):
        """Test batch processing functionality"""
        # Create test items
        items = list(range(100))
        
        def simple_processor(batch):
            return [x * 2 for x in batch]
        
        start_time = time.time()
        results = self.optimizer.batch_process_items(items, batch_size=20, processor_func=simple_processor)
        end_time = time.time()
        
        assert len(results) == len(items)
        assert results[0] == 0  # 0 * 2
        assert results[50] == 100  # 50 * 2
        
        print(f"✅ Batch processing completed in {end_time - start_time:.3f}s")
    
    def test_performance_stats(self):
        """Test performance statistics collection"""
        # Perform some operations to generate stats
        with self.optimizer.performance_monitor("Test Stats"):
            time.sleep(0.05)
        
        stats = self.optimizer.get_performance_stats()
        
        assert 'memory_usage_mb' in stats
        assert 'cache_hit_rate' in stats
        assert 'system_info' in stats
        assert 'optimization_recommendations' in stats
        
        assert isinstance(stats['memory_usage_mb'], float)
        assert isinstance(stats['cache_hit_rate'], (int, float))
        assert isinstance(stats['system_info'], dict)
        assert isinstance(stats['optimization_recommendations'], list)
        
        print("✅ Performance stats collection working")
        print(f"   Memory: {stats['memory_usage_mb']:.1f} MB")
        print(f"   CPU: {stats['system_info']['cpu_percent']:.1f}%")

class TestEnhancedCache:
    """Test suite for EnhancedCache class"""
    
    def setup_method(self):
        """Setup method for each test"""
        self.cache = EnhancedCache(cache_dir="test_cache")
    
    def teardown_method(self):
        """Cleanup method for each test"""
        # Clean up test cache files
        import shutil
        if os.path.exists("test_cache"):
            shutil.rmtree("test_cache")
    
    def test_basic_cache_operations(self):
        """Test basic cache set/get operations"""
        key = "test_key"
        value = {"data": "test_value", "number": 123}
        
        # Set value
        self.cache.set(key, value, ttl=60)
        
        # Get value
        cached_value = self.cache.get(key)
        
        assert cached_value == value
        print("✅ Basic cache operations working")
    
    def test_cache_expiration(self):
        """Test cache TTL expiration"""
        key = "expiring_key"
        value = "expiring_value"
        
        # Set with very short TTL
        self.cache.set(key, value, ttl=1)
        
        # Should be available immediately
        assert self.cache.get(key) == value
        
        # Wait for expiration
        time.sleep(2)
        
        # Should be None after expiration
        assert self.cache.get(key) is None
        print("✅ Cache expiration working")
    
    def test_cache_levels(self):
        """Test different cache levels"""
        key = "multilevel_key"
        value = "multilevel_value"
        
        # Test memory only
        self.cache.set(key, value, cache_levels=["memory"])
        assert self.cache.get(key) == value
        
        # Test file only
        self.cache.delete(key)
        self.cache.set(key, value, cache_levels=["file"])
        
        # Clear memory to test file retrieval
        self.cache.memory_cache.clear()
        assert self.cache.get(key) == value
        
        print("✅ Multi-level caching working")
    
    def test_cache_statistics(self):
        """Test cache statistics collection"""
        # Perform some cache operations
        for i in range(10):
            self.cache.set(f"key_{i}", f"value_{i}")
        
        for i in range(5):
            self.cache.get(f"key_{i}")  # Cache hits
        
        for i in range(5):
            self.cache.get(f"missing_key_{i}")  # Cache misses
        
        stats = self.cache.get_cache_stats()
        
        assert 'memory_cache' in stats
        assert 'file_cache' in stats
        assert 'general' in stats
        
        assert stats['memory_cache']['hits'] > 0
        assert stats['memory_cache']['misses'] > 0
        
        print("✅ Cache statistics collection working")
        print(f"   Memory hits: {stats['memory_cache']['hits']}")
        print(f"   Memory misses: {stats['memory_cache']['misses']}")
    
    def test_cache_cleanup(self):
        """Test cache cleanup functionality"""
        # Add some entries
        for i in range(5):
            self.cache.set(f"key_{i}", f"value_{i}", ttl=1)
        
        initial_count = len(self.cache.memory_cache)
        assert initial_count == 5
        
        # Wait for expiration
        time.sleep(2)
        
        # Cleanup
        self.cache.cleanup_expired_entries()
        
        final_count = len(self.cache.memory_cache)
        assert final_count == 0
        
        print(f"✅ Cache cleanup: removed {initial_count} expired entries")
    
    def test_cache_transaction(self):
        """Test cache transaction functionality"""
        try:
            with self.cache.cache_transaction("test_namespace") as tx_cache:
                tx_cache.set("key1", "value1")
                tx_cache.set("key2", "value2")
                
                # Simulate an error to test rollback
                raise ValueError("Test error")
                
        except ValueError:
            # Verify rollback occurred
            assert self.cache.get("key1", "test_namespace") is None
            assert self.cache.get("key2", "test_namespace") is None
            print("✅ Cache transaction rollback working")
    
    def test_function_caching_decorator(self):
        """Test function caching decorator"""
        call_count = 0
        
        @self.cache.cached_function(ttl=60, namespace="test_functions")
        def expensive_function(x, y):
            nonlocal call_count
            call_count += 1
            time.sleep(0.01)  # Simulate work
            return x + y
        
        # First call
        result1 = expensive_function(5, 3)
        assert result1 == 8
        assert call_count == 1
        
        # Second call with same arguments (should be cached)
        result2 = expensive_function(5, 3)
        assert result2 == 8
        assert call_count == 1  # Should not increase
        
        # Third call with different arguments
        result3 = expensive_function(10, 2)
        assert result3 == 12
        assert call_count == 2  # Should increase
        
        print("✅ Function caching decorator working")

class TestPerformanceIntegration:
    """Integration tests for performance optimization"""
    
    def test_cached_operation_decorator(self):
        """Test cached operation decorator"""
        call_count = 0
        
        @cached_operation("test_operation", ttl_hours=1)
        def test_operation(data):
            nonlocal call_count
            call_count += 1
            return f"processed_{data}"
        
        # First call
        result1 = test_operation("test_data")
        assert result1 == "processed_test_data"
        assert call_count == 1
        
        # Second call (should be cached)
        result2 = test_operation("test_data")
        assert result2 == "processed_test_data"
        assert call_count == 1  # Should not increase
        
        print("✅ Cached operation decorator working")
    
    def test_monitor_performance_decorator(self):
        """Test performance monitoring decorator"""
        @monitor_performance("Test Monitored Operation")
        def monitored_operation():
            time.sleep(0.1)
            return "completed"
        
        start_time = time.time()
        result = monitored_operation()
        end_time = time.time()
        
        assert result == "completed"
        assert end_time - start_time >= 0.1
        print("✅ Performance monitoring decorator working")
    
    def test_concurrent_cache_access(self):
        """Test thread-safe cache access"""
        cache = EnhancedCache()
        results = []
        
        def cache_worker(worker_id):
            for i in range(10):
                key = f"worker_{worker_id}_key_{i}"
                value = f"worker_{worker_id}_value_{i}"
                
                # Set and get value
                cache.set(key, value)
                retrieved_value = cache.get(key)
                
                results.append((key, value, retrieved_value))
        
        # Run multiple workers concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(cache_worker, i) for i in range(5)]
            for future in futures:
                future.result()  # Wait for completion
        
        # Verify all operations completed successfully
        assert len(results) == 50  # 5 workers * 10 operations each
        
        for key, original_value, retrieved_value in results:
            assert original_value == retrieved_value
        
        print("✅ Concurrent cache access working")

class TestPerformanceBenchmarks:
    """Performance benchmark tests"""
    
    def test_cache_performance_benchmark(self):
        """Benchmark cache performance"""
        cache = EnhancedCache()
        
        # Benchmark cache writes
        write_start = time.time()
        for i in range(1000):
            cache.set(f"benchmark_key_{i}", f"benchmark_value_{i}")
        write_time = time.time() - write_start
        
        # Benchmark cache reads
        read_start = time.time()
        for i in range(1000):
            cache.get(f"benchmark_key_{i}")
        read_time = time.time() - read_start
        
        print(f"✅ Cache performance benchmark:")
        print(f"   Write time: {write_time:.3f}s ({1000/write_time:.0f} ops/sec)")
        print(f"   Read time: {read_time:.3f}s ({1000/read_time:.0f} ops/sec)")
        
        # Performance assertions
        assert write_time < 1.0  # Should write 1000 items in under 1 second
        assert read_time < 0.5   # Should read 1000 items in under 0.5 seconds
    
    def test_memory_efficiency_benchmark(self):
        """Benchmark memory efficiency"""
        optimizer = PerformanceOptimizer()
        
        initial_memory = optimizer.get_memory_usage()
        
        # Create and optimize large DataFrame
        test_data = {
            'category': ['Category_A'] * 10000 + ['Category_B'] * 10000,
            'values': range(20000),
            'float_values': [float(i) for i in range(20000)]
        }
        df = pd.DataFrame(test_data)
        
        memory_after_creation = optimizer.get_memory_usage()
        
        # Optimize DataFrame
        optimized_df = optimizer.optimize_dataframe_operations(df)
        
        memory_after_optimization = optimizer.get_memory_usage()
        
        # Clean up
        del df, optimized_df
        freed_memory = optimizer.optimize_memory()
        
        final_memory = optimizer.get_memory_usage()
        
        print(f"✅ Memory efficiency benchmark:")
        print(f"   Initial: {initial_memory:.1f} MB")
        print(f"   After creation: {memory_after_creation:.1f} MB")
        print(f"   After optimization: {memory_after_optimization:.1f} MB")
        print(f"   Final: {final_memory:.1f} MB")
        print(f"   Memory freed: {freed_memory:.1f} MB")
    
    def test_batch_processing_benchmark(self):
        """Benchmark batch processing performance"""
        optimizer = PerformanceOptimizer()
        
        # Create large dataset
        large_dataset = list(range(10000))
        
        def simple_processor(batch):
            return [x * 2 + 1 for x in batch]
        
        # Benchmark batch processing
        batch_start = time.time()
        batch_results = optimizer.batch_process_items(
            large_dataset, 
            batch_size=100, 
            processor_func=simple_processor
        )
        batch_time = time.time() - batch_start
        
        # Benchmark regular processing
        regular_start = time.time()
        regular_results = simple_processor(large_dataset)
        regular_time = time.time() - regular_start
        
        assert len(batch_results) == len(regular_results)
        assert batch_results == regular_results
        
        print(f"✅ Batch processing benchmark:")
        print(f"   Batch processing: {batch_time:.3f}s")
        print(f"   Regular processing: {regular_time:.3f}s")
        print(f"   Performance ratio: {regular_time/batch_time:.2f}x")

def test_comprehensive_performance_suite():
    """Run comprehensive performance test suite"""
    print("\n🚀 Running Comprehensive Performance Test Suite")
    print("=" * 60)
    
    # Test Performance Optimizer
    print("\n📊 Testing Performance Optimizer...")
    test_optimizer = TestPerformanceOptimizer()
    test_optimizer.setup_method()
    test_optimizer.test_memory_monitoring()
    test_optimizer.test_performance_monitoring_context()
    test_optimizer.test_memory_optimization()
    test_optimizer.test_cache_key_generation()
    test_optimizer.test_dataframe_optimization()
    test_optimizer.test_batch_processing()
    test_optimizer.test_performance_stats()
    
    # Test Enhanced Cache
    print("\n🗄️ Testing Enhanced Cache...")
    test_cache = TestEnhancedCache()
    test_cache.setup_method()
    test_cache.test_basic_cache_operations()
    test_cache.test_cache_expiration()
    test_cache.test_cache_levels()
    test_cache.test_cache_statistics()
    test_cache.test_cache_cleanup()
    test_cache.test_cache_transaction()
    test_cache.test_function_caching_decorator()
    test_cache.teardown_method()
    
    # Test Integration
    print("\n🔗 Testing Integration...")
    test_integration = TestPerformanceIntegration()
    test_integration.test_cached_operation_decorator()
    test_integration.test_monitor_performance_decorator()
    test_integration.test_concurrent_cache_access()
    
    # Run Benchmarks
    print("\n⏱️ Running Performance Benchmarks...")
    test_benchmarks = TestPerformanceBenchmarks()
    test_benchmarks.test_cache_performance_benchmark()
    test_benchmarks.test_memory_efficiency_benchmark()
    test_benchmarks.test_batch_processing_benchmark()
    
    print("\n✅ All Performance Tests Completed Successfully!")
    print("=" * 60)

if __name__ == "__main__":
    test_comprehensive_performance_suite()
