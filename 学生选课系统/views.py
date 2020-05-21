"""
项目中的视图模块
    管理员菜单：show_manager_*****()
    学员菜单：show_student_****()
    普通菜单：show_****()
"""
import model
import utils
import time


class Views:
    """视图模块"""
    # 记录登录用户
    login_user = None
    # 登录菜单跳转
    login_dict = {"1": "cls.login(1)", "2": "cls.login(2)", "3": "cls.register()", "4": "exit_system()"}
    # 管理员菜单跳转
    manager_index_dict = {"1": "cls.chg_passwd()", "2": "cls.perfect_information()",
                          "3": "cls.show_manager_student_info()",
                          "4": "cls.show_manager_course_info()",
                          "5": "cls.show_manager_course_add()",
                          "6": "cls.show_login()",
                          "7": "utils.exit_system()"}
    # 学员菜单跳转
    student_index_dict = {"1": "cls.chg_passwd()",
                          "2": "cls.perfect_information()",
                          "3": "cls.show_student_query_select_courses()",
                          "4": "cls.show_student_query_selected_courses()",
                          "5": "cls.show_login()",
                          "6": "utils.exit_system()"}
    # 完善用户资料 字典
    perfect_information_dict = {"姓名": "real_name", "性别": "gender", "年龄": "age",
                                "邮箱": "email", "手机": "phone"}

    @classmethod
    def show_login(cls):
        """登录菜单展示"""
        print("        中公-学员选课系统")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("          1、管理员登录")
        print("          2、会员登录")
        print("          3、会员注册")
        print("          4、退出系统")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # 用户输入选项：
        choice = input("请输入您的选项：")
        res = cls.login_dict.get(choice, "cls.show_login()")
        return eval(res)

    @classmethod
    def login(cls, login_type):
        """登录方法"""
        # 提示用户输入登录信息
        username = input("请输入账号：").strip()
        password = input("请输入密码：").strip()

        # 查询用户数据：login_type是个方法的参数，调用的时候传递过来的
        if login_type == 1:
            user = model.Manager.query_username_password(username, password)
        elif login_type == 2:
            user = model.Student.query_username_password(username, password)

        # 根据最终结果，跳转到不同的界面
        if user:  # if None: 不能执行后续代码
            input("登录成功，按任意键继续")
            cls.login_user = user
            # if user.role == "管理员":
            #     return cls.show_manager_index()
            # else:
            #     return cls.show_student_index()
            # 扩展：python中的三元运算符
            # 语法： 结果1  if 条件 else 结果2：如果条件为True返回结果1，否则返回结果2
            return cls.show_manager_index() if user.role == "管理员" else cls.show_student_index()

        input("账号或者密码有误，请重新登录")
        return cls.show_login()

    @classmethod
    def register(cls):
        """注册方法"""
        # 提示用户输入注册数据
        username = input("请输入注册账号：").strip()
        password = input("请输入注册密码：").strip()
        confirm = input("请确认注册密码：").strip()

        # 账号验证
        if model.Student.query_username(username):
            print("账号已经存在，请重新注册")
            return cls.show_login()

        # 验证密码
        if password != confirm:
            print("两次密码输入不一致，请重新注册。")
            return cls.show_login()
        # 创建对象，保存数据
        student = model.Student(username, password)
        student.save()
        # 跳转回登录菜单
        return cls.show_login()

    @classmethod
    def show_manager_index(cls):
        """展示管理员首页"""
        print("       中公-学生选课系统[管]")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("          1、修改登录密码")
        print("          2、完善个人资料")
        print("          3、查看学员")
        print("          4、查看课程")
        print("          5、添加课程")
        print("          6、返回登录菜单")
        print("          7、退出系统")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # 输入选项
        choice = input("请输入您的选项：")
        oper = cls.manager_index_dict.get(choice, "cls.show_manager_index()")
        return eval(oper)

    @classmethod
    def show_student_index(cls):
        """展示学员首页"""
        print("        中公-学员选课系统[学]")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("           1、修改登录密码")
        print("           2、完善个人资料")
        print("           3、查看可选课程")
        print("           4、查看已选课程")
        print("           5、返回登录菜单")
        print("           6、退出系统")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # 用户输入选项
        choice = input("请输入您的选项：")
        opera = cls.student_index_dict.get(choice, "cls.show_student_index()")
        return eval(opera)

    @classmethod
    def chg_passwd(cls):
        """修改用户登录密码"""
        old_passwd = input("请输入您的原密码：").strip()
        if old_passwd != cls.login_user.password:
            print("原密码输入有误，请重新登录")
        else:
            passwd = input("请输入新密码：")
            confirm = input("请确认新密码：")
            if passwd != confirm:
                print("两次密码输入不一致，请重新登录.")
            else:
                # 修改登录密码
                cls.login_user.password = passwd
                print("密码修改完成，重新登录")
        return cls.show_login()

    @classmethod
    def perfect_information(cls):
        """完善用户资料"""
        # 1、展示用户信息
        cls.show_use_info()

        # 2、提示需要完善的资料
        print("\n可修改资料名称如下：")
        for attr in cls.perfect_information_dict.keys():
            print(f"{attr}、", end="")
        choice = input("请输入您要修改的个人信息：") # 姓名
        attr_name = cls.perfect_information_dict.get(choice)

        # 3、完善资料，修改属性数据
        if attr_name != None:  # 姓名--> real_name
            value = input("请输入您修改后的资料：")
            # 反射方法  setattr(对象, "real_name", "大牧")
            setattr(cls.login_user, attr_name, value)
            input("资料完善成功，按任意键返回首页")
            if cls.login_user.role == "管理员":
                return cls.show_manager_index()
            else:
                return cls.show_student_index()
        else:
            res = input("没有这个属性，按任意键重新操作(Q返回主菜单)")
            if res.upper() == "Q":
                if cls.login_user.role == "管理员":
                    return cls.show_manager_index()
                else:
                    return cls.show_student_index()
            return cls.perfect_information()

    @classmethod
    def show_use_info(cls):
        """查看个人信息"""
        print(f"用户{cls.login_user.username}的用户信息  ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"  账号：{cls.login_user.username}[不可改]")
        print(f"  姓名：{cls.login_user.real_name}[可改]")
        print(f"  性别：{cls.login_user.gender}[可改]")
        print(f"  年龄：{cls.login_user.age}[可改]")
        print(f"  邮箱：{cls.login_user.email}[可改]")
        print(f"  手机：{cls.login_user.phone}[可改]")
        print(f"  角色：{cls.login_user.role}[不可改]")
        print("~~~~~~~~~~~~~~~~~~~~~~~~")

    @classmethod
    def show_manager_student_info(cls):
        """管理员查看所有学员信息"""
        # 得到保存所有学员的字典
        students = model.Student.query_all()
        print("账号\t姓名\t性别\t年龄")
        # 遍历字典中的所有value数据: Student类型的对象
        for stu in students.values():
            print(f"{stu.username}\t{stu.real_name}\t{stu.gender}\t{stu.age}")

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        input("学员信息展示完成，按任意键返回首页")
        return cls.show_manager_index()

    @classmethod
    def show_manager_course_info(cls):
        """查看所有课程信息"""
        cls.show_course_info()
        return cls.show_manager_index()

    @classmethod
    def show_manager_course_add(cls):
        """增加课程的方法"""
        # 1、录入课程信息
        name = input("请输入课程名称:")
        if model.Course.query_name(name):
            input("课程已经存在，请重新输入课程名称")
            return cls.show_manager_course_add()
        teacher = input("清输入授课老师:")
        times = input("请输入课时:")
        score = input("请输入学分:")
        maxsize = input("请输入选择人数上限:")
        remark = input("请输入课程描述:")

        # 3、新增课程
        course = model.Course(name, teacher, times, score, maxsize, remark)
        course.save()

        input("课程添加完成，按任意键返回首页")
        return cls.show_manager_index()

    @classmethod
    def show_student_query_select_courses(cls):
        """查看可选课程:展示所有课程"""
        cls.show_course_info()
        print("---------------课程信息展示完毕")
        # 开始选课
        name = input("请输入课程名称，选择要学习的课程：")
        if name in cls.login_user.selected_course:
            input("课程已经包含在已选中，请重新选择")
            return cls.show_student_query_select_courses()
        else:
            cls.login_user.selected_course[name] = model.Course.query_name(name)
            input("课程已经选好，按任意键返回首页")  # 求助：选择课程，字典属性~已选课程；key课程名称，value？
            return cls.show_student_index()

    @classmethod
    def show_student_query_selected_courses(cls):
        """查看已选课程"""
        # 得到所有的课程数据字典
        print(">>>>> 下面是您已经选择的课程：")
        courses = cls.login_user.selected_course
        print("名称\t授课老师\t学分\t课程描述")
        # 遍历所有的课程
        for cur in courses.values():
            print(f"{cur.name}\t{cur.teacher}\t{cur.score}\t{cur.remark}")

        # 学习课程
        name = input("请输入您要学习的课程名称：")
        return cls.show_student_course_study(name)

    @classmethod
    def show_student_course_study(cls, name):
        """学习课程的行为"""
        # 1、获取要学习的课程
        course = cls.login_user.selected_course.get(name)
        if course.times > 0:
            # 2、学习过程
            for i in [1,2,3]:
                time.sleep(1)
                print(f"正在学习中{i}....")

            # 3、学习完之后修改属性
            # TODO 课时修改存在BUG~~解决方案：深浅拷贝
            print("学习完成")
            print(f"课程名称{course.name}，待学课程：{course.times}")
            course.times -= 1
            print(f"完成本次学习, 剩余学习课时：{course.times}")
            if course.times <= 0:
                # 学习完成，增加学分
                cls.login_user.score += course.score

            input("学习完成，按任意键返回学员首页")
        else:
            input("该课程已经学习完成。")
        return cls.show_student_index()

    @classmethod
    def show_course_info(cls):
        """展示所有课程：公共方法"""
        # 得到所有的课程数据字典
        courses = model.Course.query_all()
        print("名称\t授课老师\t学分\t课程描述")
        # 遍历所有的课程
        for cur in courses.values():
            print(f"{cur.name}\t{cur.teacher}\t{cur.score}\t{cur.remark}")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
