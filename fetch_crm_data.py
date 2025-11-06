#!/usr/bin/env python3
"""
CRM Data Retrieval Script
Fetches data from agent.ringcloud.et/crm/{id} for IDs 1000 to 70000
"""

import requests
import json
import time
import sys
import os
from datetime import datetime


class CRMDataFetcher:
    def __init__(self, start_id=1000, end_id=70000, output_dir="crm_data"):
        self.start_id = start_id
        self.end_id = end_id
        self.base_url = "http://agent.ringcloud.et/crm"
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        
        # Statistics
        self.successful = 0
        self.failed = 0
        self.errors = []
        
        # Create output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def fetch_single(self, record_id):
        """Fetch a single record by ID"""
        url = f"{self.base_url}/{record_id}"
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                return {
                    'id': record_id,
                    'status': 'success',
                    'data': response.text,
                    'content_type': response.headers.get('Content-Type', 'unknown')
                }
            else:
                return {
                    'id': record_id,
                    'status': 'error',
                    'status_code': response.status_code,
                    'message': f"HTTP {response.status_code}"
                }
        except requests.exceptions.Timeout:
            return {
                'id': record_id,
                'status': 'error',
                'message': 'Request timeout'
            }
        except requests.exceptions.ConnectionError:
            return {
                'id': record_id,
                'status': 'error',
                'message': 'Connection error'
            }
        except Exception as e:
            return {
                'id': record_id,
                'status': 'error',
                'message': str(e)
            }
    
    def save_result(self, result):
        """Save individual result to file"""
        if result['status'] == 'success':
            filename = f"{self.output_dir}/record_{result['id']}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result['data'])
    
    def save_summary(self):
        """Save summary of the fetch operation"""
        summary = {
            'start_id': self.start_id,
            'end_id': self.end_id,
            'total_attempted': self.end_id - self.start_id + 1,
            'successful': self.successful,
            'failed': self.failed,
            'timestamp': datetime.now().isoformat(),
            'errors': self.errors[:100]  # Save first 100 errors
        }
        
        with open(f"{self.output_dir}/summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
    
    def print_progress(self, current_id, total):
        """Print progress bar"""
        progress = (current_id - self.start_id + 1) / total * 100
        bar_length = 50
        filled = int(bar_length * progress / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        sys.stdout.write(f'\r[{bar}] {progress:.1f}% | ID: {current_id} | ✓ {self.successful} | ✗ {self.failed}')
        sys.stdout.flush()
    
    def fetch_all(self, delay=0.1, save_individual=True):
        """Fetch all records in the range"""
        total = self.end_id - self.start_id + 1
        print(f"Starting data retrieval from {self.base_url}")
        print(f"Range: {self.start_id} to {self.end_id} ({total} records)")
        print(f"Output directory: {self.output_dir}")
        print("-" * 80)
        
        start_time = time.time()
        
        for record_id in range(self.start_id, self.end_id + 1):
            result = self.fetch_single(record_id)
            
            if result['status'] == 'success':
                self.successful += 1
                if save_individual:
                    self.save_result(result)
            else:
                self.failed += 1
                self.errors.append({
                    'id': record_id,
                    'message': result.get('message', 'Unknown error')
                })
            
            self.print_progress(record_id, total)
            
            # Small delay to avoid overwhelming the server
            if delay > 0:
                time.sleep(delay)
        
        elapsed_time = time.time() - start_time
        
        print("\n" + "-" * 80)
        print(f"Completed in {elapsed_time:.2f} seconds")
        print(f"Successful: {self.successful}")
        print(f"Failed: {self.failed}")
        print(f"Success rate: {(self.successful/total*100):.2f}%")
        
        # Save summary
        self.save_summary()
        print(f"\nSummary saved to {self.output_dir}/summary.json")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fetch CRM data from agent.ringcloud.et')
    parser.add_argument('--start', type=int, default=1000, help='Start ID (default: 1000)')
    parser.add_argument('--end', type=int, default=70000, help='End ID (default: 70000)')
    parser.add_argument('--output', type=str, default='crm_data', help='Output directory (default: crm_data)')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay between requests in seconds (default: 0.1)')
    parser.add_argument('--no-save', action='store_true', help='Do not save individual records')
    
    args = parser.parse_args()
    
    fetcher = CRMDataFetcher(
        start_id=args.start,
        end_id=args.end,
        output_dir=args.output
    )
    
    try:
        fetcher.fetch_all(delay=args.delay, save_individual=not args.no_save)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        fetcher.save_summary()
        print(f"Partial results saved to {args.output}/")
        sys.exit(1)


if __name__ == "__main__":
    main()
