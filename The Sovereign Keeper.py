import requests
import csv
from datetime import datetime
import os

# --- [0] ข้อมูลทางเทคนิค ---
URL = "https://dhamkaroo-keeper-default-rtdb.asia-southeast1.firebasedatabase.app/users.json"
HISTORY_FILE = "keeper_history.csv"


def get_history_summary():
    """อ่านประวัติศาสตร์เพื่อนำมาเปรียบเทียบวัดผล"""
    if not os.path.isfile(HISTORY_FILE):
        return None
    try:
        with open(HISTORY_FILE, mode='r', encoding='utf-8-sig') as f:
            reader = list(csv.reader(f))
            if len(reader) > 1:
                return {
                    "first": reader[1],  # บันทึกแรกสุดในประวัติศาสตร์
                    "last": reader[-1],  # บันทึกล่าสุดก่อนการรันครั้งนี้
                    "count": len(reader) - 1
                }
    except:
        return None
    return None


def save_and_analyze(total, live, percent):
    history = get_history_summary()
    current_percent_str = f"{percent:.1f}%"

    # --- [ส่วนวิเคราะห์เชิงยุทธศาสตร์] ---
    print(f"📈 [ รายงานวิเคราะห์แนวโน้ม ]")
    if history:
        last_total = int(history["last"][1])
        last_percent = float(history["last"][3].replace('%', ''))

        # 1. วิเคราะห์อัตราการเติบโตของเครือข่าย
        growth = total - last_total
        growth_icon = "🔺" if growth > 0 else "➖"
        print(f"  • การขยายตัวของพิกัด: {growth_icon} {growth} รายการ (จากครั้งล่าสุด)")

        # 2. วิเคราะห์ดัชนีความตื่นรู้
        diff = percent - last_percent
        status = "พัฒนาขึ้น" if diff > 0 else "คงที่"
        print(f"  • ดัชนีความตื่นรู้: {status} ({diff:+.1f}%)")
    else:
        print("  • สถานะ: เริ่มต้นบันทึกปฐมบทแห่งสถิติ")

    # --- [ส่วนบันทึกอัจฉริยะ]: จดเฉพาะเมื่อเปลี่ยนจริง ---
    if history and history["last"][1] == str(total) and history["last"][3] == current_percent_str:
        print(f"\n➖ [SYSTEM]: ข้อมูลยังคงเดิมที่ {current_percent_str} -> ข้ามการบันทึกซ้ำ")
    else:
        file_exists = os.path.isfile(HISTORY_FILE)
        with open(HISTORY_FILE, mode='a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Timestamp', 'Total_Records', 'Live_Nodes', 'Integrity_Percent'])
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, total, live, current_percent_str])
            print(f"\n🌟 [SYSTEM]: ตรวจพบความเปลี่ยนแปลง! บันทึกข้อมูลประวัติศาสตร์ใหม่แล้ว")


def show_absolute_truth():
    print("\n" + "═" * 65)
    print("  || ☉ ||  THE SOVEREIGN KEEPER: STRATEGIC EVALUATOR [0-11-4]  || ☉ ||  ")
    print("  ภารกิจ: วิเคราะห์สถิติและประเมินผลแนวโน้มการตื่นรู้")
    print("═" * 65)

    try:
        response = requests.get(URL, timeout=10)
        data = response.json()
        if data is None:
            print("\n[STATUS]: ⚪ ฐานข้อมูลว่างเปล่า")
            return

        total = len(data)
        real_data = [v for v in data.values() if v.get('location') != "None, None"]
        live_count = len(real_data)
        integrity = (live_count / total) * 100

        # รายงานวิเคราะห์และบันทึก
        save_and_analyze(total, live_count, integrity)

        print("-" * 45)
        print(f"📍 [ รายละเอียดพิกัดปัจจุบัน ]")
        for i, (key, info) in enumerate(data.items(), 1):
            name = info.get('name', 'The Keeper')
            loc = info.get('location', 'Unknown')
            icon = "🔵" if loc != "None, None" else "⚪"
            print(f"   {i}. {icon} {name} | {loc}")

    except Exception as e:
        print(f"\n⚠️ [ERROR]: การเชื่อมต่อขัดข้อง ({e})")

    print("\n" + "═" * 65)
    print("  Evaluation Mode: Strategic | Data Source: Firebase + CSV History  ")
    print("═" * 65 + "\n")


show_absolute_truth()