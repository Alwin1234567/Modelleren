import uuid

class ID:
    def __init__(self):
        # Generate a unique ID and store it
        self._id = uuid.uuid4()
    
    def get_id(self):
        # Return the stored unique ID
        return self._id
