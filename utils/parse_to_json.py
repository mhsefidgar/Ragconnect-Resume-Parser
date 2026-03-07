import json

def convert_to_json(result_obj):
    """
    Converts a resume result object into a formatted JSON string.
    """
    # Create a dictionary from the object attributes
    data = {
        "name": result_obj.name,
        "email": result_obj.email,
        "skills": result_obj.skills
    }
    
    # Convert dictionary to JSON string
    return json.dumps(data, indent=4)

# Optional: Function to save directly to a file
def save_resume_json(result_obj, filename="resume.json"):
    data = {
        "name": result_obj.name,
        "email": result_obj.email,
        "skills": result_obj.skills
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)