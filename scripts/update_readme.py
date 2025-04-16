import requests
from datetime import datetime
import os

HEADERS = {"Authorization": f"token {os.environ['GH_TOKEN']}"}

def get_following_activity():
    # 获取关注用户的公开活动
    events = []
    users = requests.get("https://api.github.com/users/tomnkey/following", headers=HEADERS).json()
    for user in users[:5]:  # 取前5个关注用户
        events += requests.get(f"https://api.github.com/users/{user['login']}/events/public", headers=HEADERS).json()
    return sorted(events, key=lambda x: x['created_at'], reverse=True)[:10]

def get_starred_activity():
    # 获取star项目的最近动态
    stars = requests.get("https://api.github.com/users/tomnkey/starred", headers=HEADERS).json()
    return sorted(stars, key=lambda x: x['pushed_at'], reverse=True)[:5]

def update_readme():
    # 生成动态内容
    new_content = "## 🚀 关注动态\n"
    for event in get_following_activity():
        new_content += f"- [{event['type']}] {event['actor']['login']} - {event['repo']['name']}\n"

    new_content += "\n## 🌟 Star动态\n"
    for star in get_starred_activity():
        new_content += f"- [{star['name']}] 最后更新：{datetime.strptime(star['pushed_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M')}\n"

    # 替换README中的动态区块
    with open('README.md', 'r') as f:
        readme = f.read()

    updated_readme = readme.replace('<!--DYNAMIC-->', f'<!--DYNAMIC-->\n{new_content}')

    with open('README.md', 'w') as f:
        f.write(updated_readme)
