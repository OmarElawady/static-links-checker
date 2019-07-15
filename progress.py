class ProgressBar:
    def __init__(self, count):
        self.bars = []
        self.data = []
        self.count = count

    def get_id(self, data):
        self.bars.append([-1, -1])
        self.data.append(data)
        return len(self.bars) - 1

    def set_start(self, index, tim):
        #self.remaining += 1
        self.bars[index][0] = tim

    def set_end(self, index, tim):
        self.count -= 1
        self.bars[index][1] = tim
        if self.count == 0:
            self.print()
    def set_count(self, count):
        self.count = count

    def get_bar_string(self, bar, mn, mx):
        bar_length = (bar[1] - bar[0]) / (mx - mn) * 142
        bar_offset = (bar[0] - mn) / (mx - mn) * 142
        #print(str(bar[0]) + " " + str(bar[1]))
        #print(str(mn) + " " + str(mx))
        return ' ' * round(bar_offset) + '█' * round(bar_length)

    def print(self):
        mn_bound = 100000000000000000000000
        mx_bound = 0
        for bar in self.bars:
            #print(bar[0])
            mn_bound = min(mn_bound, bar[0])
            mx_bound = max(mx_bound, bar[1])
        for i in range(len(self.bars)):
            print(self.data[i])
            print(self.get_bar_string(self.bars[i], mn_bound, mx_bound))

p = ProgressBar(10000)
