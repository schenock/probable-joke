#!/usr/bin/env python
import inspect
import os
import random
import sys

import matplotlib.cm as cmx
import matplotlib.colors as colors
import matplotlib.legend as lgd
import matplotlib.markers as mks
import matplotlib.pyplot as plt

random.seed(813)


def get_log_parsing_script():
    dirname = os.path.dirname(os.path.abspath(inspect.getfile(
        inspect.currentframe())))
    return dirname + '/parse_log.sh'


def get_log_file_suffix():
    return '.log'


def get_chart_type_description_separator():
    return '  vs. '


def is_x_axis_field(field):
    x_axis_fields = ['Iters', 'Seconds']
    return field in x_axis_fields


def create_field_index():
    train_key = 'Train'
    test_on_train_key = 'Test_on_Train'
    test_on_test_key = 'Test_on_Test'
    field_index = {
        train_key: {
            'Iters': 0,
            # 'Seconds': 1,
            train_key + ' loss': 1,
            train_key + ' learning rate': 2
        }, test_on_train_key: {
            'Iters': 0,
            # 'Seconds': 1,
            test_on_train_key + ' accuracy1': 1,
            test_on_train_key + ' accuracy5': 2,
            test_on_train_key + ' loss': 3
        }, test_on_test_key: {
            'Iters': 0,
            # 'Seconds': 1,
            test_on_test_key + ' accuracy1': 1,
            test_on_test_key + ' accuracy5': 2,
            test_on_test_key + ' loss': 3
        }
    }
    fields = set()
    for data_file_type in field_index.keys():
        fields = fields.union(set(field_index[data_file_type].keys()))
    fields = list(fields)
    fields.sort()
    return field_index, fields


def get_supported_chart_types():
    field_index, fields = create_field_index()
    num_fields = len(fields)
    supported_chart_types = []
    for i in xrange(num_fields):
        if not is_x_axis_field(fields[i]):
            for j in xrange(num_fields):
                if i != j and is_x_axis_field(fields[j]):
                    supported_chart_types.append('%s%s%s' % (
                        fields[i], get_chart_type_description_separator(),
                        fields[j]))
    return supported_chart_types


def get_chart_type_description(chart_type):
    supported_chart_types = get_supported_chart_types()
    chart_type_description = supported_chart_types[chart_type]
    return chart_type_description


def get_data_file_type(chart_type):
    description = get_chart_type_description(chart_type)
    data_file_type = description.split()[0]
    return data_file_type


def get_data_file(chart_type, path_to_log):
    # return (os.path.basename(path_to_log) + '.' +
    return (path_to_log + '.' +
            get_data_file_type(chart_type).lower())


def get_field_descriptions(chart_type):
    description = get_chart_type_description(chart_type).split(
        get_chart_type_description_separator())
    y_axis_field = description[0]
    x_axis_field = description[1]
    return x_axis_field, y_axis_field


def get_field_indices(x_axis_field, y_axis_field):
    data_file_type = get_data_file_type(chart_type)
    fields = create_field_index()[0][data_file_type]
    return fields[x_axis_field], fields[y_axis_field]


