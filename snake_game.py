import tkinter as tk
import random
import time

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("贪吃蛇游戏")
        self.master.geometry("600x600")
        self.master.resizable(False, False)
        self.master.config(bg="black")
        
        # 游戏变量
        self.width = 600
        self.height = 600
        self.grid_size = 20
        self.snake_speed = 150  # 毫秒
        
        # 创建画布
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack()
        
        # 创建得分标签
        self.score_var = tk.StringVar()
        self.score_var.set("得分: 0")
        self.score_label = tk.Label(self.master, textvariable=self.score_var, fg="white", bg="black", font=("Arial", 14))
        self.score_label.place(x=10, y=10)
        
        # 初始化游戏
        self.reset_game()
        
        # 绑定按键
        self.master.bind("<Up>", lambda event: self.change_direction("up"))
        self.master.bind("<Down>", lambda event: self.change_direction("down"))
        self.master.bind("<Left>", lambda event: self.change_direction("left"))
        self.master.bind("<Right>", lambda event: self.change_direction("right"))
        self.master.bind("<space>", lambda event: self.toggle_pause())
        self.master.bind("<Return>", lambda event: self.restart_game() if self.game_over else None)
        
        # 开始游戏循环
        self.update()
    
    def reset_game(self):
        # 重置游戏状态
        self.snake = [(self.width // 2, self.height // 2)]
        self.snake_direction = "right"
        self.next_direction = "right"
        self.food = self.create_food()
        self.score = 0
        self.score_var.set(f"得分: {self.score}")
        self.game_over = False
        self.paused = False
        self.game_over_text = None
        self.restart_text = None
        
    def create_food(self):
        # 创建食物，确保不在蛇身上
        while True:
            x = random.randint(0, (self.width - self.grid_size) // self.grid_size) * self.grid_size
            y = random.randint(0, (self.height - self.grid_size) // self.grid_size) * self.grid_size
            if (x, y) not in self.snake:
                return (x, y)
    
    def change_direction(self, direction):
        # 改变蛇的方向，但不允许直接反向
        if self.game_over or self.paused:
            return
            
        if direction == "up" and self.snake_direction != "down":
            self.next_direction = "up"
        elif direction == "down" and self.snake_direction != "up":
            self.next_direction = "down"
        elif direction == "left" and self.snake_direction != "right":
            self.next_direction = "left"
        elif direction == "right" and self.snake_direction != "left":
            self.next_direction = "right"
    
    def toggle_pause(self):
        # 暂停/继续游戏
        if not self.game_over:
            self.paused = not self.paused
            if self.paused:
                self.pause_text = self.canvas.create_text(self.width // 2, self.height // 2, 
                                                        text="游戏暂停", fill="white", font=("Arial", 24))
            else:
                self.canvas.delete(self.pause_text)
    
    def move_snake(self):
        # 根据方向移动蛇
        self.snake_direction = self.next_direction
        head_x, head_y = self.snake[0]
        
        if self.snake_direction == "up":
            new_head = (head_x, head_y - self.grid_size)
        elif self.snake_direction == "down":
            new_head = (head_x, head_y + self.grid_size)
        elif self.snake_direction == "left":
            new_head = (head_x - self.grid_size, head_y)
        elif self.snake_direction == "right":
            new_head = (head_x + self.grid_size, head_y)
        
        # 检查是否吃到食物
        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.score += 10
            self.score_var.set(f"得分: {self.score}")
            self.food = self.create_food()
            # 每得100分加快速度
            if self.score % 100 == 0 and self.snake_speed > 50:
                self.snake_speed -= 10
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()
        
        # 检查是否撞墙或撞到自己
        if (new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height or
            new_head in self.snake[1:]):
            self.game_over = True
    
    def draw_objects(self):
        # 清空画布
        self.canvas.delete("all")
        
        # 绘制蛇
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + self.grid_size, y + self.grid_size, fill="green", outline="")
        
        # 绘制蛇头（不同颜色）
        head_x, head_y = self.snake[0]
        self.canvas.create_rectangle(head_x, head_y, head_x + self.grid_size, head_y + self.grid_size, 
                                    fill="dark green", outline="")
        
        # 绘制食物
        food_x, food_y = self.food
        self.canvas.create_oval(food_x, food_y, food_x + self.grid_size, food_y + self.grid_size, 
                                fill="red", outline="")
        
        # 如果游戏结束，显示游戏结束文本
        if self.game_over:
            self.game_over_text = self.canvas.create_text(self.width // 2, self.height // 2 - 30, 
                                                        text=f"游戏结束! 得分: {self.score}", 
                                                        fill="white", font=("Arial", 24))
            self.restart_text = self.canvas.create_text(self.width // 2, self.height // 2 + 30, 
                                                        text="按回车键重新开始", 
                                                        fill="white", font=("Arial", 18))
    
    def restart_game(self):
        # 重新开始游戏
        self.canvas.delete("all")
        self.reset_game()
    
    def update(self):
        # 游戏主循环
        if not self.game_over and not self.paused:
            self.move_snake()
        
        self.draw_objects()
        
        # 继续游戏循环
        self.master.after(self.snake_speed, self.update)

def main():
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()