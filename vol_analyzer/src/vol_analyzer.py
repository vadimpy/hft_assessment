import numpy as np

class VolAnalyzer:

    def comp_slide_win_var(data: np.array, win_len: int) -> np.array:
        nticks = data.shape[0]
        var = np.zeros(nticks)
        cum_var = np.var(data[:win_len])
        cum_sum = np.sum(data[:win_len])
        cum_sum_sqr = np.sum(data[:win_len] ** 2)

        var[win_len - 1] = cum_var
        for i in range(win_len, nticks):
            cum_sum = cum_sum - data[i - win_len] + data[i]
            cum_sum_sqr = cum_sum_sqr - data[i - win_len] ** 2 + data[i] ** 2
            var[i] = cum_sum_sqr / win_len - (cum_sum / win_len) ** 2

        return var

    def comp_slide_win_mean(data: np.array, win_len: int) -> np.array:
        nticks = data.shape[0]
        cum_sum = np.sum(data[:win_len])
        win_mean = np.zeros(nticks)

        win_mean[win_len - 1] = cum_sum / win_len
        for i in range(win_len, nticks):
            cum_sum = cum_sum - data[i - win_len] + data[i]
            win_mean[i] = cum_sum / win_len

        return win_mean