def load_data(data_file, field_idx0, field_idx1):
    data = [[], []]
    last_fields = -1
    with open(data_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line[0] != '#':
                fields = line.split()
                if len(fields) == last_fields or last_fields == -1:
                    last_fields = len(fields)
                    data[0].append(float(fields[field_idx0].strip()))
                    data[1].append(float(fields[field_idx1].strip()))
                else:
                    print "Read until:"
                    print "\t", line
                    break
    return data


def random_marker():
    markers = mks.MarkerStyle.markers
    num = len(markers.keys())
    idx = random.randint(0, num - 1)
    return markers.keys()[idx]


def get_data_label(path_to_log):
    label = path_to_log[path_to_log.rfind('/') + 1: path_to_log.rfind(
        get_log_file_suffix())]
    label = label.split('.')[-3:-2]
    name=label[0]
    label[0]=name[8:]
    return label


def get_legend_loc(chart_type):
    x_axis, y_axis = get_field_descriptions(chart_type)
    loc = 'lower right'
    if y_axis.find('accuracy') != -1:
        pass
    if y_axis.find('loss') != -1 or y_axis.find('learning rate') != -1:
        loc = 'upper right'
    return loc


def plot_chart(chart_type, png_prefix, path_to_log_list):
    for path_to_log in path_to_log_list:
        os.system('%s %s' % (get_log_parsing_script(), path_to_log))
        data_file = get_data_file(chart_type, path_to_log)
        x_axis_field, y_axis_field = get_field_descriptions(chart_type)
        x, y = get_field_indices(x_axis_field, y_axis_field)
        data = load_data(data_file, x, y)
        # TODO: more systematic color cycle for lines
        color = [random.random(), random.random(), random.random()]
        label = get_data_label(path_to_log)
        linewidth = 0.75
        # If there too many datapoints, do not use marker.
        use_marker = False
	if(str(chart_type)=="0"):
		#ind_min_2000=len(filter(lambda x: x<2000,data[0]))
		#data[0]=data[0][:ind_min_2000]
		#data[1]=data[1][:ind_min_2000]
		max_acc=max(data[1])
		ind=data[1].index(max_acc)
		iter_max_acc=data[0][ind]
		print(path_to_log,iter_max_acc,max_acc)
        label_plot = label[0].replace('_', ' ')
        if not use_marker:
            plt.plot(data[0], data[1], label=label_plot, color=color,
                     linewidth=linewidth)
	    #, alpha=1. / len(path_to_log_list)
        else:
            marker = random_marker()
            plt.plot(data[0], data[1], label=label_plot, color=color,
                     marker=marker, linewidth=linewidth)
    legend_loc = get_legend_loc(chart_type)
    plt.legend(loc=legend_loc, ncol=1)  # ajust ncol to fit the space
    plt.title(get_chart_type_description(chart_type).replace('_', ' '))
    plt.xlabel(x_axis_field.replace('_', ' '))
    plt.ylabel(y_axis_field.replace('_', ' '))
    filename = ' '.join(get_chart_type_description(chart_type).split()).replace(
        ' ', '_').replace('.', '').lower() + '.png'
    path_to_png = os.path.join(png_prefix, filename)
    plt.savefig(path_to_png)
    # plt.show()


def print_help():
    print """This script mainly serves as the basis of your customizations.
Customization is a must.
You can copy, paste, edit them in whatever way you want.
Be warned that the fields in the training log may change in the future.
You had better check the data files and change the mapping from field name to
 field index in create_field_index before designing your own plots.
Usage:
    ./plot_training_log.py chart_type[0-%s] /where/to/save/png_prefix /path/to/first.log ...
Notes:
    1. Supporting multiple logs.
    2. Log file name must end with the lower-cased "%s".
Supported chart types:""" % (len(get_supported_chart_types()) - 1,
                             get_log_file_suffix())
    supported_chart_types = get_supported_chart_types()
    num = len(supported_chart_types)
    for i in xrange(num):
        print '    %d: %s' % (i, supported_chart_types[i])
    sys.exit()


def is_valid_chart_type(chart_type):
    return chart_type >= 0 and chart_type < len(get_supported_chart_types())


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print_help()
    else:
        chart_type = int(sys.argv[1])
        if not is_valid_chart_type(chart_type):
            print '%s is not a valid chart type.' % chart_type
            print_help()
        png_prefix = sys.argv[2]
        # if not png_prefix.endswith('.png'):
        #     print 'Path must ends with png' % png_prefix
        #     sys.exit()
        path_to_logs = sys.argv[3:]
        for path_to_log in path_to_logs:
            if not os.path.exists(path_to_log):
                print 'Path does not exist: %s' % path_to_log
                sys.exit()
            if not path_to_log.endswith(get_log_file_suffix()):
                print 'Log file must end in %s.' % get_log_file_suffix()
                print_help()
        # plot_chart accpets multiple path_to_logs
        plot_chart(chart_type, png_prefix, path_to_logs)
