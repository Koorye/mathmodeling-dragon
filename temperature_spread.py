import numpy as np
import matplotlib.pyplot as plt


class Matrix:
    def __init__(self):
        self.row_num, self.col_num = 25, 25
        self.matrix = np.mat(np.zeros(self.row_num * self.col_num)).reshape(self.row_num, self.col_num) + 20
        self.center_pos = (12, 12)

        self.spread_rate = .02

    def cal_diff(self, row_pos, col_pos):
        temperature = self.matrix[row_pos, col_pos]
        temperature_around = 0
        if row_pos >= 1:
            temperature_around += self.matrix[row_pos - 1, col_pos]
        else:
            temperature_around += 20

        if row_pos < self.row_num - 1:
            temperature_around += self.matrix[row_pos + 1, col_pos]
        else:
            temperature_around += 20

        if col_pos >= 1:
            temperature_around += self.matrix[row_pos, col_pos - 1]
        else:
            temperature_around += 20

        if col_pos < self.col_num - 1:
            temperature_around += self.matrix[row_pos, col_pos + 1]
        else:
            temperature_around += 20

        temperature_around /= 4
        return temperature - temperature_around

    def fit(self, temperature_increase=0):
        self.matrix[self.center_pos[0], self.center_pos[1]] += temperature_increase
        new_matrix = np.matrix.copy(self.matrix)
        for i in range(self.row_num):
            for j in range(self.col_num):
                diff = self.cal_diff(i, j)
                new_matrix[i, j] -= diff * self.spread_rate
        self.matrix = new_matrix

    def show(self):
        plt.imshow(self.matrix, cmap=plt.cm.hot, vmin=20, vmax=22.5)
        plt.colorbar()

    def show_24_hours_after_eat(self):
        self.fit(647)
        index = 1
        for j in range(16001):
            self.fit()
            if j % 2000 == 0 and j != 0:
                plt.subplot(2, 4, index)
                plt.title('{} Hours after'.format(3 * index))
                plt.imshow(self.matrix, cmap=plt.cm.hot, vmin=20, vmax=22.5)
                index += 1

        plt.savefig('龙进食 24 小时内的温度变化.png')
        plt.show()

    def show_7_days(self):
        temperature_list = []
        index = 1
        for day in range(7):
            self.fit(647)
            for j in range(16001):
                self.fit()
                if j % 100 == 0 and j != 0:
                    temperature_list.append(self.matrix[self.center_pos[0], self.center_pos[1]])
                if j % 4000 == 0 and j != 0:
                    plt.subplot(7, 4, index)
                    index += 1
                    plt.title('{} Hours after'.format(index * 6))
                    plt.imshow(self.matrix, cmap=plt.cm.hot, vmin=20, vmax=22.5)

        plt.savefig('龙进食一周内的温度变化.png')
        plt.show()

        plt.plot(temperature_list)
        plt.title('Changes in Central Temperature during a Week of Feeding in a Dragon')
        plt.xlabel('Time (Unit: Hours)')
        plt.ylabel('Temperature (Unit: Celsius)')
        plt.savefig('龙进食一周内的中心温度变化.png')
        plt.show()


if __name__ == '__main__':
    matrix = Matrix()
    matrix.show_7_days()
