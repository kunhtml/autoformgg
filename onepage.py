import datetime
import random
import requests
import time

URL = "https://docs.google.com/forms/d/e/(id)/formResponse"

def get_gmt_time(delta=7):
    ''' Get local time Vietnam (+7), help run correctly on any server '''
    date = datetime.datetime.now()
    tz = datetime.timezone(datetime.timedelta(hours=delta))
    return date.astimezone(tz)

def load_used_data():
    ''' Load used names and emails from a file '''
    try:
        with open("used_data.txt", "r") as f:
            used_names = set()
            used_emails = set()
            for line in f:
                name, email = line.strip().split(',')
                used_names.add(name)
                used_emails.add(email)
            return used_names, used_emails
    except FileNotFoundError:
        return set(), set()

def save_used_data(used_names, used_emails):
    ''' Save used names and emails to a file '''
    with open("used_data.txt", "w") as f:
        for name in used_names:
            # Tạo email giả dựa trên tên nếu không có email thực tế
            email = f"{name.lower().replace(' ', '')}@gmail.com"
            f.write(f"{name},{email}\n")

def load_names_from_file(file_path):
    ''' Load names from a file and return as a list '''
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            names = [line.strip() for line in f.readlines() if line.strip()]
        return names
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại.")
        return []

def fill_form(used_names, used_emails, names_list):
    ''' Generate random form data '''
    # Khởi tạo lại seed của random mỗi lần chạy
    random.seed()

    # Chọn tên ngẫu nhiên từ danh sách
    available_names = [name for name in names_list if name not in used_names]
    if not available_names:
        print("Đã hết tên để sử dụng!")
        return None

    name = random.choice(available_names)
    used_names.add(name)
    email = f"{name.lower().replace(' ', '')}@gmail.com"
    used_emails.add(email)

    # Danh sách giá trị cơ bản và giá trị có trọng số
    weighted_values = ["1", "2", "3", "4", "4", "5", "5", "5", "5"]

    # Tạo dictionary chứa tất cả các entry và giá trị tương ứng
    form_data = {
        "entry.1407895576": random.choice(weighted_values),
        "entry.670211927": random.choice(weighted_values),
        "entry.958840722": random.choice(weighted_values),
        "entry.1016235368": random.choice(weighted_values),
        "entry.22365963": random.choice(weighted_values),
        "entry.908312035": random.choice(weighted_values),
        "entry.1024875306": random.choice(weighted_values),
        "entry.1874851143": random.choice(weighted_values),
        "entry.769948362": random.choice(weighted_values),
        "entry.1488032517": random.choice(weighted_values),
        "entry.1539484353": random.choice(weighted_values),
        "entry.1894728305": random.choice(weighted_values),
        "entry.1807063731": random.choice(weighted_values),
        "entry.1117920360": random.choice(weighted_values),
        "entry.857436292": random.choice(weighted_values),
        "entry.64129414": random.choice(weighted_values),
        "entry.421463454": random.choice(weighted_values),
        "entry.190649394": random.choice(weighted_values),
        "entry.1218429730": random.choice(weighted_values),
        "entry.696559849": random.choice(weighted_values),
        # Thêm trường tên và email (giả định Google Form có các trường này)
        "entry.123456789": name,  # Thay bằng entry ID thực tế của trường "Name" nếu có
        "entry.987654321": email,  # Thay bằng entry ID thực tế của trường "Email" nếu có
    }

    # In dữ liệu trước khi gửi
    print("\nValues being sent:")
    for key, value in form_data.items():
        print(f"{key}: {value}")
    
    return form_data

def submit(url, data):
    ''' Submit form to url with data '''
    try:
        res = requests.post(url, data=data, timeout=10)
        if res.status_code != 200:
            raise Exception("Error! Can't submit form", res.status_code)
        else:
            print(f"Đã gửi form thành công lúc {get_gmt_time().strftime('%Y-%m-%d %H:%M:%S')} (GMT+7)", flush=True)
        return True
    except Exception as e:
        print("Error!", e, flush=True)
        return False

def main():
    print("Running script...", flush=True)

    # Load danh sách tên từ file 'names.txt'
    names_list = load_names_from_file("names.txt")
    if not names_list:
        print("Không có tên nào để sử dụng.")
        return

    # Khởi tạo set để lưu các giá trị đã sử dụng
    used_names, used_emails = load_used_data()

    # Thực hiện 150 lần (hoặc ít hơn nếu hết tên)
    for i in range(150):
        print(f"\nSubmitting form {i+1}/150...")
        form_data = fill_form(used_names, used_emails, names_list)
        if form_data is None:
            break
        submit(URL, form_data)
        save_used_data(used_names, used_emails)  # Lưu dữ liệu vào tệp sau mỗi lần gửi
        time.sleep(5)  # Dừng 5 giây giữa mỗi lần gửi form để tránh bị chặn

if __name__ == "__main__":
    main()
