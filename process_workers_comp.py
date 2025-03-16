#!/usr/bin/env python
"""
Command-line script to run the Kansas Workers' Compensation document processor.
"""
import sys
from kswc_processor.main import main

if __name__ == "__main__":
    sys.exit(main()) 