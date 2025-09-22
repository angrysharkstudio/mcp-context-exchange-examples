"""
Sample code for demonstrating MCP context exchange
This file has intentional issues for the AI models to find
"""


class DataProcessor:
    """Processes data from various sources"""
    
    def __init__(self):
        self.data = []
        self.processed_count = 0
    
    def process_file(self, filename):
        """Read and process a file"""
        # Issue 1: No error handling for file operations
        with open(filename, 'r') as f:
            data = f.read()
        
        # Issue 2: No validation of data format
        items = data.split(',')
        
        # Issue 3: Inefficient - processes same data multiple times
        for item in items:
            self.process_item(item)
            self.process_item(item)  # Duplicate processing
        
        return items
    
    def process_item(self, item):
        """Process a single item"""
        # Issue 4: No input validation
        processed = item.strip().upper()
        
        # Issue 5: Race condition - not thread-safe
        self.data.append(processed)
        self.processed_count += 1
        
        return processed
    
    def get_statistics(self):
        """Get processing statistics"""
        # Issue 6: Division by zero not handled
        average_length = sum(len(item) for item in self.data) / len(self.data)
        
        return {
            "total": self.processed_count,
            "unique": len(set(self.data)),
            "average_length": average_length
        }


def calculate_metrics(values):
    """Calculate basic metrics for a list of values"""
    # Issue 7: No validation for an empty list
    total = sum(values)
    
    # Issue 8: Repeated calculation without caching
    average = total / len(values)
    
    # Issue 9: Inefficient for large lists
    sorted_values = sorted(values)
    median = sorted_values[len(values) // 2]
    
    return {
        "total": total,
        "average": average,
        "median": median,
        "min": min(values),
        "max": max(values)
    }


def find_duplicates(items):
    """Find duplicate items in a list"""
    duplicates = []
    
    # Issue 10: O(n²) complexity - inefficient
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    
    return duplicates


# Issue 11: Global state
processed_files = []


def main():
    """Main entry point"""
    processor = DataProcessor()
    
    # Issue 12: Hardcoded filename
    data = processor.process_file("input.txt")
    
    # Issue 13: No error handling
    metrics = calculate_metrics([1, 2, 3, 4, 5])
    
    print(f"Processed {len(data)} items")
    print(f"Metrics: {metrics}")


if __name__ == "__main__":
    main()