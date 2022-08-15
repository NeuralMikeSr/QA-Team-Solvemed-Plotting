import json
import plotly.graph_objects as go
import os
import numpy as np
from scipy.signal import savgol_filter
from datafetcher import get_bbox_size_IBP, get_diff_IBP, get_stats_IBP

def get_bbox_size(json_file):
    with open(json_file) as f:
        data = json.load(f)
    bbox_size = []
    for i in range(len(data)):
        for j in range(len(data[i]['annotations'])):
            if data[i]['annotations'][j]['label'] == 'IBP':
                bbox_size.append(data[i]['annotations'][j]['coordinates']['width'] * data[i]['annotations'][j]['coordinates']['height'])
                # print(bbox_size)
    return bbox_size

def get_diff(bbox_size):
    diff = []
    for i in range(len(bbox_size)-1):
        diff.append(abs(bbox_size[i+1] - bbox_size[i]))
    return diff

def get_stats(diff):
    mean = np.mean(diff)
    std = np.std(diff)
    return mean, std

def plot_hist(diff):
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=diff,
                               xbins=dict(start=min(diff), end=max(diff), size=20)))
    fig.update_layout(title='Histogram of differences between adjacent frames IBP', title_x=0.5,
                   xaxis_title='Difference IBP [px]',
                   yaxis_title='Number of frames IBP')
    fig.show()

def smooth_plot(bbox_size):
    yhat = savgol_filter(bbox_size, 51, 3)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(yhat))), y=yhat,
                    mode='lines',
                    name='lines'))
    fig.update_layout(title='Bbox size IBP', title_x=0.5,
                   xaxis_title='Frame IBP',
                   yaxis_title='Bbox size IBP [px]')
                   
    fig.show()

def main():
    json_files = os.listdir('C:/Users/48795/Documents/Solvemed/Annotations/13-08-2022/13-08-2022/')
    bbox_size = []
    for json_file in json_files:
        bbox_size.extend(get_bbox_size_IBP('C:/Users/48795/Documents/Solvemed/Annotations/13-08-2022/13-08-2022/' + json_file))
    diff = get_diff_IBP(bbox_size)
    mean, std = get_stats_IBP(diff)
    print('Mean:', mean)
    print('Standard deviation:', std)
    plot_hist(diff)
    smooth_plot(bbox_size)

if __name__ == '__main__':
    main()