import numpy as np
from scipy.spatial.distance import pdist

x = np.random.random(10)
y = np.random.random(10)

# 根据scipy库求解余弦相似度
X = np.vstack([x, y])
Y = np.vstack([y, x])

d1x = 1 - pdist(X, 'cosine')
d1y = 1 - pdist(Y, 'cosine')
# 根据numpy库求解皮尔逊相似度
d2 = np.corrcoef(X)[0][1]
print(X)
print(Y)
print(d1x)
print(d1y)

