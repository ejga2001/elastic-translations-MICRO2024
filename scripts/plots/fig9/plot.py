#!/usr/bin/env python

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

# Estilo global
plt.style.use('ggplot')
sns.set_style("whitegrid")

def rgb2hex(c):
	return "#{:02x}{:02x}{:02x}".format(int(c[0]*255), int(c[1]*255), int(c[2]*255))

def make_rgb_transparent(rgb, bg_rgb, alpha):
	return [alpha * c1 + (1 - alpha) * c2 for (c1, c2) in zip(rgb, bg_rgb)]

def prep_df(df, name):
	df = df.stack().reset_index()
	df.columns = ['c1', 'c2', 'values']
	df['Size'] = name
	return df

def main():
	# Colores
	palete = sns.color_palette("Paired")
	ours = make_rgb_transparent(palete[5], (1, 1, 1), 0.8)

	colors = {
		"4KiB": palete[1],
		"THP": palete[6],
		"HugeTLB": palete[2],
		"ET-aggr": ours,
		"ET-heap": ours,
		"ET-leshy": ours,
		"64KiB": make_rgb_transparent(palete[1], (1, 1, 1), 0.3),
		"2MiB": palete[6],
		"32MiB": make_rgb_transparent(palete[6], (1, 1, 1), 0.3)
	}

	benchmarks = ["stream", "astar", "omnet", "bfs", "canneal", "xsbench", "btree", "svm", "hashjoin", "gups"]
	df_all = {}

	for name in benchmarks:
		print(name)
		file_map = {
			"stream": "streamcluster",
			"omnet": "omnetpp",
			"PageRank": "pagerank",
			"xsb": "xsbench"
		}
		filename = file_map.get(name, name)
		df_all[name] = pd.read_csv(f"./{filename}.csv", skipinitialspace=True, index_col=0)
		df_all[name] = df_all[name].dropna().apply(pd.to_numeric)

		footprint = df_all[name]["4KiB"]["4KiB"] * 4096
		df_all[name]["4KiB"] = df_all[name]["4KiB"] * 4096 * 100 / footprint
		df_all[name]["64KiB"] = df_all[name]["64KiB"] * 16 * 4096 * 100 / footprint
		df_all[name]["2MiB"] = df_all[name]["2MiB"] * 512 * 4096 * 100 / footprint
		df_all[name]["32MiB"] = df_all[name]["32MiB"] * 16 * 512 * 4096 * 100 / footprint

		df_all[name].drop('4KiB', inplace=True)
		df_all[name].rename(index={'ET-Leshy-offline': 'ET-L-offline'}, inplace=True)

	def build_df(size):
		df_size = pd.DataFrame(index=benchmarks, columns=df_all["astar"].index, dtype=object)
		for name in benchmarks:
			column = df_all[name][size].values
			for i, idx in enumerate(df_size.columns):
				df_size.loc[name, idx] = column[i]
		return df_size

	df4K = build_df("4KiB")
	df64K = build_df("64KiB")
	df2M = build_df("2MiB")
	df32M = build_df("32MiB")

	df_all_sizes = pd.concat([
		prep_df(df4K, '4KiB'),
		prep_df(df64K, '64KiB'),
		prep_df(df2M, '2MiB'),
		prep_df(df32M, '32MiB')
	])

	df_all_sizes['order'] = df_all_sizes['Size'].replace(
		{val: i for i, val in enumerate(['4KiB', '64KiB', '2MiB', '32MiB'])}
	)

	alt.Chart(df_all_sizes).mark_bar(
		size=17, stroke='black', filled=True, strokeWidth=3, clip=True
	).encode(
		x=alt.X('c2:N', title=None, sort=benchmarks),
		y=alt.Y('sum(values):Q', axis=alt.Axis(grid=True, title="Distribution of translation sizes (%)", titleFontSize=38, titleFontWeight='normal')),
		column=alt.Column('c1:N', title=None, sort=benchmarks),
		color=alt.Color(
			'Size:N',
			scale=alt.Scale(range=[rgb2hex(colors["32MiB"]), rgb2hex(colors["2MiB"]), rgb2hex(colors["64KiB"]), rgb2hex(colors["4KiB"])]),
			sort=["32MiB", "2MiB", "64KiB", "4KiB"]
		),
		order='order'
	).properties(
		width=95, height=320
	).configure_header(
		labelFontSize=28, labelAngle=0, labelBaseline='line-top'
	).configure_legend(
		labelFontSize=34, titleFontSize=34, legendX=320, legendY=-115,
		direction='horizontal', orient='none', title=None
	).configure_axis(
		labelFontSize=20
	).configure_view(
		strokeOpacity=0
	).save("pagedistr.png", engine="vl-convert")

if __name__ == "__main__":
	main()
