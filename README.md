以下是为您的无人机竞赛项目编写的 `README.md` 文档。内容基于您提供的说明文档和四个 Python 程序，适合上传至 GitHub 仓库。

```markdown
# Tello 无人机子赛道竞赛项目

本项目基于 **DJI Tello 无人机** 和 **Tello SDK**，实现了无人机在竞赛子赛道中的四个核心任务：**自主穿环**、**自主巡线**、**自主避障** 与 **自主降落**。通过计算机视觉（OpenCV）与 PID 控制算法，无人机能够根据摄像头实时画面完成全自主飞行。

## 功能简介

| 任务模块 | 功能描述 |
|---------|----------|
| 穿环 (Through) | 检测圆环目标，控制无人机从圆环中心区域穿越。 |
| 巡线 (Line Following) | 识别地面引导线，将画面分区并依据线像素占比调整飞行方向。 |
| 避障 (Obstacle Avoidance) | 检测已知颜色与形状的障碍物，通过 PID 控制左右平移避开障碍。 |
| 自主降落 (Auto Landing) | 搜索降落标志，通过几何计算与区间逼近实现精准降落。 |

## 算法原理简述

### 穿环
- 使用 **霍夫圆环检测** 或固定轨迹飞行。
- 使无人机前置摄像头中心对准圆环圆心，减少碰撞概率。

### 巡线
- 将画面水平分为三份（左、中、右）。
- 通过 HSV 颜色阈值提取引导线，统计各区域线像素占比。
- 根据占比组合（如 `[1,0,0]` 表示仅左侧有线）控制无人机偏航或前进。

### 避障
- 利用障碍物颜色（HSV 范围）生成掩膜，提取最大轮廓。
- 比较轮廓中心与画面中心横坐标：
  - 障碍物偏左 → 向右平移
  - 障碍物偏右 → 向左平移
  - 未检测到障碍物 → 前进
- 使用 **PID 控制器** 平滑平移速度。

### 自主降落
1. **搜索阶段**：旋转扫描，直至检测到降落标志（特定 HSV 颜色范围）。
2. **对准阶段**：先水平移动使标志中心靠近画面中心，再前移使标志靠近画面下边界。
3. **下降阶段**：根据无人机高度 \( H \) 和摄像头下视夹角 \( \theta \)，计算水平位移 \( X = H / \tan\theta \)，向前飞行 \( X \) 后降落。

## 硬件要求

- **DJI Tello 无人机**（或 Tello EDU）
- **运行 Windows / Linux / macOS 的电脑**（需支持 Wi-Fi 连接 Tello）
- Tello 电池（建议多块备用）

## 软件依赖

- Python 3.7+
- OpenCV (`pip install opencv-python`)
- NumPy (`pip install numpy`)
- djitellopy (`pip install djitellopy`)

## 安装与使用

1. **克隆仓库**
   ```bash
   git clone https://github.com/Youxin166/tello-vision-challenges.git
   cd tello-race-project
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```
   （若无 `requirements.txt`，请手动安装上述依赖）

3. **连接 Tello**
   - 开启 Tello 电源
   - 电脑 Wi-Fi 连接至 Tello 热点（如 `TELLO-XXXXXX`）

4. **运行各任务程序**

   - **穿环**：`python through_ring.py`
   - **巡线**：`python line_following.py`
   - **避障**：`python obstacle_avoidance.py`
   - **自主降落**：`python auto_landing.py`

   > 注意：程序默认会执行起飞、任务逻辑与降落。请确保飞行区域空旷、光线良好，设置降落标志。

## 代码结构

```
.
├── through_ring.py          # 项目一：穿环（固定轨迹示例）
├── line_following.py        # 项目二：巡线（HSV阈值 + 分区控制）
├── obstacle_avoidance.py    # 项目三：避障（PID + 颜色检测）
├── auto_landing.py          # 项目四：自主降落（搜索+对准+几何下降）
├── pid.py                   # PID 控制器类（若单独提取）
└── README.md
```

## 参数调整指南

- **HSV 阈值**：在 `line_following.py`、`obstacle_avoidance.py`、`auto_landing.py` 中均有 `hsvVals` 或 `lower_color/upper_color` 变量，请根据实际赛道颜色（如红色引导线、蓝色障碍物）重新标定。
- **PID 参数**：`Kp, Ki, Kd` 影响避障的响应速度与稳定性，建议在安全环境下调试。
- **前进距离**：避障模块中的 `foward <= 400` 及累计方式可根据实际障碍区长调整。

## 常见问题

1. **无人机连接失败**  
   确保电脑已连接 Tello Wi-Fi，且无其他设备占用。可在程序中先执行 `tello.connect()` 并打印电池电量确认。

2. **图像处理延迟**  
   降低 `tello.streamon()` 后的分辨率（如 480×360）可提升帧率。

3. **降落计算不准确**  
   `tanθ` 需要预先通过实验标定。程序中 `tello.move_forward(int (H/0.66))` 中的 `0.66` 为示例值，请根据实测替换。

4. **文件被占用或权限问题**  
   请以管理员身份运行终端，或关闭其他可能占用摄像头的软件。

## 贡献与许可

- 欢迎提交 Issue 或 Pull Request 改进算法。

## 致谢

- DJI 与 Ryze Robotics 提供的 Tello SDK
- `djitellopy` 开源库
- OpenCV 社区

---

**祝飞行顺利，赛出佳绩！** 🚁
```
