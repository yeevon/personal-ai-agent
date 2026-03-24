from config import MAX_CHARS
from functions.get_file_content import get_file_content

content = get_file_content("calculator", "lorem.txt")
check_max_char = len(content)
print(f"Max Char Test: {check_max_char <= MAX_CHARS + 92} {check_max_char}\n")
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))