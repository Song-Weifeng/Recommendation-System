import pandas as pd
import numpy as np

from sklearn.metrics import precision_recall_curve,auc

import matplotlib.pyplot as plt

from sklearn import metrics  ###计算roc和auc

data = pd.read_csv('PR.csv')
score_list = data['sim_value'].values.tolist()
# print(score_list)
test_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1]

y_true = np.array(test_list)
y_score = np.array(score_list)
precision, recall, _thresholds = precision_recall_curve(y_true, y_score)

auc = auc(recall, precision)

lw = 2

plt.figure(figsize=(10, 10), facecolor=(1, 1, 1))

plt.plot(precision, recall, color='darkorange', lw=lw, label=' (AUC = %0.2f)' % auc)  ###假正率为横坐标，真正率为纵坐标做曲线

plt.plot([0, 1], [1, 0], color='navy', lw=lw, linestyle='--')

plt.xlim([0.0, 1.0])

plt.ylim([0.0, 1.0])

# 设置刻度字体大小

plt.xticks(fontsize=15)

plt.yticks(fontsize=15)

plt.xlabel('recall', fontsize=20)

plt.ylabel('precision', fontsize=20)

# plt.title('Receiver operating characteristic example')

plt.legend(loc="upper left")

plt.show()
print(metrics.average_precision_score(y_true, y_score, average='macro', pos_label=1, sample_weight=None))

