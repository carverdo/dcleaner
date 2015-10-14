__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

from . import devy
from flask import render_template, request, jsonify


@devy.route('/locn')
def locn():
    return render_template('./device/locn.html')


@devy.route('/orientn')
def orientn():
    return render_template('./device/orientn.html')


@devy.route('/ajaxsub', methods=['GET', 'POST'])
def ajaxsub():
    return render_template('./device/ajax.html')


@devy.route('/test')
def test():
    return render_template('./device/test.html')


@devy.route('/echo/', methods=['GET'])
def echo():
    ret_data = {"value": request.args.get('echoValue')}
    return jsonify(ret_data)



"""
@paym.route('/test')
def test():
    return render_template('test_orient.html')

@paym.route('/indexer')
def indexer():
    return render_template('indexer.html')

@paym.before_request
def before_request():
    flash(request.headers)
    flash(request.headers['Content-Type'])
    flash(request.headers.keys())
    flash(request.headers.values())

    if request.path != '/indexer':
        if request.headers['content-type'].find('application/json'):
            return 'Unsupported Media Type', 415
"""