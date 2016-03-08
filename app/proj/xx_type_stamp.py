"""
Users assert their Types on the client interface.
This allows them to save and later recover those choices for use.
"""
from datetime import datetime
from config_project import VERSION

__author__ = 'donal'
__project__ = 'dataHoover'
#todo fileName hardwires

class TypeStamper(object):
    """
    Stamps type assertions onto .txt file for later recovery.
    """
    def __init__(self):
        pass

    def save_choices(self, data, fileName='Stamp_Vers'):
        fileName = '{}_{}_{}.txt'.format(
                fileName,
                VERSION,
                datetime.now().strftime('%Y%m%d_%H%M%S')
        )
        s3_upload_by_str(fileName, str(data))
        """
        fileName = os.path.join(DL_DIR, fileName)
        # save data to local
        with open(fileName, 'w') as fileObj:
            fileObj.write(str(data))
        # save local to remote
        s3_upload_by_filename(fileName)
        """

    def load_choices(self, fileName):
        fileName = 'app/static/data/{}'.format(fileName)
        with open(fileName) as fileObj:
            tmp = fileObj.read()
        return tmp

    def load_choices2(self, fileName):
        pass