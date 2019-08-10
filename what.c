#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "frameobject.h"

static PyObject *
what_next(PyObject *self, PyObject *arg)
{
    PyFrameObject *frame = NULL;
	PyObject **stack_pointer;
    PyObject *next = NULL;

    if (!PyFrame_Check(arg))
	{
		PyErr_SetString(PyExc_TypeError, "Argument must be a frame object.");
		return NULL;
	}

    frame = (PyFrameObject*) arg;
	stack_pointer = frame->f_stacktop;
    if (!stack_pointer) {
        PyErr_SetString(PyExc_SystemError, "stack pointer is null?");
        return NULL;
    }
    next = *stack_pointer;
    if (!next) {
        PyErr_SetString(PyExc_SystemError, "thing on stack is null?");
        return NULL;
    }
    Py_INCREF(next);
    return next;
}

static PyMethodDef what_functions[] = {
    {"next",  what_next, METH_O, "Next frame for the given frame."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef whatmodule = {
    PyModuleDef_HEAD_INIT,
    "what", /* name of module */
    NULL,   /* module documentation, may be NULL */
    -1,     /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    what_functions
};

PyMODINIT_FUNC
PyInit_what(void)
{
    PyObject *m;

    m = PyModule_Create(&whatmodule);
    if (m == NULL)
        return NULL;

    PyModule_AddFunctions(m, what_functions);
    return m;
}
