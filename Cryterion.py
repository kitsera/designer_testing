class Cryterion:

    def __init__(self, params):
        self.params = params
        self.result = self.calc_result()

    def calc_result(self):
        pass

    def get_result(self):
        return self.result


class Vald(Cryterion):

    def calc_result(self):
        reserve = []
        for i in range(len(self.params)):
            reserve.append(min(self.params[i]))
        return reserve


class Gulvic(Cryterion):

    def calc_result(self):
        reserve = []
        x = 0.5
        for i in range(len(self.params)):
            maxi = max(self.params[i])
            mini = min(self.params[i])

            reserve.append(mini*x + maxi*(1-x))
        return reserve


class Laplas(Cryterion):

    def calc_result(self):
        reserve = []
        for i in range(len(self.params)):
            reserve.append(sum(self.params[i])/len(self.params[i]))
        return reserve


class Bayes_Laplas(Cryterion):

    def calc_result(self):
        reserve = []
        p = [0.5, 0.35, 0.15]
        for i in range(len(self.params)):
            reserve.append(sum(list(map(lambda x: x[0]*x[1], zip(p, self.params[i])))))
        return reserve