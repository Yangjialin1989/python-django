import threading
import time


class CountdownTimer:
    def __init__(self, duration):
        self.duration = duration
        self.running = False
        self.start_time = None

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            threading.Thread(target=self.countdown).start()

    def countdown(self):
        while self.running:
            remaining = self.duration - (time.time() - self.start_time)
            if remaining <= 0:
                self.running = False
                print("时间到！")
                break
            else:
                print(f"剩余时间: {remaining:.2f}秒")
                tt = 'hhhh'
                return tt
                time.sleep(1)

# 使用示例
# timer = CountdownTimer(10)  # 创建一个10秒的倒计时
# timer.start()               # 开始倒计时