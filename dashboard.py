from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.plotting import figure, save
from bokeh.models import Legend

def format_output_name(name):
	if name.endswith('.html'):
		return name
	else:
		return name + '.html'

def show_data(true_pos, false_neg, true_neg, false_pos, output='output'):

	#	Pre-processing Data.
	samples = ['Matching of Positive Images', 'Matching of Negative Images']
	years = ['Good', 'Bad']
	colors = ["#67BF5C", "#ED665D"]

	data = {
		'samples' : samples,
		'Good'   : [true_pos, true_neg],
		'Bad'   : [false_neg, false_pos]
	}

	#	Create the figure in which we will plot.
	p = figure(x_range=samples, plot_height=250, title="Score",
	           toolbar_location=None, tools="hover", tooltips="$name")

	#	Displays the barplot
	renderers = p.vbar_stack(years, x='samples', width=0.5, color=colors, source=data)

	#	Plot settings
	p.y_range.start = 0
	p.x_range.range_padding = 0.1
	p.xgrid.grid_line_color = None
	p.axis.minor_tick_line_color = None
	p.outline_line_color = None

	#	This is done to place the legend outside the plot.
	legend = Legend(items= [('Good', [renderers[0]]),
							('Bad', [renderers[1]])
					],
					location=(20, 0),
					orientation='horizontal')
	p.add_layout(legend, 'above')

	#	Specifies in which file we want to save our figure.
	output_file( format_output_name(output) )

	#	Opens and save the html file previously specified.
	#	If you only want to save the html without open it, do...
	# save(p)
	show(p)

if __name__ == '__main__':
	show_data(
		true_pos = 15,
		false_neg = 23,
		true_neg = 11,
		false_pos = 5
	)