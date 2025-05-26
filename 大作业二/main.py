import datetime
import importlib.util
import os

def import_plant_data():
    file_path = os.path.join(os.path.dirname(__file__), "plant_data.py")
    spec = importlib.util.spec_from_file_location("plant_data", file_path)
    plant_data = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plant_data)
    return plant_data

def get_season(month):
    if month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "autumn"
    else:
        return "winter"

def get_solar_term_info(today, solar_terms_2025):
    solar_list = []
    for term in solar_terms_2025:
        name, date_info = term
        if len(date_info) == 2:
            y = today.year
            m, d = date_info
        else:
            y, m, d = date_info
        solar_list.append((name, datetime.date(y, m, d)))
    solar_list = sorted(solar_list, key=lambda x: x[1])
    prev_term = solar_list[-1]
    for term in solar_list:
        if today < term[1]:
            next_term = term
            break
        prev_term = term
    return f"当前处于【{prev_term[0]}】与【{next_term[0]}】之间（下个节气：{next_term[0]}，日期：{next_term[1].strftime('%m月%d日')})"

def choose_region(region_guide):
    print("请选择您的地区：")
    for idx, region in enumerate(region_guide.keys()):
        print(f"{idx + 1}. {region}")
    choice = input("输入序号选择地区（如 1）：")
    try:
        region = list(region_guide.keys())[int(choice) - 1]
        print(f"您选择的地区是：{region}\n")
        return region
    except Exception:
        print("输入有误，默认选择华北。")
        return "华北"

def main():
    plant_data = import_plant_data()
    plant_care_guide = plant_data.plant_care_guide
    region_guide = plant_data.region_guide
    solar_terms_2025 = plant_data.solar_terms_2025

    print("="*36)
    print("🌱 欢迎使用植物养护助手！🌱")
    print(f"😀当前时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*36)
    print("🌱支持的植物有：", "、".join(plant_care_guide.keys()))
    plants = input("🌱请输入你家中的植物名称，用空格分隔（如 多肉 绿萝 君子兰 文竹）：\n").split()
    region = choose_region(region_guide)
    today = datetime.date.today()
    season = get_season(today.month)

    # 节气信息
    solar_term_info = get_solar_term_info(today, solar_terms_2025)
    print(f"\n当前季节推断为：{season}（{today.month}月）")
    print(f"节气信息：{solar_term_info}\n")

    for plant in plants:
        if plant in plant_care_guide:
            advice = plant_care_guide[plant][season]
            print(f"【{plant}】养护建议：")
            print(f"  地区：{region}")
            print(f"  浇水：{advice['water']}")
            print(f"  光照：{advice['sun']}")
            print(f"  小贴士：{advice['tip']}")
            print("-"*30)
        else:
            print(f"暂未收录“{plant}”的养护知识，欢迎补充！\n")

if __name__ == "__main__":
    main()