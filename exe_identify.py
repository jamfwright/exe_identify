__author__ = 'jfwright'
#http://timgolden.me.uk/python/win32_how_do_i/get-document-summary-info.html

import os, sys
import pythoncom
from win32com.shell import shell
from win32com import storagecon
reload(sys)
sys.setdefaultencoding('utf-8')
myPath = "c:/Program Files/Internet Explorer/"

FORMATS = {
    pythoncom.FMTID_SummaryInformation: "SummaryInformation",
    pythoncom.FMTID_DocSummaryInformation: "DocSummaryInformation",
    pythoncom.FMTID_UserDefinedProperties: "UserDefinedProperties"
}
PROPERTIES = {
    pythoncom.FMTID_SummaryInformation: dict(
        (getattr(storagecon, d), d) for d in dir(storagecon) if d.startswith("PIDSI_")
    ),
    pythoncom.FMTID_DocSummaryInformation: dict(
        (getattr(storagecon, d), d) for d in dir(storagecon) if d.startswith("PIDDSI_")
    )
}

STORAGE_READ = storagecon.STGM_READ | storagecon.STGM_SHARE_EXCLUSIVE


def property_dict(property_set_storage, fmtid):
    properties = {}
    try:
        property_storage = property_set_storage.Open(fmtid, STORAGE_READ)
    except pythoncom.com_error, error:
        if error.strerror == 'STG_E_FILENOTFOUND':
            return {}
        else:
            raise

    for name, property_id, vartype in property_storage:
        if name is None:
            name = PROPERTIES.get(fmtid, {}).get(property_id, None)
        if name is None:
            name = hex(property_id)
        try:
            for value in property_storage.ReadMultiple([property_id]):
                properties[name] = value
        #
        # There are certain values we can't read; they
        # raise type errors from within the pythoncom
        # implementation, thumbnail
        #
        except TypeError:
            properties[name] = None
    return properties


def property_sets(filepath):
    pidl, flags = shell.SHILCreateFromPath(os.path.abspath(filepath), 0)
    property_set_storage = shell.SHGetDesktopFolder().BindToStorage(pidl, None, pythoncom.IID_IPropertySetStorage)
    for fmtid, clsid, flags, ctime, mtime, atime in property_set_storage:
        yield FORMATS.get(fmtid, unicode(fmtid)), property_dict(property_set_storage, fmtid)
        if fmtid == pythoncom.FMTID_DocSummaryInformation:
            fmtid = pythoncom.FMTID_UserDefinedProperties
            user_defined_properties = property_dict(property_set_storage, fmtid)
            if user_defined_properties:
                yield FORMATS.get(fmtid, unicode(fmtid)), user_defined_properties


if __name__ == '__main__':
    f = open('all_libraries.txt', 'a')
    for root, dirs, files in os.walk(myPath):
        for file in files:
            file = file.lower()  # Convert .EXE to .exe so next line works
            if ((file.count('.exe') or file.count('.dll')) and not file.count('.mui')):
                # Check only exe or dll files, ignoring dll files with added mui extension
                print(str.replace(root, "\\", "/") + str.replace(file, "\\", "/") + "\n")
                f.write(str.replace("\n" + root, "\\", "/") + str.replace(file, "\\", "/") + "\n")
                try:
                    for name, properties in property_sets(str.replace(os.path.normpath(root), "\\", "/") + "/" + file):
                        for k, v in properties.items():
                           print >> f, "  ", k, "=>", v
                           #f.write "  ", k, "=>", v

                    print("\n")
                except TypeError, e:
                  continue

    f.close()

## Print Value of Key 0x7 and 0x4
## Remove Duplicates
## Check Product and Version against vuln DB