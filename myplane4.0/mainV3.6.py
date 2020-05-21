"""
飞机大战V3.5版本
    展示自定义信息
"""
import random

import pygame
# 初始化pygame模块中的游戏资源
pygame.init()
pygame.mixer.init()


class Resource:
    """游戏中的资源数据"""
    # 游戏屏幕数据
    SCREEN_WIDTH = 512
    SCREEN_HEIGHT = 768
    SCREEN_FULL = 0
    SCREEN_DEPTH = 32

    # 英雄积分
    HERO_SCORE = 0
    # 逃逸敌机
    ESCAPE_COUNT = 0

    # 子弹爆炸效果图片
    BULLET_BOMB = pygame.image.load("images/bomb.png")
    BULLET_BOMB_IMG = [
        BULLET_BOMB.subsurface((721, 390, 50, 50)),
        BULLET_BOMB.subsurface((701, 450, 50, 50)), #
        BULLET_BOMB.subsurface((673, 398, 50, 50)),
        BULLET_BOMB.subsurface((701, 450, 50, 50)), #
        BULLET_BOMB.subsurface((605, 398, 50, 50)),
        BULLET_BOMB.subsurface((701, 450, 50, 50)), #
        BULLET_BOMB.subsurface((651, 459, 50, 50)),
        BULLET_BOMB.subsurface((701, 450, 50, 50)), #
        BULLET_BOMB.subsurface((602, 462, 50, 50)),
        BULLET_BOMB.subsurface((721, 390, 50, 50)),
    ]
    # 敌方飞机爆炸效果
    ENEMY_BOMB_IMG = [
        BULLET_BOMB.subsurface((585, 130, 130, 130)),
        BULLET_BOMB.subsurface((585, 0, 130, 130)),
        BULLET_BOMB.subsurface((710, 250, 130, 130)),
        BULLET_BOMB.subsurface((710, 0, 130, 130)),
        BULLET_BOMB.subsurface((580, 250, 130, 130)),
        BULLET_BOMB.subsurface((710, 130, 130, 130)),
        BULLET_BOMB.subsurface((170, 170, 130, 130)),
        BULLET_BOMB.subsurface((170, 0, 130, 130)),
        BULLET_BOMB.subsurface((450, 150, 130, 130)),
        BULLET_BOMB.subsurface((170, 320, 130, 130)),
        BULLET_BOMB.subsurface((450, 0, 130, 130)),
        BULLET_BOMB.subsurface((710, 250, 130, 130)),
        BULLET_BOMB.subsurface((330, 0, 130, 130)),
        BULLET_BOMB.subsurface((450, 285, 130, 130)),
        BULLET_BOMB.subsurface((865, 145, 130, 130)),
        BULLET_BOMB.subsurface((320, 280, 130, 130)),
        BULLET_BOMB.subsurface((320, 150, 130, 130)),
    ]

    # 自定义一个事件：每隔1秒钟，创建一个敌方小飞机
    ENEMY_SMALL_IMG = [
        "images/enemy_planes/ep03_01.png",
        "images/enemy_planes/ep03_02.png",
        "images/enemy_planes/ep03_03.png",
        "images/enemy_planes/ep03_04.png",
        "images/enemy_planes/ep03_05.png"]
    ENEMY_SMALL = pygame.USEREVENT
    pygame.time.set_timer(ENEMY_SMALL, 1000) # 24

    # 自定义一个事件：每隔5秒钟，创建一个中型飞机
    ENEMY_MIDDLE_IMG = [
        "images/enemy_planes/ep02_01.png",
        "images/enemy_planes/ep02_02.png",
        "images/enemy_planes/ep02_03.png",
    ]
    ENEMY_MIDDLE = pygame.USEREVENT + 1  # 自定义事件，为什么要加1？ 25
    pygame.time.set_timer(ENEMY_MIDDLE, 5000)

    # 自定义一个事件：敌方飞机开火
    ENEMY_FIRE = pygame.USEREVENT + 2  # 自定义事件
    pygame.time.set_timer(ENEMY_FIRE, 1000)

    @classmethod
    def play_bgm(cls):
        pygame.mixer.music.load("effect/bgm.mp3")
        pygame.mixer.music.play()

    @classmethod
    def fire_bullet(cls):
        """发射子弹：Sound方法中，加载wav格式的音效，但是不能加载mp3格式的音乐"""
        # 音效都有自己的格式，一般通过后缀名体现
        # 但是直接修改后缀名称，不能修改音效的数据格式
        # 下载mp3格式的英雄，必须转换成wav，而不是修改后缀名
        bullet = pygame.mixer.Sound("effect/bulletfire.wav")
        bullet.play()

    @classmethod
    def enemy_bomb(cls):
        bomb = pygame.mixer.Sound("effect/爆炸音效.wav")
        bomb.play()

    @classmethod
    def print_text(cls, x, y, text, color=(255,255,255),
                   # font=pygame.font.Font("font/ITCKRIST.TTF", 18)):
                   font=pygame.font.Font(None, 18)):
        """打印提示信息"""
        img = font.render(text, True, color)
        engine.screen.blit(img, (x, y))


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
        # 事件监测
        e_list = pygame.event.get()
        for e in e_list:
            if e.type == pygame.QUIT:
                pygame.quit()
            # 检查敌方小飞机创建的事件
            if e.type == Resource.ENEMY_SMALL: # 24
                print("创建一架敌方小型飞机...")
                enemy = EnemyPlane(random.choice(Resource.ENEMY_SMALL_IMG),
                                   position={"x": random.randint(0, Resource.SCREEN_WIDTH - 115),
                                             "y": -83},
                                   speed={"x": 0, "y": 5}, blood=2)
                # 添加到敌方精灵组
                engine.enemy_group.add(enemy)
            if e.type == Resource.ENEMY_MIDDLE:  # 25
                print("创建一架中型飞机>>>")
                enemy = EnemyPlane(random.choice(Resource.ENEMY_MIDDLE_IMG),
                                   position={"x": random.randint(0, Resource.SCREEN_WIDTH - 192),
                                             "y": -135},
                                   speed={"x": 0, "y": 3}, blood=3)
                engine.enemy_group.add(enemy)
            # 检测敌方飞机开火事件
            if e.type == Resource.ENEMY_FIRE:
                # 敌方飞机开火
                for enemy in engine.enemy_group:
                    # 获取到所有敌方飞机：开火
                    enemy.fire()

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
        # 添加一个敌方飞机爆炸的索引
        self.bomb_index = 0

    def bomb(self):
        """爆炸的方法"""
        # 速度清零
        self.speed = {"x": 0, "y": 0}
        # 更换爆炸图片
        self.image = Resource.ENEMY_BOMB_IMG[self.bomb_index]
        # 索引递增
        self.bomb_index += 1
        # 爆炸图片一旦全部展示完毕，销毁飞机对象
        if self.bomb_index > len(Resource.ENEMY_BOMB_IMG) - 1:
            Resource.enemy_bomb()
            self.kill()

    def boundary(self):
        """所有飞机，一旦血量清零：飞机消失"""
        if self.blood <= 0:
            # Resource.enemy_bomb()
            # self.kill()
            self.bomb()


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
                                speed={"x": 0, "y": -20})
                # 播放音效
                Resource.fire_bullet()
                # 上膛
                self.bullet_group.add(bullet)

    def boundary(self):
        """重写边界判断方法，让飞机不要越界"""
        super().boundary() # 调用父类边界判断：血量清零判断
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


    def boundary(self):
        """敌方飞机  边界判断"""
        super().boundary() # 调用父类边界判断：血量清零判断
        if self.rect.y > Resource.SCREEN_HEIGHT:
            # 逃逸飞机
            Resource.ESCAPE_COUNT += 1
            self.kill()

    def fire(self):
        """创建子弹精灵：子弹上膛"""
        # Resource.fire_bullet()
        # 创建子弹
        bullet = Bullet("images/bullets/bullet6.png",
                        position={"x": self.rect.centerx-10,
                                  "y": self.rect.centery+20},
                        speed={"x": 0, "y": 10})
        # 添加精灵组
        self.bullet_group.add(bullet)


