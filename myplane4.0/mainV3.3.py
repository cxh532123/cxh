"""
飞机大战 V3.3
    面向对象，完善GameSprite类型中的代码
"""
import pygame
pygame.init()


class Resource:
    """游戏中的固定数据：声明为资源类型中的类属性"""
    # 游戏屏幕的宽度和高度
    # 在python中如果变量中的所有字母都大写，表示这是一个约定的常量(不要去改变的数据)
    SCREEN_WIDTH = 512
    SCREEN_HEIGHT = 768
    SCREEN_FULL = 0
    SCREEN_DEPTH = 32


class GameSprite(pygame.sprite.Sprite):
    """所有游戏资源的父类"""
    def __init__(self, image, position={"x": 0, "y": 0}, speed={"x": 0, "y": 0}):
        super().__init__()
        self.image = pygame.image.load(image)  # 加载用户输入的字符串图片
        self.rect = self.image.get_rect()   # 获取当前图片的位置固定语法:(x, y, width, height)
        self.rect.x = position["x"]
        self.rect.y = position["y"]
        self.speed = speed

    def update(self):
        """精灵组.update()调用执行时，自动调用包含的精灵的update()方法"""
        self.rect.x += self.speed.get("x")
        self.rect.y += self.speed.get("y")
        # 自动调用
        self.event()

    def event(self):
        """公共事件操作"""
        e_list = pygame.event.get()
        for e in e_list:
            if e.type == pygame.QUIT:
                pygame.quit()


class BackgroundSprite(GameSprite):
    """游戏背景精灵"""

    def update(self):
        """重写update方法"""
        super().update()  # 调用父类的方法，完成移动和事件操作
        self.boundary()   # 主动调用自己的方法，完成边界判断

    def boundary(self):
        """边界判断"""
        if self.rect.y >= Resource.SCREEN_HEIGHT:
            # 背景运动超出边界
            self.rect.y = -Resource.SCREEN_HEIGHT


class RoleSprite(GameSprite):
    """游戏中运动角色的父类"""
    def __init__(self, image, position={"x": 0, "y": 0}, speed={"x": 0, "y": 0}, blood=1):
        super().__init__(image, position, speed)
        self.blood = blood  # 血量，默认1点血


class Plane(RoleSprite):
    """飞机类型"""
    def __init__(self, image, position={"x": 0, "y": 0}, speed={"x": 0, "y": 0}, blood=1):
        super().__init__(image, position, speed, blood)
        # 飞机的弹夹：是一个包含子弹的精灵组
        self.bullet_group = pygame.sprite.Group()


class HeroPlane(Plane):
    """英雄飞机"""
    def event(self):
        """事件控制:方向控制飞机移动"""
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            print("飞机向左移动<<<<<<<<")
            self.rect.x -= self.speed.get("x")
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            print("飞机向右移动>>>>>>>>>")
            self.rect.x += self.speed.get("x")
        if key[pygame.K_UP] or key[pygame.K_w]:
            print("飞机向上移动^^^^^^^^^")
            self.rect.y -= self.speed.get("y")
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            print("飞机向下移动vvvvvvvvv")
            self.rect.y += self.speed.get("y")
        if key[pygame.K_SPACE]:
            print("英雄飞机开火了.......")
            self.fire()

    def fire(self):
        """开火的方法"""
        if len(self.bullet_group) < 10:
            # 1、创建子弹对象
            bullet = Bullet("images/bullets/bullet3.png",
                            position={"x": self.rect.centerx-10,
                                      "y": self.rect.centery-100},
                            speed={"x": 0, "y": -8})
            # 2、添加到精灵组
            self.bullet_group.add(bullet)
        print(len(self.bullet_group))


    def boundary(self):
        """边界判断:飞机不能飞出场景外"""
        # 左右边界
        if self.rect.x < 0:  # 左边出边界
            self.rect.x = 0
        if self.rect.x + self.rect.width > Resource.SCREEN_WIDTH: # 右边出边界
            self.rect.x = Resource.SCREEN_WIDTH - self.rect.width
        # 上下边界
        if self.rect.y < 0: # 上
            self.rect.y = 0
        if self.rect.y + self.rect.height > Resource.SCREEN_HEIGHT: # 下
            self.rect.y = Resource.SCREEN_HEIGHT - self.rect.height

    def update(self):
        """更新方法"""
        # 英雄飞机，不主动调用父类的update()方法，执行自己的update()即可
        # 英雄飞机不主动移动
        # super().update()
        self.event()
        self.boundary()


class Bullet(RoleSprite):
    """子弹类型"""

    def update(self):
        # 调用父类的方法，移动子弹
        super().update()
        # 自动调用边界判断
        self.boundary()

    def boundary(self):
        """子弹的边界判断：子弹一旦超出窗口区域，自动销毁"""
        if (self.rect.y < -self.rect.height) \
            or (self.rect.y > Resource.SCREEN_HEIGHT):
            # 从屏幕上方超出边界 或者 从屏幕上方超出边界
            # 销毁子弹：销毁当前精灵
            self.kill()


class Replenish(RoleSprite):
    """补给资源类型"""
    pass


class Engine:
    """游戏引擎：控制游戏开始、过关、结束"""
    def __init__(self):
        """加载游戏资源初始化的方法"""
        # 游戏窗口
        self.screen = pygame.display.set_mode((Resource.SCREEN_WIDTH,
                                               Resource.SCREEN_HEIGHT),
                                              Resource.SCREEN_FULL,
                                              Resource.SCREEN_DEPTH)
        # 早上：一个精灵组；下午：三个精灵组
        # 游戏公共资源组：背景
        self.background_group = pygame.sprite.Group()
        # 游戏英雄飞机组
        self.hero_group = pygame.sprite.Group()
        # 游戏敌方飞机组
        self.enemy_group = pygame.sprite.Group()
        # 游戏时钟
        self.clock = pygame.time.Clock()

    def __update_group(self):
        """私有方法，更新所有精灵组"""
        self.background_group.update()
        self.background_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

    def start(self):
        """游戏开始的方法"""
        # 创建游戏中的背景精灵
        background1 = BackgroundSprite("images/bg1.jpg", speed={"x": 0, "y": 2})
        background2 = BackgroundSprite("images/bg1.jpg",
                                       position= {"x": 0, "y": -Resource.SCREEN_HEIGHT},
                                       speed={"x": 0, "y": 2})
        # 添加到精灵组
        self.background_group.add(background1)
        self.background_group.add(background2)

        # 创建英雄飞机，添加到英雄飞机精灵组
        hero = HeroPlane("images/hero_planes/hp02_01.png",
                         position={"x": 200, "y": 500},
                         speed={"x": 3, "y": 5})
        self.hero_group.add(hero)

        # 场景循环
        while True:
            self.clock.tick(60)
            # 更新所有精灵组
            self.__update_group()

            # 更新英雄飞机的子弹精灵组
            hero.bullet_group.update()
            hero.bullet_group.draw(self.screen)

            pygame.display.update()


# 调用游戏开始的方法：启动游戏
engine = Engine()
engine.start()



