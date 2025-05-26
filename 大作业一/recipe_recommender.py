import os
import difflib

def read_recipes(file_path):
    # 读取菜谱数据，返回列表
    recipes = []
    if not os.path.exists(file_path):
        print(f"未找到菜谱文件: {file_path}")
        return recipes
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    blocks = [block.strip() for block in content.split('\n\n') if block.strip()]
    for block in blocks:
        lines = block.split('\n')
        recipe = {}
        for line in lines:
            if line.startswith("菜名:"):
                recipe["name"] = line.replace("菜名:", "").strip()
            elif line.startswith("菜系:"):
                recipe["cuisine"] = line.replace("菜系:", "").strip()
            elif line.startswith("用料:"):
                recipe["ingredients"] = [x.strip() for x in line.replace("用料:", "").strip().split(",")]
            elif line.startswith("制作过程:"):
                recipe["steps"] = []
            elif "steps" in recipe and line and not line.startswith("制作过程:"):
                recipe["steps"].append(line.strip())
        if "steps" in recipe:
            recipe["steps"] = "\n".join(recipe["steps"])
        recipes.append(recipe)
    return recipes

def fuzzy_find_recipe(name, recipe_list):
    # 支持模糊查找菜名
    names = [r["name"] for r in recipe_list]
    matches = difflib.get_close_matches(name, names, n=1, cutoff=0.5)
    if matches:
        for r in recipe_list:
            if r["name"] == matches[0]:
                return r
    return None

def main():
    print("=== 菜谱推荐系统 ===")
    try:
        # 1. 输入冰箱里有的调味料
        condiments = input("请输入冰箱里有的调味料（用空格分隔，如 盐 酱油 糖 花椒  姜, 蒜, 盐, 酱油, 料酒 当然了谁做饭没有调料呢 所以默认都有）：\n").split()
        # 2. 输出现有食材
        ingredients = ["鸡蛋", "米", "面","面条","大米","料酒","油", "糖", "盐", "酱油", "花椒", "姜", "蒜"]
        more = input("🍆🌶🥔请输入冰箱里除调味料外的其它食材（用空格分隔，如 西红柿 青椒 豆腐 茄子 干辣椒 鸡腿肉 鲈鱼 包菜 馕 酸菜 草鱼 咖喱块 葡萄干 鸡肉 猪肉 牛肉 土豆 黄瓜 羊肉 胡萝卜 洋葱 ）：\n🍆🌶🥔当然我不会告诉你Ctrl+Shift+C可以复制我上面的Ctrl+Shift+V可以粘贴\n").split()
        if more:
            ingredients += [item for item in more if item]
        print(f"🍆🌶🥔冰箱现有食材：{'、'.join(ingredients)}")
        # 3. 输入想要品尝的菜系
        wanted_cuisine = input("🥗请输入你想要品尝的菜系（如 家常、川菜、粤菜、新疆菜，留空为不限）：\n").strip()
        # 4. 自动推荐菜品
        recipes = read_recipes("recipes.txt")
        if not recipes:
            print("菜谱数据为空，请检查 recipes.txt 文件。")
            return
        can_cook = []
        almost_cook = []
        for recipe in recipes:
            if wanted_cuisine and recipe.get("cuisine") != wanted_cuisine:
                continue
            needed = set(recipe.get("ingredients", []))
            owned = set(ingredients + condiments)
            missing = needed - owned
            if not missing:
                can_cook.append(recipe)
            elif len(missing) <= 2:
                almost_cook.append((recipe, missing))
        # 输出推荐
        if can_cook:
            print("\n🥗🍽你可以做以下菜品：")
            for idx, recipe in enumerate(can_cook, 1):
                print(f"{idx}. {recipe['name']}（{recipe['cuisine']}）")
        else:
            print("\n很抱歉，当前食材无法做出该菜系的菜品。")
        if almost_cook:
            print("\n❤只差一点就能做的菜（缺少食材）：")
            for idx, (recipe, missing) in enumerate(almost_cook, 1):
                print(f"{idx}. {recipe['name']}（{recipe['cuisine']}，还缺：{', '.join(missing)}）")
        if not can_cook:
            print("✨建议补充缺少的食材后再试试哦！")
            return
        # 5. 输入菜名输出制作过程（支持模糊匹配）
        chosen = input("\n✨请输入你想了解制作过程的菜名（支持模糊匹配）：\n").strip()
        found = next((r for r in can_cook if r["name"] == chosen), None)
        if not found:
            found = fuzzy_find_recipe(chosen, can_cook)
        if found:
            print(f"\n【{found['name']}】制作过程：\n{found['steps']}")
        else:
            print("未找到该菜名，或你当前条件无法制作该菜。请检查输入是否有误。")
    except Exception as e:
        print(f"程序运行时发生错误：{e}")
        print("请检查输入和数据文件格式。")

if __name__ == "__main__":
    main()