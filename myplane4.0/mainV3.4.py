"""
飞机大战V3.4版本
"""
import pygame
# 初始化pygame模块中的游戏资源
pygame.init()


class Resource:
    """游戏中的资源数据"""
    # 游戏屏幕数据
    SCREEN_WIDTH = 512
    SCREEN_HEIGHT = 768
    SCREEN_FULL = 0
    SCREEN_DEPTH = 32


class GameSprite(pygame.sprite.Sprite):
    """游戏中所有物体的父类"""
    def __init__(self, image, position={"x": 0, "y": 0},
                 speed={"x": 0, "y": 0}):
        super().__init__()
        self.image = pygame.image.load(image) # 将用户的字符串图片加载
        self.rect = self.image.get_rect()     # 获取图片尺寸位置(x,y,width,height)
        self.rect.x = position.get("x")
        self.rect.y = position.get("y")
        self.speed = speed

    def update(self):
        """精灵组update()更新时，自动调用精灵的update()方法"""
        self.rect.x += self.speed.get("x")
        self.rect.y += self.speed.get("y")
        # 自动调用事件处理和边界判断
        self.event()
        self.boundary()

    def event(self):
        """公共事件操作"""
        pass

    def boundary(self):
        """边界判断"""
        pass


class BackgroundSprite(GameSprite):
    """游戏背景"""

    def boundary(self):
        """边界判断  rect 游戏元素占据的长方形位置和坐标"""
        if self.rect.y > Resource.SCREEN_HEIGHT:
            # 超出边界
            self.rect.y = -Resource.SCREEN_HEIGHT


class RoleSprite(GameSprite):
    """游戏角色精灵"""

    def __init__(self, image, position={"x": 0, "y": 0},
                 speed={"x": 0, "y": 0}, blood=1):
        super().__init__(image, position, speed)
        self.blood = blood  # 血量


class Plane(RoleSprite):
    """飞机类型"""

    def __init__(self, image, position={"x": 0, "y": 0},
                 speed={"x": 0, "y": 0}, blood=1):
        super().__init__(image, position, speed, blood)
        # 弹夹：就是一个保存创建子弹的一个精灵组
        self.bullet_group = pygame.sprite.Group()
        # 添加一个英雄飞机发射子弹的计数器
        self.hero_index = 0



class HeroPlane(Plane):
    """英雄飞机类型"""

    def update(self):
        """重写update()方法，让父类中的update()自动运动失效"""
        self.event()
        self.boundary()

    def event(self):
        """重写event()方法，让键盘控制飞机运动"""
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            print("<--------飞机向左移动")
            self.rect.x -= self.speed.get("x")
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            print("飞机向右移动----------->")
            self.rect.x += self.speed.get("x")
        if key[pygame.K_UP] or key[pygame.K_w]:
            print("飞机向上移动^^^^^^^^^")
            self.rect.y -= self.speed.get("y")
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            print("飞机向下移动VVVVVVVVVV")
            self.rect.y += self.speed.get("y")
        if key[pygame.K_SPACE]:
            print("玩家按下开火键")
            self.fire()

    def fire(self):
        """创建子弹精灵：子弹上膛"""
        # 计数器：循环计数 0.1.2.3...60->0.1.2.3...60->0..
        self.hero_index += 1
        if self.hero_index >= 60:
            self.hero_index = 0

        if self.hero_index % 10 == 0:
            if (len(self.bullet_group)) < 10:
                # 创建子弹
                bullet = Bullet("images/bullets/bullet6.png",
                                position={"x": self.rect.centerx-10,
                                          "y": self.rect.centery-80},
                                speed={"x": 0, "y": -10})
                # 上膛
                self.bullet_group.add(bullet)

    def boundary(self):
        """重写边界判断方法，让飞机不要越界"""
        # 左右边界
        if self.rect.x < 0: # 左
            self.rect.x = 0
        if self.rect.x + self.rect.width > Resource.SCREEN_WIDTH: # 右
            self.rect.x = Resource.SCREEN_WIDTH - self.rect.width
        # 上下边界
        if self.rect.y < 0:# 上
            self.rect.y = 0
        if self.rect.y + self.rect.height > Resource.SCREEN_HEIGHT: # 下
            self.rect.y = Resource.SCREEN_HEIGHT - self.rect.height


class EnemyPlane(Plane):
    """地方飞机类型"""
    pass


class Bullet(RoleSprite):
    """子弹类型"""
    def boundary(self):
        """边界判断：子弹超出边界，自动销毁"""
        if (self.rect.y < -self.rect.height) \
                or (self.rect.y > Resource.SCREEN_HEIGHT):
            print("子弹销毁^_^")
            self.kill()


class Replanish(RoleSprite):
    """补给类型"""
    pass


class Engine:
    """游戏引擎类型"""

    def __init__(self):
        """初始化游戏场景,资源"""
        self.screen = pygame.display.set_mode((Resource.SCREEN_WIDTH,
                                               Resource.SCREEN_HEIGHT),
                                              Resource.SCREEN_FULL,
                                              Resource.SCREEN_DEPTH)
        self.common_group = pygame.sprite.Group() # 公共
        self.hero_group = pygame.sprite.Group()   # 我方
        self.enemy_group = pygame.sprite.Group()  # 敌方
        self.clock = pygame.time.Clock()

    def __update_group(self):
        """更新精灵组的方法"""
        self.common_group.update()
        self.common_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

    def start(self):
        """开始游戏的方法"""

        # 创建背景精灵对象
        bg1 = BackgroundSprite("images/bg1.jpg",
                               position={"x": 0, "y": 0},
                               speed={"x": 0, "y": 2})
        bg2 = BackgroundSprite("images/bg1.jpg",
                               position={"x": 0, "y": -Resource.SCREEN_HEIGHT},
                               speed={"x": 0, "y": 2})
        # 将背景添加到公共精灵组
        self.common_group.add(bg1)
        self.common_group.add(bg2)

        # 创建英雄飞机
        hero = HeroPlane("images/hero_planes/hp03_01.png", position={"x": 200, "y": 500},
                         speed={"x": 3, "y": 5})
        # 将英雄飞机添加到精灵组
        self.hero_group.add(hero)

        # 循环展示游戏场景
        while True:
            self.clock.tick(60)
            # 事件监测
            e_list = pygame.event.get()
            for e in e_list:
                if e.type == pygame.QUIT:
                    pygame.quit()
            # 更新所有的精灵组
            self.__update_group()

            # 更新英雄飞机的子弹精灵组
            hero.bullet_group.update()
            hero.bullet_group.draw(self.screen)

            # 更新展示
            pygame.display.update()


# 游戏开始
engine = Engine()
engine.start()
