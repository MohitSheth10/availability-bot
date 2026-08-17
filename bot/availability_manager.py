from typing import Dict, List, Tuple, Set
from collections import defaultdict, Counter
import discord
from time_parser import TimeParser
from config import REGION_TIMEZONES

class AvailabilityManager:
    """Manages user availability data and calculates optimal play times."""
    
    def __init__(self):
        # Store user data: {guild_id: {user_id: {'region': str, 'availability': List[Tuple[float, float]]}}}
        self.user_data: Dict[int, Dict[int, Dict]] = defaultdict(lambda: defaultdict(dict))
        self.time_parser = TimeParser()
        
    def set_user_region(self, guild_id: int, user_id: int, region: str) -> None:
        """Set region for a user."""
        if 'availability' not in self.user_data[guild_id][user_id]:
            self.user_data[guild_id][user_id]['availability'] = []
        self.user_data[guild_id][user_id]['region'] = region
        
    def set_user_availability(self, guild_id: int, user_id: int, availability_string: str) -> None:
        """Set availability for a user and convert to UTC."""
        try:
            time_ranges = self.time_parser.parse_availability(availability_string)
            if 'region' not in self.user_data[guild_id][user_id]:
                self.user_data[guild_id][user_id]['region'] = "Not Set"
            
            # Convert times to UTC based on user's region
            user_region = self.user_data[guild_id][user_id]['region']
            utc_time_ranges = []
            
            if user_region in REGION_TIMEZONES:
                region_offset = REGION_TIMEZONES[user_region]
                for start_time, end_time in time_ranges:
                    # Convert local time to UTC
                    utc_start = (start_time - region_offset) % 24
                    utc_end = (end_time - region_offset) % 24
                    
                    # Handle day boundary crossing
                    if utc_start > utc_end:
                        # Split into two ranges: start to 24 and 0 to end
                        utc_time_ranges.append((utc_start, 24.0))
                        utc_time_ranges.append((0.0, utc_end))
                    else:
                        utc_time_ranges.append((utc_start, utc_end))
            else:
                # If region not set or unknown, store as-is (assume UTC)
                utc_time_ranges = time_ranges
            
            self.user_data[guild_id][user_id]['availability'] = utc_time_ranges
            self.user_data[guild_id][user_id]['local_availability'] = time_ranges  # Store original for display
        except ValueError as e:
            raise ValueError(f"Invalid availability format: {str(e)}")
    
    def get_user_data(self, guild_id: int, user_id: int) -> Dict:
        """Get user data for a specific user."""
        return self.user_data[guild_id].get(user_id, {})
    
    def get_all_users_in_guild(self, guild_id: int) -> Dict[int, Dict]:
        """Get all user data for a guild."""
        return dict(self.user_data[guild_id])
    
    def calculate_optimal_times(self, guild_id: int, min_players: int = 2) -> List[Tuple[float, float, int, List[int]]]:
        """
        Calculate optimal play times for a guild in UTC.
        
        Args:
            guild_id: Discord guild ID
            min_players: Minimum number of players required
            
        Returns:
            List of tuples: (utc_start_time, utc_end_time, player_count, user_ids)
            Sorted by player count (descending) then by start time
        """
        guild_users = self.user_data[guild_id]
        
        # Filter users who have set availability
        available_users = {
            user_id: data for user_id, data in guild_users.items() 
            if 'availability' in data and data['availability']
        }
        
        if len(available_users) < min_players:
            return []
        
        # Create 15-minute interval availability mapping (0.25 hour increments)
        interval_availability = defaultdict(list)
        
        for user_id, user_data in available_users.items():
            for start_time, end_time in user_data['availability']:
                # Split into 15-minute intervals
                current_time = start_time
                while current_time < end_time:
                    interval_availability[current_time].append(user_id)
                    current_time += 0.25  # 15 minutes
        
        # Find time slots with minimum players
        optimal_slots = []
        
        # Group consecutive intervals with same players
        times = sorted(interval_availability.keys())
        if not times:
            return []
            
        current_slot_start = times[0]
        current_slot_players = set(interval_availability[times[0]])
        
        for i in range(1, len(times)):
            time = times[i]
            time_players = set(interval_availability[time])
            
            # If consecutive interval and same players, extend current slot
            if abs(time - times[i-1] - 0.25) < 0.01 and time_players == current_slot_players:
                continue
            else:
                # Save current slot if it meets minimum players requirement and is at least 30 minutes
                slot_duration = times[i-1] + 0.25 - current_slot_start
                if len(current_slot_players) >= min_players and slot_duration >= 0.5:  # At least 30 minutes
                    optimal_slots.append((
                        current_slot_start,
                        times[i-1] + 0.25,
                        len(current_slot_players),
                        list(current_slot_players)
                    ))
                
                # Start new slot
                current_slot_start = time
                current_slot_players = time_players
        
        # Don't forget the last slot
        slot_duration = times[-1] + 0.25 - current_slot_start
        if len(current_slot_players) >= min_players and slot_duration >= 0.5:
            optimal_slots.append((
                current_slot_start,
                times[-1] + 0.25,
                len(current_slot_players),
                list(current_slot_players)
            ))
        
        # Sort by player count (descending) then by start time
        optimal_slots.sort(key=lambda x: (-x[2], x[0]))
        
        return optimal_slots
    
    def convert_utc_to_local(self, utc_time: float, user_region: str) -> float:
        """Convert UTC time to user's local time."""
        if user_region in REGION_TIMEZONES:
            local_time = (utc_time + REGION_TIMEZONES[user_region]) % 24
            return local_time
        return utc_time
    
    def get_optimal_times_for_user(self, guild_id: int, user_id: int, min_players: int = 2) -> List[Tuple[float, float, int, List[int]]]:
        """Get optimal times converted to a specific user's timezone."""
        utc_optimal_times = self.calculate_optimal_times(guild_id, min_players)
        user_data = self.get_user_data(guild_id, user_id)
        user_region = user_data.get('region', 'Not Set')
        
        local_optimal_times = []
        for utc_start, utc_end, count, user_ids in utc_optimal_times:
            local_start = self.convert_utc_to_local(utc_start, user_region)
            local_end = self.convert_utc_to_local(utc_end, user_region)
            
            # Handle day boundary crossing
            if local_start > local_end:
                # This time slot crosses midnight in user's timezone
                local_optimal_times.append((local_start, 24.0, count, user_ids))
                local_optimal_times.append((0.0, local_end, count, user_ids))
            else:
                local_optimal_times.append((local_start, local_end, count, user_ids))
        
        return local_optimal_times
    
    def get_guild_summary(self, guild_id: int) -> str:
        """Get a summary of all users' availability in the guild (in their local times)."""
        guild_users = self.user_data[guild_id]
        
        if not guild_users:
            return "No users have set their region or availability yet."
        
        summary_lines = ["**Current User Status:**"]
        
        for user_id, data in guild_users.items():
            region = data.get('region', 'Not Set')
            local_availability = data.get('local_availability', [])
            
            if local_availability:
                time_str = self.time_parser.format_time_ranges(local_availability)
            else:
                time_str = "Not Set"
                
            summary_lines.append(f"<@{user_id}>: {region} | {time_str}")
        
        return "\n".join(summary_lines)
    
    def users_with_availability_count(self, guild_id: int) -> int:
        """Count how many users have set their availability."""
        guild_users = self.user_data[guild_id]
        return sum(1 for data in guild_users.values() if 'availability' in data)
    
    def clear_user_data(self, guild_id: int, user_id: int) -> None:
        """Clear all data for a specific user."""
        if guild_id in self.user_data and user_id in self.user_data[guild_id]:
            del self.user_data[guild_id][user_id]
    
    def clear_guild_data(self, guild_id: int) -> None:
        """Clear all data for a guild."""
        if guild_id in self.user_data:
            del self.user_data[guild_id]
