import pygame
import sys
import random
import math
import time

# 初始化Pygame
pygame.init()

# 使用系统默认中文字体
try:
    font_path = pygame.font.match_font('simhei')  # 优先使用黑体
    if font_path is None:
        font_path = pygame.font.match_font('microsoftyaheimicrosoftyaheiui')  # 尝试使用雅黑
    GAME_FONT = pygame.font.Font(font_path, 36)
except:
    GAME_FONT = pygame.font.Font(None, 36)  # 如果没有找到中文字体，使用默认字体

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)  # 深灰黑而不是纯黑
RED = (255, 59, 48)   # 苹果风格红色
GREEN = (52, 199, 89) # 苹果风格绿色
BLUE = (0, 122, 255)  # 苹果风格蓝色
GRAY = (142, 142, 147)
DARK_GRAY = (44, 44, 46)
BORDER_COLOR = (60, 60, 60)  # 边框颜色
BG_COLOR = (28, 28, 30)      # 背景色

# 方向定义
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 在颜色定义后添加按键图标
KEY_ICONS = {
    "↑": "⬆️",
    "↓": "⬇️",
    "←": "⬅️",
    "→": "���️",
    "空格键": "⎵",
    "R键": "Ⓡ",
    "ESC": "⎋"
}

# 添加游戏区域的边界常量
MARGIN = 20  # 游戏区域边距
PLAYABLE_WIDTH = (WINDOW_WIDTH - (MARGIN * 2)) // GRID_SIZE
PLAYABLE_HEIGHT = (WINDOW_HEIGHT - (MARGIN * 2)) // GRID_SIZE

# 更新颜色定义，使用更优雅的配色方案
PANEL_BG = (22, 22, 25)      # 深色背景
PANEL_LIGHT = (32, 32, 35)   # 面板色
ACCENT_BLUE = (10, 132, 255)  # 主要强调色
ACCENT_GLOW = (20, 142, 255, 50)  # 发光效果
TEXT_PRIMARY = (240, 240, 240)  # 主要文本色
TEXT_SECONDARY = (160, 160, 165)  # 次要文本色
BUTTON_BG = (40, 40, 45)     # 按键背景色
BUTTON_ACTIVE = (50, 50, 55)  # 按键激活色

