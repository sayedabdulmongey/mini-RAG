import re
import os




if __name__ =='__main__':

    filename = "example_file_name.txt"
    random_path = os.path.join("/path/to/directory", filename)
    print(random_path)  # Check if the path looks correct