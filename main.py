import os
import time
import shutil


def sort_by_time(file_path):
    # 按时间顺序排序文件
    files = os.listdir(file_path)
    if not files:
        return
    else:
        files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        return files


def rm_not_gif(gif_all):
    # 在列表内，移除不是gif的项
    del_not_gif = []
    for i in range(len(gif_all)):
        if gif_all[i][-4:] != ".gif":
            del_not_gif.append(gif_all[i])
    for i in del_not_gif:
        gif_all.remove(i)

# 路径
wechat_file = r"C:\Users\bbsa2\Documents\WeChat Files"
user_id = os.listdir(wechat_file)
output_path = os.path.expanduser("~\\Desktop")  # 保存至桌面

# 获取用户列表，删掉无关文件夹
try:
    user_id.remove('All Users')
    user_id.remove('Applet')
    user_id.remove('WMPF')
except:
    if len(user_id) != 0:
        pass
    else:
        print("WeChat File不完整。")

# 选择单用户
if len(user_id) > 1:
    print("Wechat File包含的多用户列表如下：")
    for i, element in enumerate(user_id):
        print("{}. {}".format(i + 1, element))
    choose_i = int(input("选择当前用户，只允许输入数字："))
    user_id = user_id[choose_i - 1]
    print("选择的用户是：", user_id)

# 获取GIF地址
gif_dir = os.path.join(wechat_file, user_id[0], "FileStorage", "File",
                       time.strftime("%Y-%m", time.localtime()))  # gif文件夹地址
gif_all = os.listdir(gif_dir)  # gif按时间顺序排序的文件名列表，不带路径
rm_not_gif(gif_all)  # 移除非gif项

for i in gif_all:  # 移除所有gif，防止干扰
    os.remove(os.path.join(gif_dir, i))

f = open(os.path.join(gif_dir, "wxezGIF.gif"), "w")  # 创建空gif，防止程序错误
f.close()

print("等待用户操作...")

while 1:
    # b:before, a:after
    time.sleep(0.1)
    len_b = len(gif_all)
    len_a = len(os.listdir(gif_dir))
    if len_a != len_b:
        gif_all = sort_by_time(gif_dir)  # 没有考虑月末交接的情况，可能在特殊情况下会出错。
        # 只对大于1MB的gif有效
        if (os.path.getsize(os.path.join(gif_dir, gif_all[-1])) / 1024 / 1024) > 1:
            output_file = os.path.join(gif_dir, gif_all[-1])
            print(output_file)
            break

shutil.copy(output_file, output_path)
print("已复制到指定文件夹。")
