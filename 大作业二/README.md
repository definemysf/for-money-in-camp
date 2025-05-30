# 植物养护助手 Plant Care Assistant

## 简介

**植物养护助手**是一个命令行工具，旨在帮助用户根据家中现有植物的种类和当前季节，获得科学、个性化的植物养护建议。通过输入植物名称，程序会自动推断当前季节，并输出每种植物的浇水频率、光照需求和养护小贴士，助你轻松养护绿植。

## 功能特点

- 支持多种常见家养植物（如多肉、发财树、绿萝等）的养护建议
- 根据当前月份自动判断季节，推送对应时令养护要点
- 输出内容包括浇水频率、光照条件、养护小贴士
- 易于扩展，便于添加新植物及其养护知识

## 使用方法

1. **准备环境**
    
    - 需安装 Python 3.x
    - 将 `main.py` 文件保存到本地
    
2. **运行程序**
    ```bash
    python main.py
    ```

3. **按提示操作**
    - 程序会展示支持的植物类型
    - 按要求输入你家中养护的植物名称（多个植物请用空格分隔）
    - 程序会自动判断当前季节，并输出每种植物的专属养护建议
    - 并结合当前的节气 进行判断

## 示例

```
🌱 欢迎使用植物养护助手！🌱
😀当前时间：2025-05-26 16:01:32
====================================
🌱支持的植物有： 多肉、发财树、绿萝、吊兰、虎皮兰、君子兰、富贵竹、文竹、龟背竹
🌱请输入你家中的植物名称，用空格分隔（如 多肉 绿萝 君子兰 文竹）：
多肉 吊兰 发财树
请选择您的地区：
1. 东北
2. 华北
3. 华中
4. 华南
5. 西北
6. 西南
7. 中原
输入序号选择地区（如 1）：3
您选择的地区是：华中


当前季节推断为：spring（5月）
节气信息：当前处于【小满】与【芒种】之间（下个节气：芒种，日期：06月05日)

【多肉】养护建议：
  地区：华中
  浇水：每2周一次
  光照：充足阳光
  小贴士：避免积水
------------------------------
【吊兰】养护建议：
  地区：华中
  浇水：每周2次
  光照：散射光
  小贴士：保持盆土微湿
------------------------------
【发财树】养护建议：
  地区：华中
  浇水：每周一次
  光照：明亮散射光
  小贴士：保持土壤湿润
```

## 扩展与自定义

- 想要支持更多植物？可在 `main.py` 文件中的 `plant_care_guide` 字典内新增植物及其养护数据。
- 想实现更多功能（如天气API接入、养护提醒、GUI界面等），欢迎自行扩展，也可向作者反馈建议。联系邮箱294644349@qq.com

## 许可证

本项目遵循 MIT License，欢迎学习和二次开发。

---

**让植物养护更科学，让生活更美好！**