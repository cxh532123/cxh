"""
项目中的工具类型
"""
import time

def init_manager():
    """初始化管理员数据"""
    # 创建一个默认管理员对象
    import model
    manager = model.Manager("admin", "admin")
    manager.save()


def exit_system():
    """退出系统"""
    for i in [3,2,1]:
        print(f"系统将在{i}秒后退出，请注意保存好个人数据")
    exit(1)