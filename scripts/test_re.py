import re

edu_dict = {
            'primary': '小学',
            'junior': '初中',
            'senior': '高中',
        }
subject_dict = {
    'math': '数学',
    'biology': '生物',
    'chemistry': '化学',
    'chinese': '语文',
    'english': '英语',
    'geography': '地理',
    'physics': '物理',
    'politics': '政治',
    'history': '历史',
}
e2 = {'小学': 'primary', '初中': 'junior', '高中': 'senior'}
s2 = {'数学': 'math', '生物': 'biology', '化学': 'chemistry', '语文': 'chinese', '英语': 'english', '地理': 'geography', '物理': 'physics', '政治': 'politics', '历史': 'history'}


def cn2en(s):
    e2 = {'小学': 'primary', '初中': 'junior', '高中': 'senior'}
    s2 = {'数学': 'math', '生物': 'biology', '化学': 'chemistry', '语文': 'chinese', '英语': 'english', '地理': 'geography',
          '物理': 'physics', '政治': 'politics', '历史': 'history'}
    s0 = s[:2]
    s1 = s[2:]
    f0 = e2[s0]
    f1 = s2[s1]
    return f0, f1

# r = cn2en('初中物理')
# print(r)
ans = '\\(\\left\\{ {\\begin{array}{*{20}{l}}{x + y - 2 = 0} \\\\{x + 2y - 3 = 0} \\end{array}} \\right.\\)'
ans = re.sub(r'\\\\{', r'\\\\ {', ans)
ans = re.sub(r'(?<!\\left)\\{', r'\\left\\{', ans)
print(ans)