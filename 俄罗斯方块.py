import pygame
import random

# 初始化pygame
pygame.init()

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GAME_WIDTH = BLOCK_SIZE * GRID_WIDTH
GAME_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# 计算游戏区域的起始位置（居中）
GAME_X = (WINDOW_WIDTH - GAME_WIDTH) // 2
GAME_Y = (WINDOW_HEIGHT - GAME_HEIGHT) // 2

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# 修改方块形状定义，确保每个形状都是二维列表
SHAPES = [
    [[1, 1, 1, 1],
     [0, 0, 0, 0]],  # I

    [[1, 1],
     [1, 1]],  # O

    [[1, 1, 1],
     [0, 1, 0]],  # T

    [[1, 1, 1],
     [1, 0, 0]],  # L

    [[1, 1, 1],
     [0, 0, 1]],  # J

    [[1, 1, 0],
     [0, 1, 1]],  # S

    [[0, 1, 1],
     [1, 1, 0]]   # Z
]

COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("俄罗斯方块")
        
        # 改进的字体加载方式
        font_paths = [
            "simhei.ttf",  # 当前目录下的黑体
            "C:/Windows/Fonts/simhei.ttf",  # Windows 系统黑体
            "C:/Windows/Fonts/msyh.ttc",    # Windows 系统微软雅黑
            "/System/Library/Fonts/PingFang.ttc",  # macOS 系统字体
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"  # Linux 系统字体
        ]
        
        self.font = None
        self.game_over_font = None
        
        # 尝试加载字体
        for font_path in font_paths:
            try:
                self.font = pygame.font.Font(font_path, 36)
                self.game_over_font = pygame.font.Font(font_path, 48)
                break
            except:
                continue
                
        # 如果所有字体都加载失败，使用系统默认字体
        if self.font is None:
            print("警告：无法加载中文字体，使用系统默认字体")
            self.font = pygame.font.SysFont(None, 36)
            self.game_over_font = pygame.font.SysFont(None, 48)
            
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        # 随机选择一个方块和颜色
        shape_idx = random.randint(0, len(SHAPES) - 1)
        return {
            'shape': [row[:] for row in SHAPES[shape_idx]],  # 创建深拷贝
            'color': COLORS[shape_idx],
            'x': GRID_WIDTH // 2 - len(SHAPES[shape_idx][0]) // 2,
            'y': 0
        }

    def rotate_piece(self):
        # 获取当前方块的形状
        shape = self.current_piece['shape']
        # 创建新的旋转后的形状矩阵
        rows = len(shape)
        cols = len(shape[0])
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        
        # 执行旋转
        for r in range(rows):
            for c in range(cols):
                rotated[c][rows-1-r] = shape[r][c]
        
        # 保存原始形状
        original_shape = self.current_piece['shape']
        self.current_piece['shape'] = rotated
        
        # 如果旋转后的位置无效���则恢复原始形状
        if not self.valid_move(self.current_piece, 0, 0):
            self.current_piece['shape'] = original_shape

    def valid_move(self, piece, x, y):
        for i in range(len(piece['shape'])):
            for j in range(len(piece['shape'][i])):
                if piece['shape'][i][j]:
                    new_x = piece['x'] + j + x
                    new_y = piece['y'] + i + y
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return False
        return True

    def place_piece(self):
        for i in range(len(self.current_piece['shape'])):
            for j in range(len(self.current_piece['shape'][i])):
                if self.current_piece['shape'][i][j]:
                    self.grid[self.current_piece['y'] + i][self.current_piece['x'] + j] = self.current_piece['color']

    def clear_lines(self):
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(cell != 0 for cell in self.grid[y]):
                lines_cleared += 1
                for y2 in range(y, 0, -1):
                    self.grid[y2] = self.grid[y2 - 1][:]
                self.grid[0] = [0] * GRID_WIDTH
            else:
                y -= 1
        return lines_cleared

    def draw(self):
        self.screen.fill(BLACK)
        
        # 绘制游戏区域边框
        pygame.draw.rect(self.screen, WHITE, 
                        (GAME_X - 2, GAME_Y - 2, 
                         GAME_WIDTH + 4, GAME_HEIGHT + 4), 2)

        # 绘制已放置的方块
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, self.grid[y][x],
                                   (GAME_X + x * BLOCK_SIZE,
                                    GAME_Y + y * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # 绘制当前方块
        if not self.game_over:
            for i in range(len(self.current_piece['shape'])):
                for j in range(len(self.current_piece['shape'][i])):
                    if self.current_piece['shape'][i][j]:
                        pygame.draw.rect(self.screen, self.current_piece['color'],
                                       (GAME_X + (self.current_piece['x'] + j) * BLOCK_SIZE,
                                        GAME_Y + (self.current_piece['y'] + i) * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # 修改分数显示
        score_text = self.font.render(f'分数: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = self.game_over_font.render('游戏结束!', True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        fall_time = 0
        fall_speed = 500  # 初始下落速度（毫秒）
        
        while True:
            # 获取每帧的时间增量
            delta_time = self.clock.tick(60)  # 修改这里，获取时间增量
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece, -1, 0):
                            self.current_piece['x'] -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece, 1, 0):
                            self.current_piece['x'] += 1
                    elif event.key == pygame.K_DOWN:
                        if self.valid_move(self.current_piece, 0, 1):
                            self.current_piece['y'] += 1
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        while self.valid_move(self.current_piece, 0, 1):
                            self.current_piece['y'] += 1
                elif event.type == pygame.KEYDOWN and self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()

            if not self.game_over:
                fall_time += delta_time  # 使用实际的时间增量
                if fall_time >= fall_speed:
                    fall_time = 0
                    if self.valid_move(self.current_piece, 0, 1):
                        self.current_piece['y'] += 1
                    else:
                        self.place_piece()
                        lines = self.clear_lines()
                        self.score += lines * 100
                        self.current_piece = self.new_piece()
                        if not self.valid_move(self.current_piece, 0, 0):
                            self.game_over = True

            self.draw()

if __name__ == '__main__':
    game = Tetris()
    game.run()
    pygame.quit()# �����û�������
