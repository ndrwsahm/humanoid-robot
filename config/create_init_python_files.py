import os

def add_init_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        init_path = os.path.join(dirpath, "__init__.py")
        if not os.path.exists(init_path):
            open(init_path, "w").close()
            print(f"Created: {init_path}")

# Replace with your project root
add_init_files("/Users/andre/Github/humanoid-robot/code")
