__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

from . import devy
from flask import render_template, request, jsonify, current_app, flash
from app.db_models import Visit, MotionCapture
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


@devy.route('/balltable', methods=['GET', 'POST'])
def balltable():
    # Presentation of group/summary data
    all_balldata = MotionCapture.query.order_by(MotionCapture.id).all()
    patex = current_app.config['PAHDS']['balldata']
    tadata = current_app.config['TADATA']['balldata']
    endpoint, kwargs = '', {}
    return render_template('panelbuilder.html',
                           form=all_balldata,
                           endpoint=endpoint,
                           panel_args=dict(
                               patex=patex,
                               tadata=tadata,
                               wid=12
                           ),
                           kwargs=kwargs
                           )

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
# CALCULATION SCRIPTS
# USED FOR OUR AJAX REQUESTS
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


@devy.route('/_balldata')
def balldata():
    """
    Use request args to CAPTURE or DELETE row of data.
    """
    data = {}
    # delete vs capture
    if 'strMemID' in request.args.keys():
        data['memID'] = request.args.get('strMemID', 0, type=int)
        try:
            MotionCapture.get(data['memID']).delete()
        except:  # if request.args.get produces gibberish
            pass
    else:
        data['acx'] = request.args.get('strAcx', '[0]', type=str)
        data['acy'] = request.args.get('strAcy', '[0]', type=str)
        data['theta'] = request.args.get('strTheta', '[0]', type=str)
        data['beta'] = request.args.get('strBeta', '[0]', type=str)
        data['gamma'] = request.args.get('strGamma', '[0]', type=str)
        MotionCapture.create(**data)
    return jsonify(ballData=data.values())


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