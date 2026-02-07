# Sample Python file for testing the docstring generator
# This file intentionally has missing docstrings


def calculate_area(length, width):
    return length * width


def get_user_name(user_id: int) -> str:
    # Fetch user name from database
    return f"User_{user_id}"


async def fetch_data(url: str, timeout: int = 30):
    # Simulate async data fetching
    import asyncio
    await asyncio.sleep(1)
    return {"data": "sample"}


class DataProcessor:
    def __init__(self, name: str):
        self.name = name
        self.data = []
    
    def add_item(self, item):
        self.data.append(item)
    
    def process(self):
        """Process all items in the data list."""
        return [x * 2 for x in self.data]
    
    @staticmethod
    def validate_input(value):
        return value is not None
    
    @classmethod
    def create_default(cls):
        return cls("default")


class Calculator:
    """A simple calculator class."""
    
    def add(self, a: float, b: float) -> float:
        """
        Add two numbers.
        
        Args:
            a (float): First number
            b (float): Second number
            
        Returns:
            float: Sum of a and b
        """
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        return a * b


def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email


def create_user(username: str, email: str, age: int = 18, **kwargs):
    user = {
        "username": username,
        "email": email,
        "age": age
    }
    user.update(kwargs)
    return user
