import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import subprocess
import time
import threading

class SimpleBotLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("机器人启动器")
        self.root.geometry("800x600")
        self.root.configure(bg="#f8f9fa")
        
        # 配置文件
        self.config_file = "config.json"
        self.memory_file = "memory.json"
        
        # 进程管理
        self.bot_process = None
        self.is_running = False
        
        # 加载配置
        self.load_config()
        
        # 创建主布局
        self.create_main_layout()
        
        # 状态显示
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = tk.Label(root, textvariable=self.status_var, bg="#2c3e50", fg="white", pady=10)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except Exception as e:
                messagebox.showerror("错误", f"加载配置失败: {e}")
                self.config = self.get_default_config()
        else:
            self.config = self.get_default_config()
            self.save_config()
    
    def get_default_config(self):
        """获取默认配置"""
        return {
            "host": "h.rainplay.cn",
            "port": 26165,
            "username": "dream216",
            "password": "x1x2x3x4x5x6",
            "viewDistance": 100,
            "reconnectAttempts": 5,
            "reconnectDelay": 10000
        }
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {e}")
            return False
    
    def create_main_layout(self):
        """创建主布局"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标签页
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 启动页面
        self.create_launch_tab(notebook)
        
        # 控制页面
        self.create_control_tab(notebook)
        
        # 配置页面
        self.create_config_tab(notebook)
        
        # 记忆页面
        self.create_memory_tab(notebook)
    
    def create_launch_tab(self, notebook):
        """创建启动标签页"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="启动")
        
        # 标题
        title_label = tk.Label(tab, text="机器人启动控制", font=("Microsoft YaHei", 16), bg="#f8f9fa", fg="#2c3e50")
        title_label.pack(pady=20)
        
        # 连接设置
        conn_frame = ttk.LabelFrame(tab, text="连接设置", padding="15")
        conn_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # IP设置
        ip_frame = ttk.Frame(conn_frame)
        ip_frame.pack(fill=tk.X, pady=8)
        
        ttk.Label(ip_frame, text="服务器IP:", width=15).pack(side=tk.LEFT, padx=5)
        self.host_entry = ttk.Entry(ip_frame)
        self.host_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.host_entry.insert(0, self.config.get("host", "h.rainplay.cn"))
        
        # 端口设置
        port_frame = ttk.Frame(conn_frame)
        port_frame.pack(fill=tk.X, pady=8)
        
        ttk.Label(port_frame, text="端口:", width=15).pack(side=tk.LEFT, padx=5)
        self.port_entry = ttk.Entry(port_frame, width=20)
        self.port_entry.pack(side=tk.LEFT, padx=5)
        self.port_entry.insert(0, str(self.config.get("port", 26165)))
        
        # 用户名设置
        user_frame = ttk.Frame(conn_frame)
        user_frame.pack(fill=tk.X, pady=8)
        
        ttk.Label(user_frame, text="机器人名称:", width=15).pack(side=tk.LEFT, padx=5)
        self.username_entry = ttk.Entry(user_frame)
        self.username_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.username_entry.insert(0, self.config.get("username", "dream216"))
        
        # 密码设置
        password_frame = ttk.Frame(conn_frame)
        password_frame.pack(fill=tk.X, pady=8)
        
        ttk.Label(password_frame, text="登录密码:", width=15).pack(side=tk.LEFT, padx=5)
        self.password_entry = ttk.Entry(password_frame, show="*")
        self.password_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.password_entry.insert(0, self.config.get("password", "x1x2x3x4x5x6"))
        
        # 按钮区域
        button_frame = ttk.Frame(conn_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        self.start_btn = ttk.Button(button_frame, text="启动机器人", command=self.start_bot, style="Accent.TButton")
        self.start_btn.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.stop_btn = ttk.Button(button_frame, text="停止机器人", command=self.stop_bot, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.save_btn = ttk.Button(button_frame, text="保存设置", command=self.save_settings)
        self.save_btn.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
    
    def create_config_tab(self, notebook):
        """创建配置标签页"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="配置")
        
        # 标题
        title_label = tk.Label(tab, text="高级配置", font=("Microsoft YaHei", 16), bg="#f8f9fa", fg="#2c3e50")
        title_label.pack(pady=20)
        
        # 配置框架
        config_frame = ttk.LabelFrame(tab, text="配置选项", padding="15")
        config_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # 滚动区域
        canvas = tk.Canvas(config_frame)
        scrollbar = ttk.Scrollbar(config_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 配置项
        config_items = [
            ("viewDistance", "视野距离"),
            ("reconnectAttempts", "重连次数"),
            ("reconnectDelay", "重连延迟(毫秒)")
        ]
        
        self.config_entries = {}
        for key, label in config_items:
            frame = ttk.Frame(scrollable_frame)
            frame.pack(fill=tk.X, pady=10)
            
            ttk.Label(frame, text=label, width=20).pack(side=tk.LEFT, padx=5)
            entry = ttk.Entry(frame)
            entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            entry.insert(0, str(self.config.get(key, "")))
            self.config_entries[key] = entry
        
        # 保存按钮
        save_btn = ttk.Button(scrollable_frame, text="保存所有配置", command=self.save_all_config)
        save_btn.pack(pady=20)
    
    def create_control_tab(self, notebook):
        """创建控制标签页"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="控制")
        
        # 标题
        title_label = tk.Label(tab, text="机器人控制器", font=("Microsoft YaHei", 16), bg="#f8f9fa", fg="#2c3e50")
        title_label.pack(pady=20)
        
        # 添加滚动区域
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        
        # 控制框架
        control_frame = ttk.LabelFrame(canvas, text="完全实时控制", padding="15")
        
        # 配置滚动
        control_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=control_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 移动控制
        move_frame = ttk.LabelFrame(control_frame, text="移动控制", padding="10")
        move_frame.pack(fill=tk.X, pady=10)
        
        # 实时控制说明
        info_label = tk.Label(move_frame, text="按住按键持续控制，释放按键停止控制")
        info_label.pack(pady=5)
        
        # WASD 按钮布局
        move_grid = ttk.Frame(move_frame)
        move_grid.pack(pady=10)
        
        # 移动控制变量
        self.key_states = {
            "w": False,
            "a": False,
            "s": False,
            "d": False,
            "跳": False
        }
        
        # 按键按下和释放事件处理
        def on_key_press(key):
            self.key_states[key] = True
            self.start_realtime_control()
        
        def on_key_release(key):
            self.key_states[key] = False
            if not any(self.key_states.values()):
                self.stop_realtime_control()
        
        # 创建按钮并绑定事件
        for key, row, col in [
            ("w", 0, 1),
            ("a", 1, 0),
            ("s", 1, 1),
            ("d", 1, 2),
            ("跳", 2, 1)
        ]:
            btn = ttk.Button(move_grid, text=key.upper())
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            btn.bind("<ButtonPress-1>", lambda e, k=key: on_key_press(k))
            btn.bind("<ButtonRelease-1>", lambda e, k=key: on_key_release(k))
        
        # 键盘事件绑定
        control_frame.bind("<KeyPress-w>", lambda e: on_key_press("w"))
        control_frame.bind("<KeyPress-a>", lambda e: on_key_press("a"))
        control_frame.bind("<KeyPress-s>", lambda e: on_key_press("s"))
        control_frame.bind("<KeyPress-d>", lambda e: on_key_press("d"))
        control_frame.bind("<KeyPress-space>", lambda e: on_key_press("跳"))
        
        control_frame.bind("<KeyRelease-w>", lambda e: on_key_release("w"))
        control_frame.bind("<KeyRelease-a>", lambda e: on_key_release("a"))
        control_frame.bind("<KeyRelease-s>", lambda e: on_key_release("s"))
        control_frame.bind("<KeyRelease-d>", lambda e: on_key_release("d"))
        control_frame.bind("<KeyRelease-space>", lambda e: on_key_release("跳"))
        
        # 聚焦以接收键盘事件
        control_frame.focus_set()
        
        # 动作控制
        action_frame = ttk.LabelFrame(control_frame, text="动作控制", padding="10")
        action_frame.pack(fill=tk.X, pady=10)
        
        action_grid = ttk.Frame(action_frame)
        action_grid.pack(pady=10)
        
        # 左键按钮 - 只攻击不挖矿
        left_btn = ttk.Button(action_grid, text="左键攻击")
        left_btn.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        def on_left_press(event=None):
            self.send_command("左键")
        
        left_btn.bind("<ButtonPress-1>", on_left_press)
        control_frame.bind("<ButtonPress-1>", on_left_press)
        
        # 右键按钮
        right_btn = ttk.Button(action_grid, text="右键使用")
        right_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        def on_right_press(event=None):
            self.send_command("右键")
        
        right_btn.bind("<ButtonPress-3>", on_right_press)
        control_frame.bind("<ButtonPress-3>", on_right_press)
        
        # 其他按钮
        ttk.Button(action_grid, text="Q丢弃", command=lambda: self.send_command("q")).grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        ttk.Button(action_grid, text="F切换副手", command=lambda: self.send_command("f")).grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
        
        # 物品栏控制
        item_frame = ttk.LabelFrame(action_frame, text="物品栏", padding="10")
        item_frame.pack(fill=tk.X, pady=10)
        
        item_grid = ttk.Frame(item_frame)
        item_grid.pack(pady=10)
        
        for i in range(1, 10):
            ttk.Button(item_grid, text=str(i), command=lambda i=i: self.send_command(str(i))).grid(row=0, column=i-1, padx=3, pady=3, sticky="nsew")
        
        # 模式控制
        mode_frame = ttk.LabelFrame(control_frame, text="模式控制", padding="10")
        mode_frame.pack(fill=tk.X, pady=10)
        
        mode_grid = ttk.Frame(mode_frame)
        mode_grid.pack(pady=10)
        
        ttk.Button(mode_grid, text="守卫", command=lambda: self.send_command("守卫")).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        ttk.Button(mode_grid, text="跟着", command=lambda: self.send_command("跟着")).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Button(mode_grid, text="战斗", command=lambda: self.send_command("战斗")).grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        ttk.Button(mode_grid, text="停止", command=lambda: self.send_command("停止")).grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
        
        # 聊天控制
        chat_frame = ttk.LabelFrame(control_frame, text="聊天与状态", padding="10")
        chat_frame.pack(fill=tk.X, pady=10)
        
        chat_grid = ttk.Frame(chat_frame)
        chat_grid.pack(pady=10, fill=tk.X)
        
        ttk.Label(chat_grid, text="发送消息:", width=10).pack(side=tk.LEFT, padx=5)
        self.chat_entry = ttk.Entry(chat_grid)
        self.chat_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(chat_grid, text="发送", command=self.send_chat_message).pack(side=tk.LEFT, padx=5)
        
        status_grid = ttk.Frame(chat_frame)
        status_grid.pack(pady=10)
        
        ttk.Button(status_grid, text="查看情绪", command=lambda: self.send_command("查看情绪")).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        ttk.Button(status_grid, text="聊家常", command=lambda: self.send_command("聊家常")).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Button(status_grid, text="帮助", command=lambda: self.send_command("帮助")).grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        
        # 记忆查询控制
        memory_frame = ttk.LabelFrame(control_frame, text="记忆查询", padding="10")
        memory_frame.pack(fill=tk.X, pady=10)
        
        memory_grid = ttk.Frame(memory_frame)
        memory_grid.pack(pady=10, fill=tk.X)
        
        ttk.Label(memory_grid, text="记忆类型:", width=10).pack(side=tk.LEFT, padx=5)
        self.memory_type = ttk.Combobox(memory_grid, values=["最近", "聊天", "攻击", "收集", "装备", "死亡", "伤害", "玩家", "方块", "天气", "时间", "经验", "饥饿", "实体", "所有"])
        self.memory_type.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.memory_type.current(0)
        
        ttk.Button(memory_grid, text="查询记忆", command=self.query_memory).pack(side=tk.LEFT, padx=5)
        
        # 投影功能控制
        projection_frame = ttk.LabelFrame(control_frame, text="投影功能", padding="10")
        projection_frame.pack(fill=tk.X, pady=10)
        
        projection_grid = ttk.Frame(projection_frame)
        projection_grid.pack(pady=10, fill=tk.X)
        
        ttk.Label(projection_grid, text="投影文件名:", width=15).pack(side=tk.LEFT, padx=5)
        self.projection_name = ttk.Entry(projection_grid)
        self.projection_name.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(projection_grid, text="创建投影", command=self.create_projection).pack(side=tk.LEFT, padx=5)
        
        # 精打击控制
        pvp_frame = ttk.LabelFrame(control_frame, text="PVP控制", padding="10")
        pvp_frame.pack(fill=tk.X, pady=10)
        
        pvp_grid = ttk.Frame(pvp_frame)
        pvp_grid.pack(pady=10, fill=tk.X)
        
        ttk.Label(pvp_grid, text="目标玩家:", width=10).pack(side=tk.LEFT, padx=5)
        self.pvp_target = ttk.Entry(pvp_grid)
        self.pvp_target.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(pvp_grid, text="精打击", command=self.perform_precise_attack).pack(side=tk.LEFT, padx=5)
        
        # 机器人位置查询
        location_frame = ttk.LabelFrame(control_frame, text="位置查询", padding="10")
        location_frame.pack(fill=tk.X, pady=10)
        
        location_grid = ttk.Frame(location_frame)
        location_grid.pack(pady=10)
        
        ttk.Button(location_grid, text="查询机器人位置", command=lambda: self.send_command("机器人你在哪？")).grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(location_grid, text="玩家名称:", width=10).grid(row=1, column=0, padx=5, pady=5)
        self.player_location = ttk.Entry(location_grid)
        self.player_location.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Button(location_grid, text="查询玩家位置", command=self.query_player_location).grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        
        # 控制状态
        self.control_status_var = tk.StringVar(value="未连接到机器人")
        self.control_status_label = ttk.Label(control_frame, textvariable=self.control_status_var, foreground="red")
        self.control_status_label.pack(pady=10)
        
        # 实时控制定时器
        self.realtime_timer = None
        self.realtime_interval = 100  # 100毫秒发送一次命令
    
    def send_command(self, command):
        """向机器人发送命令"""
        try:
            import socket
            import json
            
            # 创建TCP连接
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("127.0.0.1", 26167))
            
            # 构建命令数据
            command_data = {
                "type": "command",
                "data": {
                    "command": command
                }
            }
            
            # 发送命令
            sock.sendall((json.dumps(command_data) + "\n").encode("utf-8"))
            
            # 关闭连接
            sock.close()
            
            # 更新状态
            self.control_status_var.set(f"命令发送成功: {command}")
            self.control_status_label.configure(foreground="green")
            
        except Exception as e:
            self.control_status_var.set(f"命令发送失败: {e}")
            self.control_status_label.configure(foreground="red")
    
    def start_realtime_control(self):
        """启动实时控制"""
        if not self.realtime_timer:
            self.send_realtime_commands()
    
    def stop_realtime_control(self):
        """停止实时控制"""
        if self.realtime_timer:
            self.realtime_timer.cancel()
            self.realtime_timer = None
    
    def send_realtime_commands(self):
        """发送实时控制命令"""
        # 发送当前按键状态对应的命令
        for key, is_pressed in self.key_states.items():
            if is_pressed:
                self.send_command(key)
        
        # 继续定时发送
        if any(self.key_states.values()):
            self.realtime_timer = self.root.after(self.realtime_interval, self.send_realtime_commands)
    
    def send_chat_message(self):
        """发送聊天消息"""
        message = self.chat_entry.get().strip()
        if message:
            self.send_command(f"说 {message}")
            self.chat_entry.delete(0, tk.END)
    
    def query_memory(self):
        """查询记忆"""
        memory_type = self.memory_type.get()
        self.send_command(f"记忆 {memory_type}")
    
    def create_projection(self):
        """创建投影"""
        projection_name = self.projection_name.get().strip()
        if projection_name:
            self.send_command(f"投影 {projection_name}")
            self.projection_name.delete(0, tk.END)
        else:
            messagebox.showerror("错误", "请输入投影文件名")
    
    def perform_precise_attack(self):
        """执行精打击"""
        target = self.pvp_target.get().strip()
        if target:
            self.send_command(f"精打击 {target}")
            self.pvp_target.delete(0, tk.END)
        else:
            messagebox.showerror("错误", "请输入目标玩家名称")
    
    def query_player_location(self):
        """查询玩家位置"""
        player_name = self.player_location.get().strip()
        if player_name:
            self.send_command(f"{player_name}它在哪呢？")
            self.player_location.delete(0, tk.END)
        else:
            messagebox.showerror("错误", "请输入玩家名称")

    def create_memory_tab(self, notebook):
        """创建记忆标签页"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="记忆")
        
        # 标题
        title_label = tk.Label(tab, text="机器人记忆", font=("Microsoft YaHei", 16), bg="#f8f9fa", fg="#2c3e50")
        title_label.pack(pady=20)
        
        # 记忆框架
        memory_frame = ttk.LabelFrame(tab, text="最近记忆", padding="15")
        memory_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # 搜索框
        search_frame = ttk.Frame(memory_frame)
        search_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(search_frame, text="搜索:", width=10).pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        search_btn = ttk.Button(search_frame, text="搜索", command=self.search_memory)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(search_frame, text="刷新", command=self.load_memory)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # 记忆显示
        self.memory_text = scrolledtext.ScrolledText(memory_frame, wrap=tk.WORD, font=("Microsoft YaHei", 10))
        self.memory_text.pack(fill=tk.BOTH, expand=True)
        
        # 加载记忆
        self.load_memory()
    
    def start_bot(self):
        """启动机器人"""
        if self.is_running:
            messagebox.showinfo("提示", "机器人已经在运行中")
            return
        
        try:
            # 更新配置
            self.save_settings()
            
            # 启动机器人
            self.bot_process = subprocess.Popen(
                ["node", "index.js"],
                cwd=os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8"
            )
            
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_var.set("机器人运行中...")
            
            # 读取输出
            self.output_thread = threading.Thread(target=self.read_output, daemon=True)
            self.output_thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"启动失败: {e}")
    
    def stop_bot(self):
        """停止机器人"""
        if not self.is_running:
            messagebox.showinfo("提示", "机器人未运行")
            return
        
        try:
            self.bot_process.terminate()
            self.bot_process.wait(timeout=5)
            
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_var.set("机器人已停止")
            
        except subprocess.TimeoutExpired:
            self.bot_process.kill()
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_var.set("机器人已强制停止")
        except Exception as e:
            messagebox.showerror("错误", f"停止失败: {e}")
    
    def read_output(self):
        """读取机器人输出"""
        while self.is_running:
            try:
                line = self.bot_process.stdout.readline()
                if not line:
                    break
                print(line.strip())
            except Exception:
                break
        
        # 检查进程是否结束
        if self.is_running:
            self.bot_process.wait()
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_var.set("机器人已停止")
    
    def save_settings(self):
        """保存连接设置"""
        try:
            host = self.host_entry.get().strip()
            port = int(self.port_entry.get())
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()
            
            if not host:
                messagebox.showerror("错误", "IP地址不能为空")
                return
            
            # 更新配置
            self.config["host"] = host
            self.config["port"] = port
            self.config["username"] = username
            self.config["password"] = password
            
            # 保存配置
            if self.save_config():
                # 更新index.js文件
                self.update_index_js()
                messagebox.showinfo("成功", "设置保存成功")
        except ValueError:
            messagebox.showerror("错误", "端口必须是数字")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {e}")
    
    def save_all_config(self):
        """保存所有配置"""
        try:
            # 更新配置
            for key, entry in self.config_entries.items():
                value = entry.get().strip()
                if value:
                    self.config[key] = int(value)
            
            # 保存配置
            if self.save_config():
                messagebox.showinfo("成功", "配置保存成功")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {e}")
    
    def update_index_js(self):
        """更新index.js文件"""
        try:
            with open("index.js", "r", encoding="utf-8") as f:
                content = f.read()
            
            # 更新主连接配置
            content = content.replace(
                f"host: '{self.config.get('host', '')}'",
                f"host: '{self.config['host']}'"
            )
            content = content.replace(
                f"port: {self.config.get('port', '')}",
                f"port: {self.config['port']}"
            )
            content = content.replace(
                f"username: '{self.config.get('username', '')}'",
                f"username: '{self.config['username']}'"
            )
            
            # 更新重连配置
            content = content.replace(
                f"host: '{self.config.get('host', '')}'",
                f"host: '{self.config['host']}'",
                1
            )
            content = content.replace(
                f"port: {self.config.get('port', '')}",
                f"port: {self.config['port']}",
                1
            )
            
            with open("index.js", "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            messagebox.showerror("错误", f"更新配置文件失败: {e}")
    
    def load_memory(self):
        """加载记忆"""
        if not os.path.exists(self.memory_file):
            self.memory_text.delete(1.0, tk.END)
            self.memory_text.insert(tk.END, "还没有记忆数据")
            return
        
        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                memories = json.load(f)
            
            # 显示最近50条
            recent = memories[-50:]
            
            self.memory_text.delete(1.0, tk.END)
            for i, mem in enumerate(recent, 1):
                # 简化时间格式
                time_str = mem["time"].split("T")[1].split(".")[0]
                date_str = mem["time"].split("T")[0]
                
                self.memory_text.insert(
                    tk.END,
                    f"[{i}] {date_str} {time_str} - {mem['content']}\n"
                )
                
        except Exception as e:
            self.memory_text.delete(1.0, tk.END)
            self.memory_text.insert(tk.END, f"加载记忆失败: {e}")
    
    def search_memory(self):
        """搜索记忆"""
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            self.load_memory()
            return
        
        if not os.path.exists(self.memory_file):
            return
        
        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                memories = json.load(f)
            
            # 搜索匹配的记忆
            matched = []
            for mem in memories:
                if keyword in mem["content"].lower() or \
                   keyword in str(mem.get("relatedEntity", "")).lower():
                    matched.append(mem)
            
            # 显示结果
            self.memory_text.delete(1.0, tk.END)
            if matched:
                for i, mem in enumerate(matched[-50:], 1):
                    time_str = mem["time"].split("T")[1].split(".")[0]
                    date_str = mem["time"].split("T")[0]
                    
                    self.memory_text.insert(
                        tk.END,
                        f"[{i}] {date_str} {time_str} - {mem['content']}\n"
                    )
            else:
                self.memory_text.insert(tk.END, "没有找到匹配的记忆")
                
        except Exception as e:
            self.memory_text.delete(1.0, tk.END)
            self.memory_text.insert(tk.END, f"搜索失败: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    # 设置样式
    style = ttk.Style()
    style.configure("Accent.TButton", foreground="white", background="#007bff")
    app = SimpleBotLauncher(root)
    root.mainloop()