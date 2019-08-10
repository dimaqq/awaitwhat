#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *
what_next(PyObject *self, PyObject *args)
{
    PyObject *frame = NULL;
    PyObject *next = NULL;

    if (!PyArg_ParseTuple(args, "O", &frame))
        return NULL;

    if (next) 
    {
        PyErr_SetString(PyExc_ValueError, "Argument must be a Python frame");
        return NULL;
    }
    return PyLong_FromLong(1);
}

static PyMethodDef what_functions[] = {
    {"next",  what_next, METH_VARARGS, "Next frame for the given frame."},
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
