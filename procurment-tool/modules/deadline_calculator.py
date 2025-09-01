import re
from datetime import datetime, date, timedelta
from typing import Optional, List
import calendar

class DeadlineCalculator:
    """
    Handles deadline detection, parsing, and calculation for procurement workflows.
    Automatically calculates supplier deadlines based on client deadlines.
    """
    
    def __init__(self, buffer_days: int = 2):
        """
        Initialize deadline calculator.
        
        Args:
            buffer_days: Number of days to subtract from client deadline for supplier deadline
        """
        self.buffer_days = buffer_days
        
        # Date patterns for extraction
        self.date_patterns = [
            # Standard formats
            (r'(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})', 'dmy'),  # DD/MM/YYYY or DD-MM-YYYY
            (r'(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2})', 'dmy_short'),  # DD/MM/YY
            (r'(\d{4})[\/\-\.](\d{1,2})[\/\-\.](\d{1,2})', 'ymd'),  # YYYY/MM/DD
            
            # Text-based dates
            (r'(\w+)\s+(\d{1,2}),?\s+(\d{4})', 'month_day_year'),  # December 15, 2024
            (r'(\d{1,2})\s+(\w+)\s+(\d{4})', 'day_month_year'),    # 15 December 2024
            (r'(\w+)\s+(\d{1,2})\w{0,2},?\s+(\d{4})', 'month_day_year_ord'),  # December 15th, 2024
        ]
        
        # Context patterns that indicate deadlines
        self.deadline_contexts = [
            r'deadline\s*:?\s*',
            r'due\s*(?:by|on|date)?\s*:?\s*',
            r'submit\s*(?:by|before|on)?\s*:?\s*',
            r'closing\s*(?:date|time)?\s*:?\s*',
            r'no\s*later\s*than\s*:?\s*',
            r'final\s*(?:date|deadline)\s*:?\s*',
            r'tender\s*(?:deadline|due)\s*:?\s*',
            r'proposal\s*(?:deadline|due)\s*:?\s*',
            r'quotation\s*(?:deadline|due)\s*:?\s*'
        ]
        
        # Month name mappings
        self.months = {
            'january': 1, 'jan': 1, 'february': 2, 'feb': 2, 'march': 3, 'mar': 3,
            'april': 4, 'apr': 4, 'may': 5, 'june': 6, 'jun': 6,
            'july': 7, 'jul': 7, 'august': 8, 'aug': 8, 'september': 9, 'sep': 9, 'sept': 9,
            'october': 10, 'oct': 10, 'november': 11, 'nov': 11, 'december': 12, 'dec': 12
        }
    
    def calculate_supplier_deadline(self, client_deadline) -> Optional[date]:
        """
        Calculate supplier deadline based on client deadline.
        
        Args:
            client_deadline: Client deadline (datetime, date, or string)
            
        Returns:
            Supplier deadline as date object, or None if invalid
        """
        try:
            # Convert to date object if necessary
            if isinstance(client_deadline, str):
                parsed_date = self._parse_date_string(client_deadline)
                if not parsed_date:
                    return None
                client_deadline = parsed_date
            elif isinstance(client_deadline, datetime):
                client_deadline = client_deadline.date()
            elif not isinstance(client_deadline, date):
                return None
            
            # Calculate supplier deadline
            supplier_deadline = client_deadline - timedelta(days=self.buffer_days)
            
            # Ensure supplier deadline is not in the past
            today = date.today()
            if supplier_deadline < today:
                # If calculated deadline is in the past, use today as supplier deadline
                supplier_deadline = today
            
            return supplier_deadline
        
        except Exception:
            return None
    
    def extract_deadline_from_text(self, text: str) -> Optional[date]:
        """
        Extract deadline from text using various patterns and contexts.
        
        Args:
            text: Text to search for deadlines
            
        Returns:
            Extracted deadline as date object, or None if not found
        """
        if not text:
            return None
        
        # Convert to lowercase for processing
        text_lower = text.lower()
        
        # Try to find dates near deadline context words
        for context_pattern in self.deadline_contexts:
            context_matches = list(re.finditer(context_pattern, text_lower))
            
            for context_match in context_matches:
                # Look for dates in the vicinity of the context
                start_pos = max(0, context_match.start() - 50)
                end_pos = min(len(text), context_match.end() + 100)
                vicinity_text = text[start_pos:end_pos]
                
                # Try to find a date in this vicinity
                found_date = self._find_date_in_text(vicinity_text)
                if found_date:
                    return found_date
        
        # If no contextual date found, try to find any date in the text
        return self._find_date_in_text(text)
    
    def _find_date_in_text(self, text: str) -> Optional[date]:
        """
        Find the first valid date in the given text.
        
        Args:
            text: Text to search
            
        Returns:
            First valid date found, or None
        """
        for pattern, format_type in self.date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                parsed_date = self._parse_match(match, format_type)
                if parsed_date:
                    # Only return future dates
                    if parsed_date >= date.today():
                        return parsed_date
        
        return None
    
    def _parse_match(self, match, format_type: str) -> Optional[date]:
        """
        Parse a regex match based on the format type.
        
        Args:
            match: Regex match object
            format_type: Type of date format
            
        Returns:
            Parsed date or None
        """
        try:
            groups = match.groups()
            
            if format_type == 'dmy':
                day, month, year = int(groups[0]), int(groups[1]), int(groups[2])
                return date(year, month, day)
            
            elif format_type == 'dmy_short':
                day, month, year = int(groups[0]), int(groups[1]), int(groups[2])
                # Handle 2-digit years
                if year < 50:
                    year += 2000
                else:
                    year += 1900 if year > 50 else 2000
                return date(year, month, day)
            
            elif format_type == 'ymd':
                year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
                return date(year, month, day)
            
            elif format_type == 'month_day_year':
                month_name, day, year = groups[0].lower(), int(groups[1]), int(groups[2])
                month = self.months.get(month_name)
                if month:
                    return date(year, month, day)
            
            elif format_type == 'day_month_year':
                day, month_name, year = int(groups[0]), groups[1].lower(), int(groups[2])
                month = self.months.get(month_name)
                if month:
                    return date(year, month, day)
            
            elif format_type == 'month_day_year_ord':
                month_name, day, year = groups[0].lower(), int(groups[1]), int(groups[2])
                month = self.months.get(month_name)
                if month:
                    return date(year, month, day)
        
        except (ValueError, TypeError):
            pass
        
        return None
    
    def _parse_date_string(self, date_str: str) -> Optional[date]:
        """
        Parse a date string using multiple format attempts.
        
        Args:
            date_str: Date string to parse
            
        Returns:
            Parsed date or None
        """
        # Common date formats to try
        formats = [
            '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y',
            '%d.%m.%Y', '%m.%d.%Y', '%Y/%m/%d', '%B %d, %Y', '%b %d, %Y',
            '%d %B %Y', '%d %b %Y', '%B %d %Y', '%b %d %Y'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).date()
            except ValueError:
                continue
        
        return None
    
    def is_business_day(self, check_date: date) -> bool:
        """
        Check if a date is a business day (Monday-Friday).
        
        Args:
            check_date: Date to check
            
        Returns:
            True if business day, False otherwise
        """
        return check_date.weekday() < 5  # Monday = 0, Friday = 4
    
    def get_next_business_day(self, from_date: date) -> date:
        """
        Get the next business day from the given date.
        
        Args:
            from_date: Starting date
            
        Returns:
            Next business day
        """
        next_day = from_date + timedelta(days=1)
        while not self.is_business_day(next_day):
            next_day += timedelta(days=1)
        return next_day
    
    def get_previous_business_day(self, from_date: date) -> date:
        """
        Get the previous business day from the given date.
        
        Args:
            from_date: Starting date
            
        Returns:
            Previous business day
        """
        prev_day = from_date - timedelta(days=1)
        while not self.is_business_day(prev_day):
            prev_day -= timedelta(days=1)
        return prev_day
    
    def calculate_business_days_between(self, start_date: date, end_date: date) -> int:
        """
        Calculate the number of business days between two dates.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            Number of business days
        """
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        
        business_days = 0
        current_date = start_date
        
        while current_date <= end_date:
            if self.is_business_day(current_date):
                business_days += 1
            current_date += timedelta(days=1)
        
        return business_days
    
    def suggest_optimal_supplier_deadline(self, client_deadline: date, 
                                        complexity_factor: float = 1.0) -> date:
        """
        Suggest an optimal supplier deadline based on project complexity.
        
        Args:
            client_deadline: Client deadline
            complexity_factor: Factor to adjust buffer (1.0 = normal, >1.0 = more complex)
            
        Returns:
            Suggested supplier deadline
        """
        # Adjust buffer days based on complexity
        adjusted_buffer = max(1, int(self.buffer_days * complexity_factor))
        
        # Calculate initial supplier deadline
        supplier_deadline = client_deadline - timedelta(days=adjusted_buffer)
        
        # Ensure it's a business day
        if not self.is_business_day(supplier_deadline):
            supplier_deadline = self.get_previous_business_day(supplier_deadline)
        
        # Ensure it's not in the past
        today = date.today()
        if supplier_deadline < today:
            supplier_deadline = self.get_next_business_day(today)
        
        return supplier_deadline
    
    def get_deadline_status(self, deadline_date: date) -> dict:
        """
        Get status information about a deadline.
        
        Args:
            deadline_date: Deadline to check
            
        Returns:
            Dictionary with status information
        """
        today = date.today()
        days_remaining = (deadline_date - today).days
        
        if days_remaining < 0:
            status = "overdue"
            urgency = "critical"
        elif days_remaining == 0:
            status = "due_today"
            urgency = "critical"
        elif days_remaining <= 1:
            status = "due_soon"
            urgency = "high"
        elif days_remaining <= 3:
            status = "approaching"
            urgency = "medium"
        else:
            status = "on_track"
            urgency = "low"
        
        return {
            'status': status,
            'urgency': urgency,
            'days_remaining': days_remaining,
            'is_business_day': self.is_business_day(deadline_date),
            'deadline_date': deadline_date
        }