class Bullet(RoleSprite):
    """子弹类型"""
    def __init__(self, image, position={"x": 0, "y": 0},
                 speed={"x": 0, "y": 0}, blood=1):
        super().__init__(image, position, speed, blood=1)
        # 子弹爆炸图片的索引
        self.bomb_index = 0

    def bomb(self):
        """爆炸效果：让爆炸的图片，替换子弹的图片"""
        # 运动速度清零
        self.speed = {"x": 0, "y": 0}
        # 替换爆炸图片
        self.image = Resource.BULLET_BOMB_IMG[self.bomb_index]
        self.bomb_index += 1
        if self.bomb_index > len(Resource.BULLET_BOMB_IMG)-1:
            # 爆炸效果完成，移除子弹对象
            self.kill()

    def boundary(self):
        """边界判断：子弹超出边界，自动销毁"""
        if (self.rect.y < -self.rect.height) \
                or (self.rect.y > Resource.SCREEN_HEIGHT):
            print("子弹销毁^_^")
            self.kill()
        if self.blood <= 0:
            # 血量边界
            # self.kill()
            self.bomb()


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
        self.step = 1   # 关卡

    def __collide_bullet_enemy(self):
        """碰撞检测方法：英雄子弹--敌方飞机"""
        # 英雄飞机的子弹精灵组，和敌方飞机精灵组
        for hero in self.hero_group:
            # 子弹精灵组和敌方飞机精灵组
            result = pygame.sprite.groupcollide(hero.bullet_group, self.enemy_group,
                                                False,              False)
            # result: {"key:子弹": value:[被碰撞的飞机对象]}
            for bullet, enemies in result.items(): # 遍历字典中的value数据
                # 子弹 掉血
                bullet.blood -= 1
                if bullet.blood <= 0:
                    # 思考：子弹击中敌方飞机，需要添加一个击中音效吗？
                    # 从子弹精灵组中移除
                    hero.bullet_group.remove(bullet)
                    # 添加到公共精灵组
                    self.common_group.add(bullet)

                # 循环敌方飞机
                for enemy in enemies:       # 遍历列表
                    # 得到被碰撞的飞机，减少血量
                    enemy.blood -= 1
                    if enemy.blood == 0:
                        # 积分增加
                        Resource.HERO_SCORE += 1

    def __collide_hero_enemy(self):
        """碰撞检测方法：英雄飞机--敌方飞机"""
        # 直接碰撞英雄精灵组 和 敌方飞机精灵组
        pygame.sprite.groupcollide(self.hero_group, self.enemy_group,
                                   True,            True)

    def __collide_enemy_bullet_hero(self):
        """碰撞检测，敌方飞机-子弹--英雄飞机"""
        # 获取所有敌方飞机
        for enemy in self.enemy_group:
            # 敌方子弹-- 英雄飞机
            result = pygame.sprite.groupcollide(enemy.bullet_group, self.hero_group,
                                                True,               False)  # 敌方飞机子弹没有消失？
            # 英雄飞机掉血
            for heroes in result.values():
                # 得到英雄飞机
                for hero in heroes:
                    hero.blood -= 1

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
        # 播放BGM
        # Resource.play_bgm()

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
                         speed={"x": 3, "y": 5}, blood=10)
        # 将英雄飞机添加到精灵组
        self.hero_group.add(hero)

        # 循环展示游戏场景
        while True:
            self.clock.tick(60)

            # 更新所有的精灵组
            self.__update_group()

            # 调用碰撞检测方法
            self.__collide_bullet_enemy()
            self.__collide_hero_enemy()
            self.__collide_enemy_bullet_hero()

            # 更新英雄飞机的子弹精灵组
            hero.bullet_group.update()
            hero.bullet_group.draw(self.screen)

            # 更新敌方飞机子弹精灵组
            for enemy in self.enemy_group:
                enemy.bullet_group.update()
                enemy.bullet_group.draw(self.screen)

            # 展示自定义数据
            Resource.print_text(0, 0, f"HERO X POINT:{hero.rect.x}") # 英雄飞机X坐标
            Resource.print_text(0, 40, f"HERO Y POINT:{hero.rect.y}") # 英雄飞机Y坐标
            Resource.print_text(0, 60, f"ENEMIES COUNT:{len(self.enemy_group)}") # 屏幕上敌方飞机数量
            Resource.print_text(0, 80, f"ESCAPE COUNT:{Resource.ESCAPE_COUNT}") # 逃逸的地方飞机数量
            Resource.print_text(0, 100, f"PLAYER SCORE:{Resource.HERO_SCORE}") # 玩家积分

            # 更新展示
            pygame.display.update()

# 游戏开始
engine = Engine()
engine.start()
