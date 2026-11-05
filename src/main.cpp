#include <GL/glew.h>
#include <GL/freeglut.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glui.h>
#include <FreeImage.h>
#include "GL/freeglut_std.h"
#include "codebase.h"
#include "helpers.h"


// Transform vectors into a coma-separated list of values.
#define V4_UNPACK(vector) (vector[0]), (vector[1]), (vector[2]), (vector[3])
#define V3_UNPACK(vector) (vector[0]), (vector[1]), (vector[2])
#define V3_COORDS(vector) (vector).x, (vector).y, (vector).z, 

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

#define FPS_TARGET 60

using std::vector;
using cb::Vec3;

float rotation = 0;

void init(void) {
   // Set initial settings
   glClearColor(0.0, 0.0, 0.0, 0.0);
   glColor3f(1, 1, 1);

   glEnable(GL_DEPTH_TEST);
}

void display(void) {
   // Clear screen
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

   glMatrixMode(GL_MODELVIEW);
   glLoadIdentity();

   static Vec3 pov(1,2,3);

   gluLookAt(
      // where the camera is positioned
      V3_COORDS(pov)
      // where the camera points to
      0, 0, 0,
      // which way "up" is
      0, 1, 0
   );

   GL_GUARD({
      glRotatef(rotation, 0, 1, 0);
      glutWireTeapot(0.5);
   })

   cb::ejes();

   glCheckError(); // print errors to stdout

   glutSwapBuffers(); // Double buffer
}

void reshape(int width, int height) {
   float ar = width / (float) height; // aspect ratio
   glViewport(0, 0, width, height);
   glMatrixMode(GL_PROJECTION);   
   glLoadIdentity();
   gluPerspective(
      45,  // FOV
      ar,  // aspect ratio
      1,   // near
      100  // far
   );
}

void update() {
   int delta = time_delta();
   float mins = delta / 1000. / 60.;

   int rpm = 60;

   rotation += rpm * 360 * mins;
   while (rotation > 360.) {
      rotation -= 360.; 
   }

   // trigger a display event, with triggers all other events
   glutPostRedisplay();
}

void on_timer(int t) {
   glutTimerFunc(t, on_timer, t);
   update();
}

// Draw white square on black background
int main (int argc, char **argv) {
   // Window settings
   glutInit(&argc, argv);
   glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
   glutInitWindowSize(250, 250);
   glutInitWindowPosition(100, 100);

   // Create window
   glutCreateWindow("My First OpenGL Application");

   // initialization
   init();

   // callbacks
   glutDisplayFunc(display);
   glutReshapeFunc(reshape);
   glutTimerFunc(1000/FPS_TARGET, on_timer, 1000/FPS_TARGET);

   // begin main loop
   glutMainLoop();
}
