import re
from typing import List, Tuple, Optional

class TimeParser:
    """Handles parsing and validation of time availability inputs."""
    
    def __init__(self):
        # Regex pattern to match time ranges like "3-4", "15-17", "12:30-13:15", "9:00-10:30"
        self.time_range_pattern = r'^(\d{1,2}(?::\d{2})?)-(\d{1,2}(?::\d{2})?)$'
        
    def parse_availability(self, availability_string: str) -> List[Tuple[float, float]]:
        """
        Parse availability string into list of time ranges.
        
        Args:
            availability_string: Input like "Not Available", "3-4", "12:30-13:15", or "5-8, 14:30-16:45"
            
        Returns:
            List of tuples representing time ranges (start_time, end_time) in hours as floats
            Empty list if "Not Available" or invalid format
        """
        if not availability_string or availability_string.strip().lower() in ['not available', 'na', 'none']:
            return []
            
        # Split by comma and process each time range
        time_ranges = []
        ranges = [r.strip() for r in availability_string.split(',')]
        
        for time_range in ranges:
            parsed_range = self._parse_single_range(time_range)
            if parsed_range:
                time_ranges.append(parsed_range)
            else:
                raise ValueError(f"Invalid time format: '{time_range}'. Use format like '3-4' or '5-8'")
                
        return time_ranges
    
    def _parse_single_range(self, time_range: str) -> Optional[Tuple[float, float]]:
        """Parse a single time range like '3-4' or '12:30-13:15' into (3.0, 4.0) or (12.5, 13.25)."""
        match = re.match(self.time_range_pattern, time_range.strip())
        if not match:
            return None
            
        start_time_str = match.group(1)
        end_time_str = match.group(2)
        
        # Parse start time
        start_time = self._parse_time_string(start_time_str)
        end_time = self._parse_time_string(end_time_str)
        
        # Validate times are valid
        if start_time is None or end_time is None:
            return None
            
        # Validate times are in 24-hour format
        if not (0 <= start_time < 24 and 0 <= end_time <= 24):
            raise ValueError(f"Times must be between 0:00-23:59. Got: {start_time_str}-{end_time_str}")
            
        # Handle cases where end time is next day (e.g., 22:00-2:00)
        if start_time >= end_time:
            raise ValueError(f"Start time must be less than end time. Got: {start_time_str}-{end_time_str}")
            
        return (start_time, end_time)
    
    def _parse_time_string(self, time_str: str) -> Optional[float]:
        """Parse time string like '3' or '12:30' into float hours like 3.0 or 12.5."""
        if ':' in time_str:
            # Handle format like "12:30"
            try:
                hour_str, minute_str = time_str.split(':')
                hour = int(hour_str)
                minute = int(minute_str)
                
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    return None
                    
                return hour + (minute / 60.0)
            except ValueError:
                return None
        else:
            # Handle format like "3"
            try:
                hour = int(time_str)
                if not (0 <= hour <= 23):
                    return None
                return float(hour)
            except ValueError:
                return None
    
    def format_time_ranges(self, time_ranges: List[Tuple[float, float]]) -> str:
        """Format time ranges back to readable string."""
        if not time_ranges:
            return "Not Available"
            
        formatted_ranges = []
        for start, end in time_ranges:
            start_formatted = self._format_time_float(start)
            end_formatted = self._format_time_float(end)
            formatted_ranges.append(f"{start_formatted}-{end_formatted}")
            
        return ", ".join(formatted_ranges)
    
    def _format_time_float(self, time_float: float) -> str:
        """Format float time like 12.5 into '12:30' or 3.0 into '03:00'."""
        hour = int(time_float)
        minute = int((time_float - hour) * 60)
        return f"{hour:02d}:{minute:02d}"
    
    def validate_availability_input(self, availability_string: str) -> bool:
        """Validate if availability input is in correct format."""
        try:
            self.parse_availability(availability_string)
            return True
        except (ValueError, AttributeError):
            return False
