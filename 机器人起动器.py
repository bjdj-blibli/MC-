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
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        
        # 设置现代主题颜色
        self.bg_color = "#f0f2f5"
        self.primary_color = "#3498db"
        self.secondary_color = "#2ecc71"
        self.accent_color = "#e74c3c"
        self.text_color = "#2c3e50"
        self.light_text = "#7f8c8d"
        self.white = "#ffffff"
        
        # 配置文件
        self.config_file = "config.json"
        self.memory_file = "memory.json"
        
        # 进程管理
        self.bot_process = None
        self.is_running = False
        
        # 加载配置
        self.load_config()
        
        # 设置样式
        self.setup_styles()
        
        # 创建主布局
        self.create_main_layout()
        
        # 状态显示
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = tk.Label(
            root, 
            textvariable=self.status_var, 
            bg=self.text_color, 
            fg=self.white, 
            pady=10,
            font=("Microsoft YaHei", 10, "bold")
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_styles(self):
        """设置现代样式"""
        style = ttk.Style()
        
        # 设置主题
        style.theme_use("clam")
        
        # 配置标签样式
        style.configure(
            "TLabel",
            font=("Microsoft YaHei", 10),
            foreground=self.text_color,
            background=self.bg_color
        )
        
        # 配置按钮样式
        style.configure(
            "TButton",
            font=("Microsoft YaHei", 10, "bold"),
            padding=(10, 5),
            relief=tk.FLAT
        )
        
        # 配置强调按钮样式
        style.configure(
            "Accent.TButton",
            foreground=self.white,
            background=self.primary_color,
            padding=(12, 6)
        )
        
        # 配置按钮悬停效果
        style.map(
            "Accent.TButton",
            background=[("active", self.secondary_color)],
            foreground=[("active", self.white)]
        )
        
        # 配置标签框架样式
        style.configure(
            "TLabelframe",
            font=("Microsoft YaHei", 11, "bold"),
            foreground=self.text_color,
            background=self.bg_color
        )
        
        # 配置标签框架边框样式
        style.configure(
            "TLabelframe.Label",
            font=("Microsoft YaHei", 11, "bold"),
            foreground=self.primary_color
        )
        
        # 配置输入框样式
        style.configure(
            "TEntry",
            font=("Microsoft YaHei", 10),
            padding=(8, 4),
            relief=tk.FLAT,
            borderwidth=2
        )
        
        # 配置标签页样式
        style.configure(
            "TNotebook",
            background=self.bg_color,
            borderwidth=0
        )
        
        # 配置标签页标签样式
        style.configure(
            "TNotebook.Tab",
            font=("Microsoft YaHei", 10, "bold"),
            padding=(15, 8),
            background="#e0e0e0",
            foreground=self.text_color
        )
        
        # 配置标签页标签悬停效果
        style.map(
            "TNotebook.Tab",
            background=[("active", self.primary_color), ("selected", self.primary_color)],
            foreground=[("active", self.white), ("selected", self.white)]
        )
    
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
        # 设置根窗口背景
        self.root.configure(bg=self.bg_color)
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标签页
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
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
        tab.configure(style="TFrame")
        notebook.add(tab, text="启动")
        
        # 标题
        title_label = tk.Label(
            tab, 
            text="机器人启动控制", 
            font=("Microsoft YaHei", 18, "bold"), 
            bg=self.bg_color, 
            fg=self.primary_color
        )
        title_label.pack(pady=20)
        
        # 连接设置
        conn_frame = ttk.LabelFrame(tab, text="连接设置", padding="20")
        conn_frame.pack(pady=15, padx=30, fill=tk.X)
        
        # IP设置
        ip_frame = ttk.Frame(conn_frame)
        ip_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(ip_frame, text="服务器IP:", width=15).pack(side=tk.LEFT, padx=5)
        self.host_entry = ttk.Entry(ip_frame)
        self.host_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.host_entry.insert(0, self.config.get("host", "h.rainplay.cn"))
        
        # 端口设置
        port_frame = ttk.Frame(conn_frame)
        port_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(port_frame, text="端口:", width=15).pack(side=tk.LEFT, padx=5)
        self.port_entry = ttk.Entry(port_frame, width=20)
        self.port_entry.pack(side=tk.LEFT, padx=5)
        self.port_entry.insert(0, str(self.config.get("port", 26165)))
        
        # 用户名设置
        user_frame = ttk.Frame(conn_frame)
        user_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(user_frame, text="机器人名称:", width=15).pack(side=tk.LEFT, padx=5)
        self.username_entry = ttk.Entry(user_frame)
        self.username_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.username_entry.insert(0, self.config.get("username", "dream216"))
        
        # 密码设置
        password_frame = ttk.Frame(conn_frame)
        password_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(password_frame, text="登录密码:", width=15).pack(side=tk.LEFT, padx=5)
        self.password_entry = ttk.Entry(password_frame, show="*")
        self.password_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.password_entry.insert(0, self.config.get("password", "x1x2x3x4x5x6"))
        
        # 按钮区域
        button_frame = ttk.Frame(conn_frame)
        button_frame.pack(fill=tk.X, pady=25)
        
        self.start_btn = ttk.Button(button_frame, text="启动机器人", command=self.start_bot, style="Accent.TButton")
        self.start_btn.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.stop_btn = ttk.Button(button_frame, text="停止机器人", command=self.stop_bot, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.save_btn = ttk.Button(button_frame, text="保存设置", command=self.save_settings, style="TButton")
        self.save_btn.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
    
    def create_config_tab(self, notebook):
        """创建配置标签页"""
        tab = ttk.Frame(notebook)
        tab.configure(style="TFrame")
        notebook.add(tab, text="配置")
        
        # 标题
        title_label = tk.Label(
            tab, 
            text="高级配置", 
            font=("Microsoft YaHei", 18, "bold"), 
            bg=self.bg_color, 
            fg=self.primary_color
        )
        title_label.pack(pady=20)
        
        # 配置框架
        config_frame = ttk.LabelFrame(tab, text="配置选项", padding="20")
        config_frame.pack(pady=15, padx=30, fill=tk.BOTH, expand=True)
        
        # 滚动区域
        canvas = tk.Canvas(config_frame, bg=self.bg_color)
        scrollbar = ttk.Scrollbar(config_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.configure(style="TFrame")
        
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
            frame.pack(fill=tk.X, pady=12)
            
            ttk.Label(frame, text=label, width=20).pack(side=tk.LEFT, padx=10)
            entry = ttk.Entry(frame)
            entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
            entry.insert(0, str(self.config.get(key, "")))
            self.config_entries[key] = entry
        
        # 保存按钮
        save_btn = ttk.Button(
            scrollable_frame, 
            text="保存所有配置", 
            command=self.save_all_config,
            style="Accent.TButton"
        )
        save_btn.pack(pady=30)
        save_btn.pack_configure(ipadx=20, ipady=5)
    
    def create_control_tab(self, notebook):
        """创建机器人指令大全标签页"""
        tab = ttk.Frame(notebook)
        tab.configure(style="TFrame")
        notebook.add(tab, text="机器人指令大全")
        
        # 标题
        title_label = tk.Label(
            tab, 
            text="机器人指令大全", 
            font=("Microsoft YaHei", 18, "bold"), 
            bg=self.bg_color, 
            fg=self.primary_color
        )
        title_label.pack(pady=20)
        
        # 添加滚动区域
        canvas = tk.Canvas(tab, bg=self.bg_color)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        
        # 指令框架
        command_frame = ttk.LabelFrame(canvas, text="指令列表", padding="20")
        command_frame.configure(style="TLabelframe")
        
        # 配置滚动
        command_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=command_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=15)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 指令分类
        command_categories = {
            "移动控制": [
                ("w", "向前移动"),
                ("s", "向后移动"),
                ("a", "向左移动"),
                ("d", "向右移动"),
                ("跳", "跳跃")
            ],
            "动作控制": [
                ("左键", "攻击实体"),
                ("右键", "使用物品或交互"),
                ("q", "丢弃物品"),
                ("f", "切换副手物品")
            ],
            "物品栏": [
                ("1", "选择物品栏第1格"),
                ("2", "选择物品栏第2格"),
                ("3", "选择物品栏第3格"),
                ("4", "选择物品栏第4格"),
                ("5", "选择物品栏第5格"),
                ("6", "选择物品栏第6格"),
                ("7", "选择物品栏第7格"),
                ("8", "选择物品栏第8格"),
                ("9", "选择物品栏第9格")
            ],
            "模式控制": [
                ("守卫", "守卫当前区域"),
                ("跟着", "跟随玩家"),
                ("战斗", "进入战斗模式"),
                ("停止", "停止当前动作")
            ],
            "聊天与状态": [
                ("说 <内容>", "发送聊天消息"),
                ("查看情绪", "查看机器人当前情绪状态"),
                ("聊家常", "让机器人讲述经历"),
                ("帮助", "显示帮助信息")
            ],
            "记忆查询": [
                ("记忆 最近", "查看最近的记忆"),
                ("记忆 聊天", "查看聊天相关记忆"),
                ("记忆 攻击", "查看攻击相关记忆"),
                ("记忆 收集", "查看收集物品相关记忆"),
                ("记忆 装备", "查看装备相关记忆"),
                ("记忆 死亡", "查看死亡相关记忆"),
                ("记忆 伤害", "查看伤害相关记忆"),
                ("记忆 玩家", "查看玩家相关记忆"),
                ("记忆 方块", "查看方块相关记忆"),
                ("记忆 天气", "查看天气相关记忆"),
                ("记忆 时间", "查看时间相关记忆"),
                ("记忆 经验", "查看经验相关记忆"),
                ("记忆 饥饿", "查看饥饿相关记忆"),
                ("记忆 实体", "查看实体相关记忆"),
                ("记忆 所有", "查看所有记忆")
            ],
            "投影功能": [
                ("投影 <文件名>", "创建投影文件")
            ],
            "PVP控制": [
                ("精打击 <玩家名>", "精确攻击指定玩家")
            ],
            "位置查询": [
                ("机器人你在哪？", "查询机器人当前位置"),
                ("<玩家名>它在哪呢？", "查询指定玩家位置")
            ],
            "白名单管理": [
                ("添加白名单<玩家名>", "添加玩家到白名单（仅管理员）"),
                ("移除白名单<玩家名>", "从白名单移除玩家（仅管理员）"),
                ("查看白名单", "查看当前白名单")
            ]
        }
        
        # 显示指令分类和指令
        for category, commands in command_categories.items():
            # 创建分类框架
            category_frame = ttk.LabelFrame(command_frame, text=category, padding="15")
            category_frame.pack(fill=tk.X, pady=15)
            
            # 创建指令表格
            command_grid = ttk.Frame(category_frame)
            command_grid.pack(fill=tk.X, pady=10)
            
            # 添加指令
            for i, (command, description) in enumerate(commands):
                # 指令标签
                cmd_label = tk.Label(
                    command_grid, 
                    text=command,
                    font=("Microsoft YaHei", 10, "bold"),
                    fg=self.primary_color,
                    bg=self.bg_color
                )
                cmd_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
                
                # 指令描述
                desc_label = tk.Label(
                    command_grid, 
                    text=description,
                    font=("Microsoft YaHei", 10),
                    fg=self.text_color,
                    bg=self.bg_color,
                    wraplength=400,
                    justify=tk.LEFT
                )
                desc_label.grid(row=i, column=1, padx=10, pady=5, sticky="w")
    
    def create_memory_tab(self, notebook):
        """创建记忆标签页"""
        tab = ttk.Frame(notebook)
        tab.configure(style="TFrame")
        notebook.add(tab, text="记忆")
        
        # 标题
        title_label = tk.Label(
            tab, 
            text="机器人记忆", 
            font=("Microsoft YaHei", 18, "bold"), 
            bg=self.bg_color, 
            fg=self.primary_color
        )
        title_label.pack(pady=20)
        
        # 记忆框架
        memory_frame = ttk.LabelFrame(tab, text="最近记忆", padding="20")
        memory_frame.pack(pady=15, padx=30, fill=tk.BOTH, expand=True)
        
        # 搜索框
        search_frame = ttk.Frame(memory_frame)
        search_frame.pack(fill=tk.X, pady=15)
        
        ttk.Label(search_frame, text="搜索:", width=10).pack(side=tk.LEFT, padx=10)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        search_btn = ttk.Button(search_frame, text="搜索", command=self.search_memory, style="Accent.TButton")
        search_btn.pack(side=tk.LEFT, padx=10)
        
        refresh_btn = ttk.Button(search_frame, text="刷新", command=self.load_memory, style="TButton")
        refresh_btn.pack(side=tk.LEFT, padx=10)
        
        # 记忆显示
        self.memory_text = scrolledtext.ScrolledText(
            memory_frame, 
            wrap=tk.WORD, 
            font=("Microsoft YaHei", 10),
            bg=self.white,
            fg=self.text_color,
            relief=tk.FLAT,
            borderwidth=2
        )
        self.memory_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
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