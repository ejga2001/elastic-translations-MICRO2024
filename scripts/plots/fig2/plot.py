import matplotlib
matplotlib.use('Agg')  # <-- añadir esto aquí

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Estilo claro
plt.style.use('default')

def load_and_normalize(csv_path):
	df = pd.read_csv(csv_path, index_col=0)
	df = df.apply(pd.to_numeric)
	df["64KiB"] = df["4KiB"]/df["64KiB"]
	df["2MiB"] = df["4KiB"]/df["2MiB"]
	df["32MiB"] = df["4KiB"]/df["32MiB"]
	df = df.drop(columns='4KiB')
	#normalized = df.div(df['4KiB'], axis=0)
	#normalized = normalized.drop(columns='4KiB')
	return df

def plot_figure(host_df, vm_df):
	fig, axs = plt.subplots(2, 2, figsize=(10, 8))
	fig.subplots_adjust(hspace=0.3, wspace=0.3)

	benchmarks_groups = [
		(["Astar", "Omnetpp", "Streamcluster"], host_df, "Native"),
		(["Astar", "Omnetpp", "Streamcluster"], vm_df, "Virtualized"),
		(["Canneal", "SVM", "Hashjoin"], host_df, ""),
		(["Canneal", "SVM", "Hashjoin"], vm_df, ""),
	]

	colors = ['#4f81bd', '#f4b183', '#c55a11', '#c00000']  # 64KiB, 2MiB, 32MiB, 1GB
	hatches = ['/', '', '//', 'xx']
	labels = ['64KiB', '2MiB', '32MiB']

	for ax, (benches, df, title) in zip(axs.flatten(), benchmarks_groups):
		data = df.loc[benches]
		data.index = [name.lower() for name in data.index]
		bar_width = 0.2
		x = np.arange(len(data))
		print(data.columns)
		for i, column in enumerate(data.columns):
			bars = ax.bar(x + i * bar_width, data[column], width=bar_width,
						  color=colors[i], hatch=hatches[i], label=labels[i], edgecolor='black')
			# Añadimos los números encima de las barras
			for bar in bars:
				height = bar.get_height()
				ax.annotate(f'{height:.2f}',
							xy=(bar.get_x() + bar.get_width() / 2, height),
							xytext=(0, 5),
							textcoords="offset points",
							ha='center', va='bottom', fontsize=7)

		ax.set_xticks(x + bar_width * 1.5)
		ax.set_xticklabels(data.index, fontsize=10)
		ax.set_ylim(0.9, 2.1)
		if title:
			ax.set_title(title, fontsize=12)
		if ax in [axs[0, 0], axs[1, 0]]:
			ax.set_ylabel('Speedup normalized to 4KiB', fontsize=10)

	handles, labels = axs[0, 0].get_legend_handles_labels()
	fig.legend(handles, labels, loc='lower center', ncol=4, fontsize=10)
	fig.suptitle('Performance Speedup Comparison', fontsize=14)
	plt.savefig('speedup_comparison.pdf', bbox_inches='tight')
	plt.savefig('speedup_comparison.png', bbox_inches='tight')
	plt.savefig('speedup_comparison.eps', format='eps', bbox_inches='tight')
	plt.show()

def main():
	host_df = load_and_normalize('cycles.host.csv')
	vm_df = load_and_normalize('cycles.vm.csv')
	plot_figure(host_df, vm_df)

if __name__ == "__main__":
	main()