class Snake:
    def __init__(self):
        self.size = 20
        self.game_padding = 20
        # 更新颜色设置
        self.head_color = (60, 220, 60)    # 鲜艳的绿色头部
        self.body_color = (50, 180, 50)    # 稍暗的绿色身体
        self.edge_light = (120, 255, 120)  # 明亮的边缘高光
        self.edge_dark = (40, 160, 40)     # 深色边缘
        self.reset()

    def reset(self):
        """重置蛇的位置到网格中心"""
        # 计算起始网格位置
        grid_x = (WINDOW_WIDTH - 2 * self.game_padding) // (2 * self.size)
        grid_y = (WINDOW_HEIGHT - 2 * self.game_padding) // (2 * self.size)
        
        # 计算实际像素位置（确保对齐网格）
        start_x = self.game_padding + grid_x * self.size
        start_y = self.game_padding + grid_y * self.size
        
        self.positions = [(start_x, start_y)]
        self.direction = (1, 0)
        self.score = 0
        self.length = 1

    def update(self):
        """更新蛇的位置，修复边界判定"""
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        
        # 计算新位置
        new_x = head_x + dir_x * self.size
        new_y = head_y + dir_y * self.size
        
        # 检查是否真正撞墙（严格判定）
        if (new_x <= self.game_padding - self.size or 
            new_x >= WINDOW_WIDTH - self.game_padding or
            new_y <= self.game_padding - self.size or 
            new_y >= WINDOW_HEIGHT - self.game_padding):
            return False
        
        # 检查是否撞到自己
        if (new_x, new_y) in self.positions[:-1]:
            return False
            
        # 更新位置
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def get_head_position(self):
        return self.positions[0]

    def turn(self, direction):
        if self.length > 1:
            if (direction[0] * -1, direction[1] * -1) == self.direction:
                return
        self.direction = direction

    def render(self, screen):
        """绘制蛇，使用更明显的渐变效果"""
        for i, pos in enumerate(self.positions):
            if i == 0:  # 蛇头
                base_color = self.head_color
                edge_light = self.edge_light
                edge_dark = self.edge_dark
            else:  # 蛇身渐变
                # 计算渐变比例，但保持颜色明亮
                fade = min(0.5, i * 0.05)  # 限制最大渐变程度
                # 向黄色渐变而不是变暗
                base_color = (
                    min(255, self.body_color[0] + int(100 * fade)),  # 红色增加
                    max(100, self.body_color[1] - int(30 * fade)),   # 绿色稍微降低
                    min(255, self.body_color[2] + int(80 * fade))    # 蓝色增加
                )
                edge_light = (
                    min(255, self.edge_light[0] + int(100 * fade)),
                    max(120, self.edge_light[1] - int(30 * fade)),
                    min(255, self.edge_light[2] + int(80 * fade))
                )
                edge_dark = (
                    min(255, self.edge_dark[0] + int(100 * fade)),
                    max(40, self.edge_dark[1] - int(30 * fade)),
                    min(255, self.edge_dark[2] + int(80 * fade))
                )
            
            # 绘制主体
            pygame.draw.rect(screen, base_color,
                           (pos[0], pos[1], self.size, self.size))
            
            # 绘制高光
            pygame.draw.rect(screen, edge_light,
                           (pos[0], pos[1], self.size, self.size//3))
            
            # 绘制边框
            pygame.draw.rect(screen, edge_dark,
                           (pos[0], pos[1], self.size, self.size), 1)

class Food:
    def __init__(self):
        self.size = 20 # 网格大小
        self.game_padding = 20
        self.radius = 8
        # 添加所有需要的颜色属性
        self.main_color = (220, 40, 40)      # 主体颜色
        self.highlight_color = (255, 180, 180)  # 高光颜色
        self.shadow_color = (150, 30, 30, 100)  # 阴影颜色
        self.glow_color = (255, 100, 100)      # 边缘光晕颜色
        self.reset()

    def reset(self):
        """重置食物位置到网格中心"""
        grid_width = (WINDOW_WIDTH - 2 * self.game_padding) // self.size
        grid_height = (WINDOW_HEIGHT - 2 * self.game_padding) // self.size
        
        # 随机选择网格位置
        grid_x = random.randint(0, grid_width - 1)
        grid_y = random.randint(0, grid_height - 1)
        
        # 计算网格左上角坐标
        self.grid_pos = (
            self.game_padding + grid_x * self.size,
            self.game_padding + grid_y * self.size
        )
        
        # 计算食物中心点坐标（网格中心）
        self.position = (
            self.grid_pos[0] + self.size // 2,
            self.grid_pos[1] + self.size // 2
        )

    def render(self, screen):
        """绘制食物，使用预定义的颜色"""
        x, y = self.position
        
        # 阴影
        shadow_offset = 2
        s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, self.shadow_color, (self.radius, self.radius), self.radius)
        screen.blit(s, (x - self.radius + shadow_offset, y - self.radius + shadow_offset))
        
        # 主体
        pygame.draw.circle(screen, self.main_color, (x, y), self.radius)
        
        # 高光
        highlight_radius = self.radius // 2
        pygame.draw.circle(screen, self.highlight_color,
                         (x - highlight_radius//2, y - highlight_radius//2),
                         highlight_radius)
        
        # 边缘光晕
        pygame.draw.circle(screen, self.glow_color, (x, y), self.radius, 1)

def draw_rounded_rect(surface, color, rect, radius=15, border=0):
    """绘制圆角矩形"""
    rect = pygame.Rect(rect)
    
    # 绘制主要矩形
    pygame.draw.rect(surface, color, rect.inflate(-radius * 2, 0))
    pygame.draw.rect(surface, color, rect.inflate(0, -radius * 2))
    
    # 绘制四个圆角
    circle_centers = [
        (rect.topleft, rect.topright, rect.bottomleft, rect.bottomright)
    ]
    for circle_center in circle_centers[0]:
        pygame.draw.circle(surface, color, circle_center, radius)

    # 如果需要边
    if border > 0:
        pygame.draw.rect(surface, BORDER_COLOR, rect, border, border_radius=radius)

# 在游戏开始时初始化字体
def get_chinese_font():
    """获取系统中可用的中文字体"""
    chinese_fonts = [
        'microsoftyahei', 
        'simsun', 
        'simhei', 
        'microsoft yahei',
        'dengxian',
        'fangsong',
        'kaiti'
    ]
    
    available_font = None
    for font_name in chinese_fonts:
        try:
            available_font = pygame.font.SysFont(font_name, 24)
            if available_font.render('试', True, (0, 0, 0)).get_width() > 10:
                return font_name
        except:
            continue
    
    return None

class Game:
    def create_gradient_surface(self, width, height, start_color, end_color):
        """创建渐变效果"""
        surface = pygame.Surface((width, height))
        for y in range(height):
            ratio = y / height
            color = [int(start + (end - start) * ratio) 
                    for start, end in zip(start_color, end_color)]
            pygame.draw.line(surface, color, (0, y), (width, y))
        return surface

    def draw_instructions(self):
        """绘制控制说明面板"""
        # 创建主面板背景
        panel_bg = self.create_gradient_surface(
            self.control_panel_width,
            self.control_panel_height,
            (40, 40, 45),  # 顶部颜色
            (30, 30, 35)   # 底部颜色
        )
        
        # 添加阴影效果
        shadow_surface = pygame.Surface((self.control_panel_width + 6, self.control_panel_height + 6))
        shadow_surface.fill((20, 20, 25))
        shadow_surface.set_alpha(100)
        self.screen.blit(shadow_surface, 
                        (self.control_panel_x - 3, self.control_panel_y - 3))
        
        # 绘制主面板
        self.screen.blit(panel_bg, (self.control_panel_x, self.control_panel_y))
        
        # 绘制边框光效
        for i in range(3):
            alpha = 255 - i * 50
            color = (80 - i * 10, 80 - i * 10, 85 - i * 10)
            border_rect = pygame.Rect(
                self.control_panel_x - i,
                self.control_panel_y - i,
                self.control_panel_width + i * 2,
                self.control_panel_height + i * 2
            )
            pygame.draw.rect(self.screen, color, border_rect, 1)
        
        # 分数显示
        y_offset = self.control_panel_y + 30
        
        # 分数背景
        score_bg_rect = pygame.Rect(
            self.control_panel_x + 20,
            y_offset - 10,
            self.control_panel_width - 40,
            80
        )
        pygame.draw.rect(self.screen, (35, 35, 40), score_bg_rect, border_radius=10)
        pygame.draw.rect(self.screen, (45, 45, 50), score_bg_rect, 1, border_radius=10)
        
        # 当前得分
        score_text = self.font.render("当前得分:", True, (200, 200, 200))
        self.screen.blit(score_text, (self.control_panel_x + 30, y_offset))
        
        score_value = self.score_font.render(str(self.snake.score), True, (255, 255, 255))
        score_value_rect = score_value.get_rect(
            right=self.control_panel_x + self.control_panel_width - 30,
            centery=y_offset + 10
        )
        self.screen.blit(score_value, score_value_rect)
        
        # 最高分
        y_offset += 40
        high_score_text = self.font.render("最高分:", True, (200, 200, 200))
        self.screen.blit(high_score_text, (self.control_panel_x + 30, y_offset))
        
        high_score_value = self.score_font.render(str(self.high_score), True, (255, 255, 255))
        high_score_value_rect = high_score_value.get_rect(
            right=self.control_panel_x + self.control_panel_width - 30,
            centery=y_offset + 10
        )
        self.screen.blit(high_score_value, high_score_value_rect)
        
        # 分隔线
        y_offset += 50
        for i in range(3):
            alpha = 255 - i * 50
            color = (60 - i * 10, 60 - i * 10, 65 - i * 10)
            pygame.draw.line(
                self.screen,
                color,
                (self.control_panel_x + 20, y_offset + i),
                (self.control_panel_x + self.control_panel_width - 20, y_offset + i)
            )
        
        # 控制说明标题
        y_offset += 20
        title = self.title_font.render("控制", True, (255, 255, 255))
        self.screen.blit(title, (self.control_panel_x + 20, y_offset))
        
        # 方向键说明
        y_offset += 45
        spacing = 50
        
        controls = [
            ("↑", "向上移动"),
            ("↓", "向下移动"),
            ("←", "向左移动"),
            ("→", "向右移动"),
        ]
        
        for key, desc in controls:
            self.draw_keyboard_button(key, self.control_panel_x + 20, y_offset)
            text = self.font.render(desc, True, (200, 200, 200))
            self.screen.blit(text, (self.control_panel_x + 70, y_offset + 10))
            y_offset += spacing
        
        # 其他控制键
        y_offset += 20
        other_controls = [
            ("空格键", "暂停游戏"),
            ("R键", "重新开始"),
            ("ESC", "退出游戏")
        ]
        
        for key, desc in other_controls:
            self.draw_keyboard_button(key, self.control_panel_x + 20, y_offset)
            text = self.font.render(desc, True, (200, 200, 200))
            self.screen.blit(text, (self.control_panel_x + 70, y_offset + 10))
            y_offset += spacing

    def draw_game_area(self):
        """绘制游戏区域、网格和边框"""
        # 主背景
        pygame.draw.rect(self.screen, (30, 30, 35),
                        (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # 绘制网格背景
        grid_size = 20
        for x in range(self.game_padding, WINDOW_WIDTH - self.game_padding, grid_size):
            for y in range(self.game_padding, WINDOW_HEIGHT - self.game_padding, grid_size):
                # 交替使用稍深和稍浅的颜色创建棋盘效果
                if (x + y) // grid_size % 2 == 0:
                    color = (35, 35, 40)
                else:
                    color = (32, 32, 37)
                pygame.draw.rect(self.screen, color,
                               (x, y, grid_size, grid_size))
        
        # 外部装饰边框
        border_colors = [
            (120, 120, 140),  # 最外层 - 明亮的边框
            (90, 90, 110),    # 第二层
            (70, 70, 90),     # 第三层
            (50, 50, 70)      # 最内层
        ]
        
        # 绘制渐变边框
        for i, color in enumerate(border_colors):
            pygame.draw.rect(self.screen, color,
                           (i, i,
                            WINDOW_WIDTH - i*2,
                            WINDOW_HEIGHT - i*2),
                           2)
        
        # 内部金属质感边框
        inner_border = 8
        metallic_colors = [
            (130, 130, 150),  # 高光
            (100, 100, 120),  # 主色
            (80, 80, 100),    # 阴影
        ]
        
        for i, color in enumerate(metallic_colors):
            pygame.draw.rect(self.screen, color,
                           (self.game_padding - inner_border + i,
                            self.game_padding - inner_border + i,
                            WINDOW_WIDTH - (self.game_padding - inner_border + i)*2,
                            WINDOW_HEIGHT - (self.game_padding - inner_border + i)*2),
                           2)
        
        # 角落装饰
        corner_size = 20
        corner_thickness = 3
        corner_color = (140, 140, 160)
        corners = [
            # 左上角
            [(self.game_padding - inner_border, self.game_padding - inner_border),
             (self.game_padding - inner_border + corner_size, self.game_padding - inner_border)],
            [(self.game_padding - inner_border, self.game_padding - inner_border),
             (self.game_padding - inner_border, self.game_padding - inner_border + corner_size)],
            
            # 右上角
            [(WINDOW_WIDTH - self.game_padding + inner_border, self.game_padding - inner_border),
             (WINDOW_WIDTH - self.game_padding + inner_border - corner_size, self.game_padding - inner_border)],
            [(WINDOW_WIDTH - self.game_padding + inner_border, self.game_padding - inner_border),
             (WINDOW_WIDTH - self.game_padding + inner_border, self.game_padding - inner_border + corner_size)],
            
            # 左下角
            [(self.game_padding - inner_border, WINDOW_HEIGHT - self.game_padding + inner_border),
             (self.game_padding - inner_border + corner_size, WINDOW_HEIGHT - self.game_padding + inner_border)],
            [(self.game_padding - inner_border, WINDOW_HEIGHT - self.game_padding + inner_border),
             (self.game_padding - inner_border, WINDOW_HEIGHT - self.game_padding + inner_border - corner_size)],
            
            # 右下角
            [(WINDOW_WIDTH - self.game_padding + inner_border, WINDOW_HEIGHT - self.game_padding + inner_border),
             (WINDOW_WIDTH - self.game_padding + inner_border - corner_size, WINDOW_HEIGHT - self.game_padding + inner_border)],
            [(WINDOW_WIDTH - self.game_padding + inner_border, WINDOW_HEIGHT - self.game_padding + inner_border),
             (WINDOW_WIDTH - self.game_padding + inner_border, WINDOW_HEIGHT - self.game_padding + inner_border - corner_size)]
        ]
        
        # 绘制加粗的角落装饰
        for start, end in corners:
            pygame.draw.line(self.screen, corner_color, start, end, corner_thickness)
        
        # 添加内部光晕效果
        glow_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        glow_color = (160, 160, 180, 30)  # 半透明的光晕
        glow_rect = pygame.Rect(
            self.game_padding - 4,
            self.game_padding - 4,
            WINDOW_WIDTH - 2 * (self.game_padding - 4),
            WINDOW_HEIGHT - 2 * (self.game_padding - 4)
        )
        pygame.draw.rect(glow_surface, glow_color, glow_rect, 4)
        self.screen.blit(glow_surface, (0, 0))

    def __init__(self):
        pygame.init()
        # 设置窗口和面板尺寸
        self.window_width = WINDOW_WIDTH + 350
        self.window_height = WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("贪吃蛇")
        
        # 初始化字体 -使用支持中文的字体
        try:
            # 尝试使用系统中文字体
            self.title_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 24)  # 微软雅黑
            self.font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 16)
            self.score_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 28)
        except:
            try:
                # 备选：使用系统默认中文字体
                self.title_font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 24)  # 黑体
                self.font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 16)
                self.score_font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 28)
            except:
                # 如果都失败了，使用系统默认字体
                print("警告：无法加载文字体，可无法正确显示中文")
                self.title_font = pygame.font.SysFont('arial', 24)
                self.font = pygame.font.SysFont('arial', 16)
                self.score_font = pygame.font.SysFont('arial', 28)
        
        # 初始化控制面板尺寸和位置
        self.control_panel_width = 300
        self.control_panel_height = 650
        self.control_panel_x = WINDOW_WIDTH + 25
        self.control_panel_y = 20
        
        # 初始化游戏对象
        self.snake = Snake()
        self.food = Food()
        self.clock = pygame.time.Clock()
        self.speed = 6.0  # 降低初始速度（原来是8.0或更高）
        self.high_score = 0
        
        # 游戏状态
        self.game_over = False
        self.paused = False
        self.show_final_score = False
        
        # 更新游戏区域内边距
        self.game_padding = 20
        
        # 更新游戏区域边界
        self.game_area = {
            'left': self.game_padding,
            'top': self.game_padding,
            'right': WINDOW_WIDTH - self.game_padding,
            'bottom': WINDOW_HEIGHT - self.game_padding
        }

    def reset(self):
        """重置游戏状态"""
        # 保存最高分
        if hasattr(self, 'snake') and self.snake.score > self.high_score:
            self.high_score = self.snake.score
        
        # 重置蛇和食物
        self.snake = Snake()
        self.food = Food()
        self.speed = 6.0  # 降低初始速度（原来是8.0或更高）
        self.game_over = False
        self.show_final_score = False
        self.paused = False

    def check_food_collision(self):
        """检查蛇是否吃到食物，调整速度增长"""
        snake_head = self.snake.positions[0]
        food_grid = self.food.grid_pos
        
        if snake_head == food_grid:
            self.snake.length += 1
            self.snake.score += 10
            if self.speed < 12.0:  # 降低最大速度（原来是15.0）
                self.speed += 0.15  # 降低每次增加的速度（原来是0.2）
            self.reset_food()

    def reset_food(self):
        """重置食物位置，确保不与蛇重叠"""
        while True:
            self.food.reset()
            # 检查新的食物位置是否与蛇身重叠
            if self.food.grid_pos not in self.snake.positions:
                break

    def draw_score(self):
        """在右侧绘制得分面板"""
        # 绘制得分面板背景
        pygame.draw.rect(self.screen, (30, 30, 35),
                        (self.score_panel_x, self.score_panel_y,
                         self.score_panel_width, self.score_panel_height))
        pygame.draw.rect(self.screen, (60, 60, 65),
                        (self.score_panel_x, self.score_panel_y,
                         self.score_panel_width, self.score_panel_height), 2)
        
        # 面板标题
        title = self.title_font.render("得分", True, (255, 255, 255))
        title_rect = title.get_rect(x=self.score_panel_x + 20,
                                  y=self.score_panel_y + 15)
        self.screen.blit(title, title_rect)
        
        # 当前得分
        score_text = self.score_font.render(str(self.snake.score), True, (255, 255, 255))
        score_rect = score_text.get_rect(x=self.score_panel_x + 20,
                                       y=self.score_panel_y + 50)
        self.screen.blit(score_text, score_rect)
        
        # 最高分
        high_score_text = self.font.render(f"最高: {self.high_score}", True, (200, 200, 200))
        high_score_rect = high_score_text.get_rect(x=self.score_panel_x + 20,
                                                 y=self.score_panel_y + 85)
        self.screen.blit(high_score_text, high_score_rect)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:  # 简化R键的判断条件
                    if self.game_over or self.show_final_score:
                        self.reset()
                        continue  # 重新开始后立即进入下一个循环
                elif event.key == pygame.K_SPACE and not self.game_over:
                    self.paused = not self.paused
                elif not self.game_over and not self.paused and not self.show_final_score:
                    if event.key == pygame.K_UP and self.snake.direction != DOWN:
                        self.snake.turn(UP)
                    elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                        self.snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                        self.snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                        self.snake.turn(RIGHT)

    def pause_game(self):
        paused = True
        pause_text = self.font.render('游戏暂停 - 按空格键继续', True, WHITE)
        text_rect = pause_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            
            self.screen.blit(pause_text, text_rect)
            pygame.display.flip()
            self.clock.tick(60)

    def draw_arrow(self, surface, color, direction, x, y, size=20):
        """绘制箭头"""
        if direction == "up":
            points = [(x, y + size), (x + size/2, y), (x + size, y + size)]
        elif direction == "down":
            points = [(x, y), (x + size/2, y + size), (x + size, y)]
        elif direction == "left":
            points = [(x + size, y), (x, y + size/2), (x + size, y + size)]
        elif direction == "right":
            points = [(x, y), (x + size, y + size/2), (x, y + size)]
        
        pygame.draw.polygon(surface, color, points)

    def draw_keyboard_button(self, key, x, y):
        """绘制类似键盘按键的效果"""
        button_width = 40
        button_height = 40
        
        # 按键主体 - 类似键盘按键的颜色
        key_color = (45, 45, 50)
        highlight_color = (65, 65, 70)
        border_color = (30, 30, 35)
        text_color = (220, 220, 220)
        
        # 按键主体
        pygame.draw.rect(self.screen, key_color, 
                        (x, y, button_width, button_height))
        
        # 按键顶部高光
        pygame.draw.rect(self.screen, highlight_color, 
                        (x, y, button_width, button_height//3))
        
        # 按键边框
        pygame.draw.rect(self.screen, border_color, 
                        (x, y, button_width, button_height), 1)

        # 使用简单的箭头符号
        key_symbols = {
            "↑": "↑",
            "↓": "↓",
            "←": "←",
            "→": "→",
            "空格键": "Space",
            "R键": "R",
            "ESC": "Esc"
        }

        symbol = key_symbols.get(key, key)
        
        # 为不同类型的按键选择合适的字体大小
        if symbol == "Space":
            font_size = 16
        else:
            font_size = 20
            
        button_font = pygame.font.SysFont('arial', font_size)
        text = button_font.render(symbol, True, text_color)
        text_rect = text.get_rect(center=(x + button_width//2, y + button_height//2))
        self.screen.blit(text, text_rect)
        
        # 添加按键阴影效果
        shadow_color = (20, 20, 25)
        pygame.draw.line(self.screen, shadow_color,
                        (x, y + button_height),
                        (x + button_width, y + button_height),
                        2)
        pygame.draw.line(self.screen, shadow_color,
                        (x + button_width, y),
                        (x + button_width, y + button_height),
                        2)

    def draw_final_score(self):
        """绘制游戏结束画面"""
        # 创建半透明背景
        s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        # 绘制游戏结束面板
        panel_width = 400
        panel_height = 300
        panel_x = (WINDOW_WIDTH - panel_width) // 2
        panel_y = (WINDOW_HEIGHT - panel_height) // 2
        
        # 面板背景
        pygame.draw.rect(self.screen, (30, 30, 35),
                        (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, (60, 60, 65),
                        (panel_x, panel_y, panel_width, panel_height), 2)
        
        # 游戏结束标题
        title = self.title_font.render("游戏结束", True, (255, 255, 255))
        title_rect = title.get_rect(centerx=WINDOW_WIDTH//2, y=panel_y + 30)
        self.screen.blit(title, title_rect)
        
        # 显示得分
        score_text = self.font.render(f"本局得分: {self.snake.score}", True, (200, 200, 200))
        score_rect = score_text.get_rect(centerx=WINDOW_WIDTH//2, y=panel_y + 100)
        self.screen.blit(score_text, score_rect)
        
        # 显示最高分
        high_score_text = self.font.render(f"最高记录: {self.high_score}", True, (200, 200, 200))
        high_score_rect = high_score_text.get_rect(centerx=WINDOW_WIDTH//2, y=panel_y + 150)
        self.screen.blit(high_score_text, high_score_rect)
        
        # 分割线
        pygame.draw.line(self.screen, (60, 60, 65),
                        (panel_x + 50, panel_y + 200),
                        (panel_x + panel_width - 50, panel_y + 200))
        
        # 操作提示
        hint_text = self.font.render("按 R 键开始新游戏", True, (255, 255, 255))
        hint_rect = hint_text.get_rect(centerx=WINDOW_WIDTH//2, y=panel_y + 230)
        self.screen.blit(hint_text, hint_rect)
        
        quit_text = self.font.render("按 ESC 键退出游戏", True, (150, 150, 150))
        quit_rect = quit_text.get_rect(centerx=WINDOW_WIDTH//2, y=panel_y + 260)
        self.screen.blit(quit_text, quit_rect)

    def run(self):
        running = True
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        elif event.key == pygame.K_SPACE and not self.game_over:
                            self.paused = not self.paused
                        elif event.key == pygame.K_r:
                            # 重置游戏状态
                            self.reset()
                        elif not self.paused and not self.game_over:
                            if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                                self.snake.direction = (0, -1)
                            elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                                self.snake.direction = (0, 1)
                            elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                                self.snake.direction = (-1, 0)
                            elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                                self.snake.direction = (1, 0)

                self.screen.fill(BG_COLOR)
                self.draw_game_area()
                
                if not self.game_over and not self.paused:
                    if not self.snake.update():
                        self.game_over = True
                        self.show_final_score = True
                        # 更新最高分
                        if self.snake.score > self.high_score:
                            self.high_score = self.snake.score
                    else:
                        self.check_food_collision()
                
                self.snake.render(self.screen)
                self.food.render(self.screen)
                self.draw_instructions()
                
                if self.show_final_score:
                    self.draw_final_score()
                elif self.paused:
                    self.draw_pause()
                
                pygame.display.flip()
                self.clock.tick(self.speed)
                
            except Exception as e:
                print("戏发生错误:", str(e))
                running = False
        
        pygame.quit()
        sys.exit()

    def draw_pause(self):
        """绘制暂停界面"""
        # 创建半透明背景
        s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        # 绘制暂停文本
        pause_text = self.title_font.render("游戏暂停", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(pause_text, text_rect)
        
        # 绘制提示文本
        hint_text = self.font.render("按空格键继续游戏", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 40))
        self.screen.blit(hint_text, hint_rect)

if __name__ == '__main__':
    game = Game()
    game.run()
