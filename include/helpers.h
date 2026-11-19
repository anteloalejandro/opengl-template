#pragma once

#include "GL/freeglut.h"
#include <GL/gl.h>
#include <cstdio>

// Transform vectors into a coma-separated list of values.
#define V4_UNPACK(vector) (vector[0]), (vector[1]), (vector[2]), (vector[3])
#define V3_UNPACK(vector) (vector[0]), (vector[1]), (vector[2])
#define V3_COORDS(vector) (vector).x, (vector).y, (vector).z

// Helpers to scope blocks of OpenGL code.

// Create a scope wrapped in glBegin and glEnd.
#define GL_SCOPE(mode, ...) glBegin(mode); { __VA_ARGS__; } glEnd();
// Asign a new Display List to and existing variable.
#define GL_LISTS_ASSIGN(varname, nlists, ...) varname = glGenLists((nlists)); glNewList(varname, GL_COMPILE); { __VA_ARGS__ } glEndList();
// Create a new Display List with glGenLists(nlists)
#define GL_LISTS(varname, nlists,...) GLuint GL_LISTS_ASSIGN(varname, nlists, __VA_ARGS__)
// Create a new Display List with glGenLists(1)
#define GL_LIST(varname, ...) GL_LISTS(varname, 1, __VA_ARGS__)
// Enapsulate attributes
#define GL_ATTRIB(...) glPushAttrib(GL_ALL_ATTRIB_BITS); { __VA_ARGS__; } glPopAttrib();
// Encapsulate matrix transformations
#define GL_MATRIX(...) glPushMatrix(); { __VA_ARGS__; } glPopMatrix();
// Encapsulate attributes and matrix transformations
#define GL_GUARD(...) GL_ATTRIB(GL_MATRIX(__VA_ARGS__));

int time_delta() {
    static int last_time = glutGet(GLUT_ELAPSED_TIME);
    int now = glutGet(GLUT_ELAPSED_TIME);

    int diff = now - last_time;
    last_time = now;

    return diff;
}

GLenum glCheckError_(const char *file, int line)
{
    GLenum errorCode;
    while ((errorCode = glGetError()) != GL_NO_ERROR)
    {
        char *error;
        switch (errorCode)
        {
            case GL_INVALID_ENUM:                  error = "INVALID_ENUM"; break;
            case GL_INVALID_VALUE:                 error = "INVALID_VALUE"; break;
            case GL_INVALID_OPERATION:             error = "INVALID_OPERATION"; break;
            case GL_STACK_OVERFLOW:                error = "STACK_OVERFLOW"; break;
            case GL_STACK_UNDERFLOW:               error = "STACK_UNDERFLOW"; break;
            case GL_OUT_OF_MEMORY:                 error = "OUT_OF_MEMORY"; break;
            case GL_INVALID_FRAMEBUFFER_OPERATION: error = "INVALID_FRAMEBUFFER_OPERATION"; break;
        }
        printf("%s | %s ( %d )", error, file, line);
    }
    return errorCode;
}
#define glCheckError() glCheckError_(__FILE__, __LINE__) 
