import os
import string
import shutil

# 1. Вывод всех директорий и файлов в указанном пути
def list_dirs_files(path):
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return dirs, files

# 2. Проверка доступа к пути
def check_path_access(path):
    return {
        "exists": os.path.exists(path),
        "readable": os.access(path, os.R_OK),
        "writable": os.access(path, os.W_OK),
        "executable": os.access(path, os.X_OK)
    }

# 3. Проверка существования пути
def path_info(path):
    if os.path.exists(path):
        return os.path.split(path)  # (directory, filename)
    return None

# 4. Подсчет строк в файле
def count_lines(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)

# 5. Запись списка в файл
def write_list_to_file(filename, lst):
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(f"{item}\n" for item in lst)

# 6. Генерация 26 файлов от A.txt до Z.txt
def generate_alphabet_files():
    for letter in string.ascii_uppercase:
        with open(f"{letter}.txt", "w") as f:
            f.write(f"File {letter}.txt created.")

# 7. Копирование содержимого файла
def copy_file(src, dest):
    shutil.copy(src, dest)

# 8. Удаление файла после проверки
def delete_file(filename):
    if os.path.exists(filename) and os.access(filename, os.W_OK):
        os.remove(filename)
        return True
    return False

# Тесты
print(list_dirs_files("."))  
print(check_path_access("example.txt"))  
print(path_info("example.txt"))  
write_list_to_file("test.txt", ["Hello", "World"])  
generate_alphabet_files()  
copy_file("test.txt", "copy_test.txt")  
print(delete_file("test.txt"))  