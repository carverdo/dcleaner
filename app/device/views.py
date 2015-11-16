__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

from . import devy
from flask import render_template, request, jsonify
from app.db_models import Visit
from app.log_auth.geodata import get_clientdata


@devy.route('/locn')
def locn():
    return render_template('./device/locn.html')


@devy.route('/orientn')
def orientn():
    return render_template('./device/orientn.html')


@devy.route('/motion')
def motion():
    return render_template('./device/motion.html')


@devy.route('/capture')
def capture():
    return render_template('./device/move_capture.html')

@devy.route('/ball')
def ball():
    return render_template('./device/ball.html')

# =================================================
@devy.route('/test')
def test():
    return render_template('./device/test.html')


@devy.route('/test2')
def test2():
    return render_template('./device/test2.html')


@devy.route('/test2echo/', methods=['GET'])
def test2echo():
    ret_data = {'value': request.args.get('echoValue')}
    return jsonify(ret_data)


# =================================================
# CALCULATION SCRIPT
# =================================================
@devy.route('/_clientdata')
def clientdata():
    """
    This function is called by locn_script as it determines client data.
    That data is processed here, and, if desired, sent back.
    """
    # basic client data
    data = get_clientdata()
    # plus, better geographically generated client data (more accurate)
    data['latitude'] = request.args.get('lat', 0, type=float)
    data['longitude'] = request.args.get('long', 0, type=float)
    Visit.create(**data)
    return jsonify(result=data.values())


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