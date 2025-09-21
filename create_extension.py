import os
import sys
import argparse
import json

def get_user_input():
    """
    获取用户输入的扩展信息
    """
    print("请输入扩展的基本信息（直接回车使用默认值）")
    
    name = input("扩展名称 (默认: 使用目录名称): ").strip()
    
    version = input("版本号 (默认: 1.0.0): ").strip()
    if not version:
        version = "1.0.0"
    
    description = input("扩展描述 (默认: A sample browser extension): ").strip()
    if not description:
        description = "A sample browser extension"
    
    return name, version, description

def create_extension_structure(directory_name, name, version, description):
    """
    创建浏览器扩展的基本目录结构
    """
    # 如果没有输入扩展名称，使用目录名称
    if not name:
        name = os.path.basename(directory_name)
    
    # 创建主目录
    try:
        os.makedirs(directory_name)
        print(f"✓ 创建目录: {directory_name}")
    except FileExistsError:
        print(f"✗ 目录 {directory_name} 已存在")
        return False
    except Exception as e:
        print(f"✗ 创建目录失败: {e}")
        return False
    
    # 创建 options 目录
    options_dir = os.path.join(directory_name, "options")
    try:
        os.makedirs(options_dir)
        print(f"✓ 创建目录: {options_dir}")
    except Exception as e:
        print(f"✗ 创建 options 目录失败: {e}")
        return False
    
    # 创建 content 目录
    content_dir = os.path.join(directory_name, "content")
    try:
        os.makedirs(content_dir)
        print(f"✓ 创建目录: {content_dir}")
    except Exception as e:
        print(f"✗ 创建 content 目录失败: {e}")
        return False
    
    # 创建 background 目录
    background_dir = os.path.join(directory_name, "background")
    try:
        os.makedirs(background_dir)
        print(f"✓ 创建目录: {background_dir}")
    except Exception as e:
        print(f"✗ 创建 background 目录失败: {e}")
        return False
    
    # 创建 icon 目录（空目录）
    icon_dir = os.path.join(directory_name, "icon")
    try:
        os.makedirs(icon_dir)
        print(f"✓ 创建目录: {icon_dir}")
    except Exception as e:
        print(f"✗ 创建 icon 目录失败: {e}")
        return False
    
    # 创建 manifest.json 文件（包含用户输入的扩展名称）
    manifest_content = {
        "manifest_version": 3,
        "name": name,
        "version": version,
        "description": description,
        "icons": {
            # 图标配置项留空，用户可以根据需要添加
        },
        "action": {
            "default_popup": "options/popup.html"
        },
        "permissions": ["activeTab", "storage"],
        "content_scripts": [
            {
                "matches": ["<all_urls>"],
                "js": ["content/content.js"]
            }
        ],
        "background": {
            "service_worker": "background/background.js"
        },
        "options_page": "options/popup.html"
    }
    
    manifest_path = os.path.join(directory_name, "manifest.json")
    try:
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_content, f, indent=2, ensure_ascii=False)
        print(f"✓ 创建文件: {manifest_path}")
        print(f"  - 名称: {name}")
        print(f"  - 版本: {version}")
        print(f"  - 描述: {description}")
    except Exception as e:
        print(f"✗ 创建 manifest.json 失败: {e}")
        return False
    
    # 创建 content.js 文件（在 content 目录下）
    content_js_content = """// content.js - 内容脚本
console.log("Content script loaded");

// 示例：修改页面背景色
document.addEventListener('DOMContentLoaded', function() {
    // document.body.style.backgroundColor = '#f0f0f0';
});
"""
    
    content_js_path = os.path.join(content_dir, "content.js")
    try:
        with open(content_js_path, 'w', encoding='utf-8') as f:
            f.write(content_js_content)
        print(f"✓ 创建文件: {content_js_path}")
    except Exception as e:
        print(f"✗ 创建 content.js 失败: {e}")
        return False
    
    # 创建 background.js 文件（在 background 目录下）
    background_js_content = """// background.js - 后台脚本
console.log("Background script loaded");

// 示例：监听浏览器事件
chrome.runtime.onInstalled.addListener(() => {
    console.log("Extension installed");
});

// 示例消息监听
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log("Message received:", request);
});
"""
    
    background_js_path = os.path.join(background_dir, "background.js")
    try:
        with open(background_js_path, 'w', encoding='utf-8') as f:
            f.write(background_js_content)
        print(f"✓ 创建文件: {background_js_path}")
    except Exception as e:
        print(f"✗ 创建 background.js 失败: {e}")
        return False
    
    # 创建 popup.html 文件（使用用户输入的扩展名称）
    popup_html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{name}</title>
    <link rel="stylesheet" href="popup.css">
