__author__ = 'donal'
__project__ = 'dcleaner'

from . import log_recs
from ..log_auth.views import admin_required, set_template

@log_recs.route('/logs')
@admin_required
def logs():
    txt = open('logs/Devel_logs.log').readlines()
    return set_template('panelbuilder.html', txt, '',
                        panel_args=dict(
                                patex='Your Logged Records',
                                tadata='log_records_tdata.html',
                                wid=12
                        ))
