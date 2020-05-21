"""
项目中的数据模型
    声明项目中的数据类型的：用户 ->[管理员、学员]、课程

    用户类型[学员]
        属性：
            __init__()中初始化数据

        实例方法：操作当前对象，需要访问实例数据，所以定义成实例方法
            save(self)：保存当前对象数据

        类方法：不需要访问实例数据，为了方便调用执行，声明成类 方法
            query_all(cls)：查询所有的学员数据
"""
import data
import utils


class User:
    """用户类型"""
    def __init__(self, username, password, real_name, gender, age,
                 email, phone, role):
        self.username = username
        self.password = password
        self.real_name = real_name
        self.gender = gender
        self.age = age
        self.email = email
        self.phone = phone
        self.role = role

    @classmethod
    def query_username_password(cls, username, password):
        """根据账号+密码查询用户的方法"""
        pass


class Manager(User):
    """管理员"""

    def __init__(self, username, password, real_name="待完善", gender="待完善",
                 age="待完善", email="待完善", phone="待完善", score=0):
        super().__init__(username, password, real_name, gender, age, email, phone, role="管理员")

    def save(self):
        """保存管理员对象数据的方法"""
        data.Database.manager_dict[self.username] = self

    @classmethod
    def query_username_password(cls, username, password):
        """根据账号+密码查询学员"""
        if username in data.Database.manager_dict:
            user = data.Database.manager_dict.get(username)
            if password == user.password:
                # 查询到用户
                print("查询到符合账号+密码的用户")
                return user
        print("没有查询到符合账号+密码的用户")
        return None


class Student(User):
    """学员类型"""

    def __init__(self, username, password, real_name="待完善", gender="待完善",
                 age="待完善", email="待完善", phone="待完善", score=0):
        super().__init__(username, password, real_name, gender, age, email, phone, role="学员")
        self.score = score  # 学分
        self.selected_course = dict()  # 已选课程字典

    def save(self):
        """保存学员对象数据的方法"""
        data.Database.student_dict[self.username] = self

    @classmethod
    def query_username(cls, username):
        """根据账号查询用户是否存在"""
        if username in data.Database.student_dict:
            return True
        return False

    @classmethod
    def query_username_password(cls, username, password):
        """根据账号+密码查询学员"""
        if username in data.Database.student_dict:
            user = data.Database.student_dict.get(username)
            if password == user.password:
                # 查询到用户
                print("查询到符合账号+密码的用户")
                return user
        print("没有查询到符合账号+密码的用户")
        return None

    @classmethod
    def query_all(cls):
        """查询所有的学员信息"""
        return data.Database.student_dict


class Course:
    """课程类型"""

    def __init__(self, name, teacher, times, score, maxsize, remark):
        """课程属性初始化"""
        self.name = name
        self.teacher = teacher
        self.times = int(times)
        self.score = int(score)
        self.maxsize = int(maxsize)
        self.remark = remark

    def save(self):
        """保存当前课程数据"""
        data.Database.course_dict[self.name] = self

    @classmethod
    def query_name(cls, name):
        """根据课程名称查询，这个课程是否存在：存在就返回课程，否则返回False"""
        # return name in data.Database.course_dict
        if name in data.Database.course_dict:
            return data.Database.course_dict.get(name)
        return False

    @classmethod
    def query_all(cls):
        """查询所有课程"""
        return data.Database.course_dict