</head>
<body>
    <div class="popup-container">
        <h1>{name} v{version}</h1>
        <p>{description}</p>
        <button id="clickMe">Click Me</button>
    </div>
    <script src="popup.js"></script>
</body>
</html>
"""
    
    popup_html_path = os.path.join(options_dir, "popup.html")
    try:
        with open(popup_html_path, 'w', encoding='utf-8') as f:
            f.write(popup_html_content)
        print(f"✓ 创建文件: {popup_html_path}")
    except Exception as e:
        print(f"✗ 创建 popup.html 失败: {e}")
        return False
    
    # 创建 popup.js 文件
    popup_js_content = """// popup.js - 弹出窗口的JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log("Popup script loaded");
    
    const button = document.getElementById('clickMe');
    if (button) {
        button.addEventListener('click', function() {
            alert('Button clicked!');
            
            // 发送消息到背景脚本
            chrome.runtime.sendMessage({action: "buttonClicked", data: "Hello from popup"});
        });
    }
    
    // 从存储中获取数据
    chrome.storage.local.get(['settings'], function(result) {
        console.log('Settings loaded:', result.settings);
    });
});
"""
    
    popup_js_path = os.path.join(options_dir, "popup.js")
    try:
        with open(popup_js_path, 'w', encoding='utf-8') as f:
            f.write(popup_js_content)
        print(f"✓ 创建文件: {popup_js_path}")
    except Exception as e:
        print(f"✗ 创建 popup.js 失败: {e}")
        return False
    
    # 创建 popup.css 文件
    popup_css_content = """/* popup.css - 弹出窗口的样式 */
body {
    width: 300px;
    height: 200px;
    margin: 0;
    padding: 15px;
    font-family: Arial, sans-serif;
}

.popup-container {
    text-align: center;
}

h1 {
    color: #333;
    font-size: 18px;
    margin-bottom: 10px;
}

p {
    color: #666;
    font-size: 14px;
    margin-bottom: 15px;
}

button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

button:hover {
    background-color: #0056b3;
}
"""
    
    popup_css_path = os.path.join(options_dir, "popup.css")
    try:
        with open(popup_css_path, 'w', encoding='utf-8') as f:
            f.write(popup_css_content)
        print(f"✓ 创建文件: {popup_css_path}")
    except Exception as e:
        print(f"✗ 创建 popup.css 失败: {e}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='创建浏览器扩展的基本目录结构')
    parser.add_argument('directory', help='要创建的目录名称')
    
    args = parser.parse_args()
    
    if not args.directory:
        print("错误：请提供目录名称")
        parser.print_help()
        sys.exit(1)
    
    print(f"开始创建扩展目录结构: {args.directory}")
    print("-" * 50)
    
    # 获取用户输入
    name, version, description = get_user_input()
    print("-" * 50)
    
    success = create_extension_structure(args.directory, name, version, description)
    
    print("-" * 50)
    if success:
        print("✓ 扩展目录结构创建完成！")
        print(f"目录位置: {os.path.abspath(args.directory)}")
        print("\n📁 目录结构:")
        print(f"{args.directory}/")
        print("├── icon/")
        print("├── options/")
        print("│   ├── popup.html")
        print("│   ├── popup.js")
        print("│   └── popup.css")
        print("├── content/")
        print("│   └── content.js")
        print("├── background/")
        print("│   └── background.js")
        print("└── manifest.json")
    else:
        print("✗ 创建过程中出现错误")
        sys.exit(1)

if __name__ == "__main__":
    main()