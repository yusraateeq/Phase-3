import json
import enum
from datetime import datetime, timezone
from uuid import uuid4

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid4().__class__): # Handle UUID
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, enum.Enum):
            return obj.value
        return super().default(obj)

class Priority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

def test_serialization():
    data = {
        "id": uuid4(),
        "created_at": datetime.now(timezone.utc),
        "priority": Priority.HIGH,
        "title": "Hello",
        "is_completed": False
    }
    
    try:
        json_str = json.dumps(data, cls=EnhancedJSONEncoder)
        print("Serialization successful!")
        print(f"JSON Output: {json_str}")
        
        # Verify content
        decoded = json.loads(json_str)
        assert isinstance(decoded["id"], str)
        assert isinstance(decoded["created_at"], str)
        assert decoded["priority"] == "high"
        assert decoded["title"] == "Hello"
        
        print("Verification passed!")
    except Exception as e:
        print(f"Serialization failed: {e}")
        exit(1)

if __name__ == "__main__":
    test_serialization()
