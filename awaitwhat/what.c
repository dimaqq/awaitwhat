#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "frameobject.h"

static PyObject *
what_next(PyObject *self, PyObject *arg)
{
    if (!PyFrame_Check(arg)) {
        PyErr_SetString(PyExc_TypeError, "Argument must be a frame object.");
        return NULL;
    }

    PyFrameObject *frame = (PyFrameObject *)arg;

    // FIXME validate that current instruction is YIELD_FROM
    // Due to optimisations, it may be the preceding GET_AWAITABLE
    // int opcode = _Py_OPCODE(*next_instr);

    // printf("val %p top %p delta value to top: %ld\n",
    //        frame->f_valuestack,
    //        frame->f_stacktop,
    //        (long)(frame->f_stacktop - frame->f_valuestack));

    PyObject **stack_pointer = frame->f_stacktop;

    if (frame->f_stacktop == frame->f_valuestack) {
        PyErr_SetString(PyExc_ValueError, "stack is empty");
        return NULL;
    }

    if (!stack_pointer) {
        PyErr_SetString(PyExc_ValueError, "stack pointer is null?");
        return NULL;
    }

    // Top-most on the value stack ought to be the "receiver".
    PyObject *next = stack_pointer[-1];

    if (!next) {
        PyErr_SetString(PyExc_SystemError, "thing on stack is null?");
        return NULL;
    }

    Py_INCREF(next);
    return next;
}

static PyMethodDef what_functions[] = {
    {"next", what_next, METH_O,
     "Next frame for the given frame."}, /* FIXME: function docstring */
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef whatmodule = {
    PyModuleDef_HEAD_INIT, "what", /* name of module */
    NULL, /* FIXME: module docstring, module documentation, may be NULL */
    0,    /* size of per-interpreter state of the module */
    what_functions};

PyMODINIT_FUNC
PyInit__what(void)
{
    PyObject *m;

    m = PyModule_Create(&whatmodule);
    if (m == NULL)
        return NULL;

    PyModule_AddFunctions(m, what_functions);
    return m;
}
