/****************************************************************************
** Meta object code from reading C++ file 'GlPreviewWidget.h'
**
** Created: Sun Feb 15 15:48:38 2009
**      by: The Qt Meta Object Compiler version 59 (Qt 4.4.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "GlPreviewWidget.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'GlPreviewWidget.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 59
#error "This file was generated using the moc from 4.4.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_GlPreviewWidget[] = {

 // content:
       1,       // revision
       0,       // classname
       0,    0, // classinfo
       1,   10, // methods
       0,    0, // properties
       0,    0, // enums/sets

 // slots: signature, parameters, type, tag, flags
      17,   16,   16,   16, 0x0a,

       0        // eod
};

static const char qt_meta_stringdata_GlPreviewWidget[] = {
    "GlPreviewWidget\0\0timer_callback()\0"
};

const QMetaObject GlPreviewWidget::staticMetaObject = {
    { &QGLWidget::staticMetaObject, qt_meta_stringdata_GlPreviewWidget,
      qt_meta_data_GlPreviewWidget, 0 }
};

const QMetaObject *GlPreviewWidget::metaObject() const
{
    return &staticMetaObject;
}

void *GlPreviewWidget::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_GlPreviewWidget))
        return static_cast<void*>(const_cast< GlPreviewWidget*>(this));
    return QGLWidget::qt_metacast(_clname);
}

int GlPreviewWidget::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QGLWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: timer_callback(); break;
        }
        _id -= 1;
    }
    return _id;
}
QT_END_MOC_NAMESPACE
