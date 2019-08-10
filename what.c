#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "frameobject.h"

static PyObject *
what_next(PyObject *self, PyObject *arg)
{
    if (!PyFrame_Check(arg))
	{
		PyErr_SetString(PyExc_TypeError, "Argument must be a frame object.");
		return NULL;
	}

    PyFrameObject *frame = (PyFrameObject*) arg;

    // FIXME validate that current instruction is YIELD_FROM
    // Due to optimisations, it may be the preceding GET_AWAITABLE
    //int opcode = _Py_OPCODE(*next_instr);

	PyObject **stack_pointer = frame->f_stacktop;

    if (!stack_pointer) {
        PyErr_SetString(PyExc_SystemError, "stack pointer is null?");
        return NULL;
    }

    // FIXME where's the "receiver" on the stack?
    // or, rather, where's the top value on the stack?
    PyObject *next = stack_pointer[-1];
    //PyObject *next = *stack_pointer;

    if (!next) {
        PyErr_SetString(PyExc_SystemError, "thing on stack is null?");
        return NULL;
    }

    Py_INCREF(next);
    return next;
}

static PyMethodDef what_functions[] = {
    {"next",  what_next, METH_O, "Next frame for the given frame."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef whatmodule = {
    PyModuleDef_HEAD_INIT,
    "what", /* name of module */
    NULL,   /* module documentation, may be NULL */
    0,      /* size of per-interpreter state of the module */
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
