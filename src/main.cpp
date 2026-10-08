#include <GL/glew.h>
#include <GL/freeglut.h>
#include <GL/gl.h>
#include <GL/glui.h>
#include <FreeImage.h>
#include "codebase.h"


// Transform color vectors into a coma-separated list of values.
#define V_TO_RGBA(vector) (vector[0]), (vector[1]), (vector[2]), (vector[3])
#define V_TO_RGB(vector) (vector[0]), (vector[1]), (vector[2])

// Helpers to scope blocks of OpenGL code.

// Create a scope wrapped in glBegin and glEnd.
#define GL_SCOPE(mode, ...) glBegin(mode); { __VA_ARGS__; } glEnd();
// Asign a new Display List to and existing variable.
#define GL_LISTS_ASIGN(varname, nlists, ...) varname = glGenLists((nlists)); glNewList(varname, GL_COMPILE); { __VA_ARGS__ } glEndList();
// Create a new Display List with glGenLists(nlists)
#define GL_LISTS(varname, nlists,...) GLuint GL_LISTS_ASIGN(varname, nlists, __VA_ARGS__)
// Create a new Display List with glGenLists(1)
#define GL_LIST(varname, ...) GL_LISTS(varname, 1, __VA_ARGS__)

void init(void) {
   // Set initial settings
   glClearColor(0.0, 0.0, 0.0, 0.0);
   glColor3f(1, 1, 1);

   // Set screen coordinates
   glMatrixMode(GL_PROJECTION);   
   glLoadIdentity();
   glOrtho(-10.0, 10.0, -10.0, 10.0, -10.0, 10.0);
}

void display(void) {
   // Clear screen
   glClear(GL_COLOR_BUFFER_BIT);
   glRectf(-5.0, 5.0, 5.0, -5.0);
   // glutSwapBuffers(); // Double buffer
   glFlush();
}

void reshape(int width, int height) {

}

// Draw white square on black background
int main (int argc, char **argv) {
   // Window settings
   glutInit(&argc, argv);
   // glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB); // Double buffer
   glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
   glutInitWindowSize(250, 250);
   glutInitWindowPosition(100, 100);

   // Create window
   glutCreateWindow("My First OpenGL Application");

   // initialization
   init();

   // callbacks
   glutDisplayFunc(display);
   glutReshapeFunc(reshape);

   // begin main loop
   glutMainLoop();
}
