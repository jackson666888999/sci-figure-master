import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scienceplots

# 关键：先应用样式，再禁用 usetex（顺序不能反！style.use 会覆盖 usetex）
plt.style.use(['science', 'nature'])
plt.rcParams['text.usetex'] = False

# 测试1: Nature 风格线图
fig, ax = plt.subplots(figsize=(3.5, 2.5))
np.random.seed(42)
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label='Group A')
ax.plot(x, np.cos(x), label='Group B')
ax.set_xlabel('Time (h)')
ax.set_ylabel('Value')
ax.legend()
fig.savefig(r'E:\git\sci-figure-master\assets\test_output\nature_style.svg')
plt.close(fig)
print('TEST 1 (line) PASSED')

# 测试2: 火山图
fig, ax = plt.subplots(figsize=(4, 3.5))
n = 500
np.random.seed(7)
log2fc = np.random.normal(0, 1.2, n)
pval = np.random.uniform(0, 1, n)
neg_log10p = -np.log10(pval)
colors = np.where((abs(log2fc) > 1) & (neg_log10p > 1.3), 'red',
         np.where((abs(log2fc) > 1) & (neg_log10p <= 1.3), 'orange', 'grey'))
ax.scatter(log2fc, neg_log10p, c=colors, s=4, alpha=0.7)
ax.axhline(1.3, ls='--', c='grey', lw=0.8)
ax.axvline(1, ls='--', c='grey', lw=0.8)
ax.axvline(-1, ls='--', c='grey', lw=0.8)
ax.set_xlabel('log2(Fold Change)')
ax.set_ylabel('-log10(p-value)')
fig.savefig(r'E:\git\sci-figure-master\assets\test_output\volcano.svg')
plt.close(fig)
print('TEST 2 (volcano) PASSED')

# 测试3: 热图
fig, ax = plt.subplots(figsize=(4, 4))
data = np.random.rand(20, 20)
im = ax.imshow(data, cmap='RdYlBu_r', aspect='auto')
fig.colorbar(im, ax=ax, shrink=0.8)
ax.set_xlabel('Samples')
ax.set_ylabel('Genes')
fig.savefig(r'E:\git\sci-figure-master\assets\test_output\heatmap.svg')
plt.close(fig)
print('TEST 3 (heatmap) PASSED')

# 测试4: 箱线图（cnsplots 风格）
fig, ax = plt.subplots(figsize=(3.5, 3))
np.random.seed(1)
data = [np.random.normal(0, 1, 50), np.random.normal(1.5, 1, 50), np.random.normal(0.5, 1.2, 50)]
bp = ax.boxplot(data, tick_labels=['Ctrl', 'Treat', 'Model'], patch_artist=True)
ax.set_ylabel('Expression')
fig.savefig(r'E:\git\sci-figure-master\assets\test_output\boxplot.svg')
plt.close(fig)
print('TEST 4 (boxplot) PASSED')

print('=== ALL TESTS PASSED ===')
print('matplotlib', matplotlib.__version__)
print('scienceplots OK')
