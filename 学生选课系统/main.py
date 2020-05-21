"""
程序运行入口
    import 绝对导入
        Builtins解释器内建路径 查询
        环境变量PYTHONPATH 查询
        当前路径 查询【pycharm工具通过明确的规范，查询当前文件夹】
        鼠标右键选择文件夹-> Mark Directory as -> Sources Root(源代码目录)
    已完成的功能
        1、会员注册
        2、会员登录
        3、管理员自动添加
        4、管理员登录
    待完成的功能
        修改登录密码
        完善个人资料
        1、管理员
            查看学员
            查看课程
            删除课程
        2、学员
            查看可选课程
            可看已选课程
            学习课程
    需要完善的细节
        密码加密
        ....
"""
import views
import utils

# 程序启动，初始化数据
utils.init_manager()

# 展示登录菜单
views.Views.show_login()
