import tracemalloc
import psutil
import time

class MemoryTracker:
    def __init__(self):
        # Initialize tracemalloc to start tracking memory allocations
        tracemalloc.start()
        self.process = psutil.Process()

    def take_snapshot(self):
        """Take a snapshot of memory usage for detailed tracking."""
        return tracemalloc.take_snapshot()

    def get_memory_usage(self):
        """Get the current memory usage of the process."""
        memory_info = self.process.memory_info()
        return {
            'rss': memory_info.rss / (1024 * 1024),      # Physical memory in MB
            'vms': memory_info.vms / (1024 * 1024),      # Virtual memory in MB
            # 'shared': memory_info.shared / (1024 * 1024) # Shared memory in MB
        }

    def compare_snapshots(self, snapshot1, snapshot2, top=10):
        """Compare two memory snapshots and display the top differences."""
        stats = snapshot2.compare_to(snapshot1, 'lineno')
        print("\nTop memory usage differences:")
        for stat in stats[:top]:
            print(stat)

    def peak_memory_usage(self):
        """Retrieve the peak memory usage tracked by tracemalloc."""
        peak = tracemalloc.get_traced_memory()[1]  # Get peak memory
        return peak / (1024 * 1024)  # Convert to MB

    def stop_tracking(self):
        """Stop tracemalloc and clear traces."""
        tracemalloc.stop()
