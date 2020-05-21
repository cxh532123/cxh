"""
飞机大战 V3.1
    面向对象，完善开发版本
"""
import pygame
pygame.init()


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

    def start(self):
        """游戏开始的方法"""


# 调用游戏开始的方法：启动游戏
Engine().start()



