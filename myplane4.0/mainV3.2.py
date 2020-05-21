"""
飞机大战 V3.2
    面向对象，初始化游戏场景
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
    pass


class RoleSprite(GameSprite):
    """游戏中运动角色的父类"""
    pass


class Plane(RoleSprite):
    """飞机类型"""
    pass


class Bullet(RoleSprite):
    """子弹类型"""
    pass


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
        # 场景循环
        while True:
            # 更新所有精灵组
            self.__update_group()

            pygame.display.update()


# 调用游戏开始的方法：启动游戏
engine = Engine()
engine.start()



