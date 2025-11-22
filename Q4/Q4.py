import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def brute_force_closest(points, callback=None):
    min_dist = float('inf')
    pair = None
    n = len(points)
    
    if callback:
        callback(f"brute force checking {n} points", points, None, None)
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(points[i], points[j])
            if (dist < min_dist):
                min_dist = dist
                pair = (points[i], points[j])
    
    return min_dist, pair

def strip_closest(strip, d, callback=None):
    min_dist = d
    pair = None
    strip.sort(key=lambda p: p.y)
    
    if callback:
        callback(f'checking strip with {len(strip)} points', strip, None, min_dist)
    
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and (strip[j].y - strip[i].y) < min_dist:
            dist = distance(strip[i], strip[j])
            if dist < min_dist:
                min_dist = dist
                pair = (strip[i], strip[j])
            j += 1
    
    return min_dist, pair

def closest_pair_recursive(points_x, points_y, callback=None):
    n = len(points_x)
    
    if n <= 3:
        return brute_force_closest(points_x, callback)
    
    mid = n // 2
    mid_point = points_x[mid]
    
    if callback:
        callback(f"dividing {n} points at x={mid_point.x:.2f}", points_x, mid_point, None)
    
    points_y_left = [p for p in points_y if p.x <= mid_point.x]
    points_y_right = [p for p in points_y if p.x > mid_point.x]
    
    left_dist, left_pair = closest_pair_recursive(points_x[:mid], points_y_left, callback)
    right_dist, right_pair = closest_pair_recursive(points_x[mid:], points_y_right, callback)
    
    if left_dist < right_dist:
        min_dist = left_dist
        min_pair = left_pair
    else:
        min_dist = right_dist
        min_pair = right_pair
    
    if callback:
        callback(f'merging: current min = {min_dist:.4f}', None, None, min_dist)
    
    strip = [p for p in points_y if abs(p.x - mid_point.x) < min_dist]
    
    if strip:
        strip_dist, strip_pair = strip_closest(strip, min_dist, callback)
        if (strip_dist < min_dist):
            min_dist = strip_dist
            min_pair = strip_pair
    
    return min_dist, min_pair

def closest_pair(points, callback=None):
    if callback:
        callback(f'starting with {len(points)} points', points, None, None)
    
    points_x = sorted(points, key=lambda p: p.x)
    points_y = sorted(points, key=lambda p: p.y)
    
    return closest_pair_recursive(points_x, points_y, callback)

def karatsuba_multiply(x, y, callback=None, depth=0):
    if x < 10 or y < 10:
        result = x * y
        if callback:
            callback(f"{'  '*depth}base case: {x} x {y} = {result}", x, y, result, depth)
        return result
    
    n = max(len(str(x)), len(str(y)))
    half = n // 2
    power = 10 ** half
    
    high1 = x // power
    low1 = x % power
    high2 = y // power
    low2 = y % power
    
    if callback:
        callback(f"{'  '*depth}split: {x} = {high1}*10^{half} + {low1}", x, y, None, depth)
    
    z0 = karatsuba_multiply(low1, low2, callback, depth + 1)
    z1 = karatsuba_multiply((low1 + high1), (low2 + high2), callback, depth + 1)
    z2 = karatsuba_multiply(high1, high2, callback, depth + 1)
    
    result = z2 * (10 ** (2 * half)) + (z1 - z2 - z0) * power + z0
    
    if callback:
        callback(f"{'  '*depth}combine: result = {result}", x, y, result, depth)
    
    return result

class AlgorithmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Divide & Conquer Visualizer')
        self.root.geometry("1400x900")
        self.root.configure(bg='#f5f5f5')
        
        self.current_algo = "closest_pair"
        self.data = None
        self.result = None
        self.steps = []
        
        self.create_ui()
    
    def create_ui(self):
        header = tk.Frame(self.root, bg='#3b82f6', pady=20)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="Divide & Conquer Algorithm Visualizer", 
                font=('Arial', 26, 'bold'), bg='#3b82f6', fg='white').pack()
        
        tk.Label(header, text='Closest Pair & Karatsuba Multiplication', 
                font=('Arial', 13), bg='#3b82f6', fg='white').pack()
        
        container = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg='#f5f5f5')
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left = tk.Frame(container, bg='white', relief=tk.RAISED, borderwidth=1)
        container.add(left, width=380)
        self.setup_left(left)
        
        right = tk.Frame(container, bg='white', relief=tk.RAISED, borderwidth=1)
        container.add(right)
        self.setup_right(right)
    
    def setup_left(self, parent):
        algo_frame = tk.LabelFrame(parent, text='Select Algorithm', 
                                   font=('Arial', 13, 'bold'), bg='white', 
                                   fg='#3b82f6', padx=15, pady=15)
        algo_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.algo_var = tk.StringVar(value="closest_pair")
        
        tk.Radiobutton(algo_frame, text="Closest Pair of Points", 
                      variable=self.algo_var, value="closest_pair",
                      command=self.algo_changed, font=('Arial', 11),
                      bg='white').pack(anchor=tk.W, pady=5)
        
        tk.Radiobutton(algo_frame, text='Karatsuba Multiplication',
                      variable=self.algo_var, value="karatsuba",
                      command=self.algo_changed, font=('Arial', 11),
                      bg='white').pack(anchor=tk.W, pady=5)
        
        file_frame = tk.LabelFrame(parent, text="Input File",
                                   font=('Arial', 13, 'bold'), bg='white',
                                   fg='#3b82f6', padx=15, pady=15)
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(file_frame, text='Load File', command=self.load_file,
                 font=('Arial', 12, 'bold'), bg='#3b82f6', fg='white',
                 cursor='hand2', padx=25, pady=10).pack(fill=tk.X, pady=5)
        
        self.file_lbl = tk.Label(file_frame, text="no file loaded",
                                font=('Arial', 10), bg='white', fg='gray')
        self.file_lbl.pack(pady=5)
        
        tk.Label(file_frame, text='preview:', font=('Arial', 10, 'bold'),
                bg='white').pack(anchor=tk.W, pady=(10,5))
        
        self.preview = scrolledtext.ScrolledText(file_frame, height=8,
                                                 font=('Courier', 9), bg='#fafafa')
        self.preview.pack(fill=tk.BOTH, pady=5)
        
        tk.Button(file_frame, text="RUN ALGORITHM", command=self.run,
                 font=('Arial', 13, 'bold'), bg='#10b981', fg='white',
                 cursor='hand2', padx=25, pady=12).pack(fill=tk.X, pady=10)
        
        stats_frame = tk.LabelFrame(parent, text='Stats', 
                                    font=('Arial', 13, 'bold'), bg='white',
                                    fg='#3b82f6', padx=15, pady=15)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats = tk.Label(stats_frame, text="run algorithm to see stats",
                             font=('Arial', 10), bg='white', justify=tk.LEFT)
        self.stats.pack(anchor=tk.W)
    
    def setup_right(self, parent):
        self.tabs = ttk.Notebook(parent)
        self.tabs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        results_tab = tk.Frame(self.tabs, bg='white')
        self.tabs.add(results_tab, text='Results')
        
        self.results_txt = scrolledtext.ScrolledText(results_tab, 
                                                     font=('Courier', 11),
                                                     bg='#fafafa', wrap=tk.WORD)
        self.results_txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        viz_tab = tk.Frame(self.tabs, bg='white')
        self.tabs.add(viz_tab, text="Visualization")
        
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        steps_tab = tk.Frame(self.tabs, bg='white')
        self.tabs.add(steps_tab, text='Steps')
        
        self.steps_txt = scrolledtext.ScrolledText(steps_tab, font=('Courier', 10),
                                                   bg='#fafafa', wrap=tk.WORD)
        self.steps_txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def algo_changed(self):
        self.current_algo = self.algo_var.get()
        self.data = None
        self.result = None
        self.file_lbl.config(text='no file loaded')
        self.preview.delete(1.0, tk.END)
        self.clear_all()
    
    def load_file(self):
        file = filedialog.askopenfilename(title="select input file",
                                         filetypes=[("text files", "*.txt"),
                                                   ('all files', "*.*")])
        
        if not file:
            return
        
        try:
            with open(file, 'r') as f:
                content = f.read()
            
            self.file_lbl.config(text=f"loaded: {file.split('/')[-1]}")
            self.preview.delete(1.0, tk.END)
            
            lines = content.split('\n')
            prev = '\n'.join(lines[:20])
            if (len(lines) > 20):
                prev += f"\n... ({len(lines)-20} more lines)"
            
            self.preview.insert(1.0, prev)
            
            if self.current_algo == "closest_pair":
                pts = []
                for line in lines:
                    if line.strip():
                        x, y = map(float, line.strip().split(','))
                        pts.append(Point(x, y))
                self.data = pts
            else:
                nums = [int(line.strip()) for line in lines if line.strip()]
                if len(nums) >= 2:
                    self.data = (nums[0], nums[1])
            
            self.clear_all()
            
        except Exception as e:
            messagebox.showerror('error', f"failed to load:\n{str(e)}")
    
    def run(self):
        if not self.data:
            messagebox.showwarning("no data", 'load a file first')
            return
        
        self.steps = []
        self.results_txt.delete(1.0, tk.END)
        self.steps_txt.delete(1.0, tk.END)
        
        try:
            if self.current_algo == "closest_pair":
                self.run_closest_pair()
            else:
                self.run_karatsuba()
            
            self.tabs.select(0)
            
        except Exception as e:
            messagebox.showerror('error', f"failed:\n{str(e)}")
    
    def run_closest_pair(self):
        self.results_txt.insert(tk.END, "="*60 + "\n")
        self.results_txt.insert(tk.END, 'CLOSEST PAIR ALGORITHM\n')
        self.results_txt.insert(tk.END, "="*60 + "\n\n")
        
        start = time.time()
        
        def callback(msg, pts, mid, dist):
            self.steps.append((msg, pts, mid, dist))
            self.steps_txt.insert(tk.END, f"> {msg}\n")
            self.steps_txt.see(tk.END)
            self.root.update_idletasks()
        
        min_d, pair = closest_pair(self.data, callback)
        end = time.time()
        
        self.result = (min_d, pair)
        
        self.results_txt.insert(tk.END, f'points: {len(self.data)}\n\n')
        self.results_txt.insert(tk.END, f"minimum distance: {min_d:.6f}\n\n")
        self.results_txt.insert(tk.END, f'closest pair:\n')
        self.results_txt.insert(tk.END, f"  p1: {pair[0]}\n")
        self.results_txt.insert(tk.END, f'  p2: {pair[1]}\n\n')
        self.results_txt.insert(tk.END, f"time: {(end-start)*1000:.2f} ms\n")
        
        self.stats.config(text=f'points: {len(self.data)}\nmin dist: {min_d:.4f}\ntime: {(end-start)*1000:.2f} ms')
        
        self.visualize_cp()
    
    def run_karatsuba(self):
        self.results_txt.insert(tk.END, "="*60 + "\n")
        self.results_txt.insert(tk.END, "KARATSUBA MULTIPLICATION\n")
        self.results_txt.insert(tk.END, "="*60 + "\n\n")
        
        n1, n2 = self.data
        start = time.time()
        
        def callback(msg, x, y, res, d):
            self.steps.append((msg, x, y, res))
            self.steps_txt.insert(tk.END, f"{msg}\n")
            if (len(self.steps) % 10 == 0):
                self.steps_txt.see(tk.END)
                self.root.update_idletasks()
        
        res = karatsuba_multiply(n1, n2, callback)
        end = time.time()
        
        self.result = res
        
        self.results_txt.insert(tk.END, f'num1 ({len(str(n1))} digits):\n')
        s1 = str(n1)
        if len(s1) > 100:
            self.results_txt.insert(tk.END, f"{s1[:50]}...{s1[-50:]}\n\n")
        else:
            self.results_txt.insert(tk.END, f"{n1}\n\n")
        
        self.results_txt.insert(tk.END, f"num2 ({len(str(n2))} digits):\n")
        s2 = str(n2)
        if (len(s2) > 100):
            self.results_txt.insert(tk.END, f"{s2[:50]}...{s2[-50:]}\n\n")
        else:
            self.results_txt.insert(tk.END, f"{n2}\n\n")
        
        self.results_txt.insert(tk.END, f'result ({len(str(res))} digits):\n')
        sr = str(res)
        if len(sr) > 100:
            self.results_txt.insert(tk.END, f"{sr[:50]}...{sr[-50:]}\n\n")
        else:
            self.results_txt.insert(tk.END, f"{res}\n\n")
        
        exp = n1 * n2
        ok = res == exp
        self.results_txt.insert(tk.END, f"verification: {'PASS' if ok else 'FAIL'}\n")
        self.results_txt.insert(tk.END, f'time: {(end-start)*1000:.2f} ms\n')
        
        self.stats.config(text=f"digits: {len(str(n1))}, {len(str(n2))}\nresult: {len(str(res))} digits\ntime: {(end-start)*1000:.2f} ms\nverified: {'yes' if ok else 'no'}")
    
    def visualize_cp(self):
        if not self.result or self.current_algo != "closest_pair":
            return
        
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        xs = [p.x for p in self.data]
        ys = [p.y for p in self.data]
        ax.scatter(xs, ys, c='blue', alpha=0.5, s=25)
        
        min_d, pair = self.result
        ax.scatter([pair[0].x, pair[1].x], [pair[0].y, pair[1].y],
                  c='red', s=120, zorder=5, marker='o')
        ax.plot([pair[0].x, pair[1].x], [pair[0].y, pair[1].y],
               'r--', linewidth=2.5)
        
        ax.set_xlabel('x coordinate')
        ax.set_ylabel('y coordinate')
        ax.set_title(f'closest pair visualization (distance = {min_d:.2f})')
        ax.grid(True, alpha=0.3)
        
        self.canvas.draw()
    
    def clear_all(self):
        self.results_txt.delete(1.0, tk.END)
        self.steps_txt.delete(1.0, tk.END)
        self.fig.clear()
        self.canvas.draw()
        self.stats.config(text='run algorithm to see stats')

if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmGUI(root)
    root.mainloop()
