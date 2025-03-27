import os

def save_to_markdown(text, directory="X:\\aillm\\gitAtlas\\atlas-research-agent\\Agents", filename="paper.md"):
    os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
    file_path = os.path.join(directory, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Text saved to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")


