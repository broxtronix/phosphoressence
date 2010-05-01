/*
* ofxCvBlob.h
* openFrameworks
*
* A blob is a homogenous patch represented by a polygonal contour.
* Typically a blob tracker uses the contour to figure out the blob's
* persistence and "upgrades" it with ids and other temporal
* information.
*
*/

#ifndef __PE_VISION_BLOB_H__
#define __PE_VISION_BLOB_H__

#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#include <AGL/agl.h>
#else // Linux
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glext.h>
#endif 

#include <pe/Math/Vector.h>
#include <pe/Math/BBox.h>
#include <pe/Core/Time.h>
#include <vector>


namespace pe {
namespace vision {

  class BlobListener {
  public:
    virtual void blobOn( float x, float y, int id, int order) = 0;
    virtual void blobMoved( float x, float y, int id, int order ) = 0;
    virtual void blobOff( float x, float y, int id, int order ) = 0;
  };

  class Blob {

  public:
    
    float area;
    float length;
    BBox2i boundingRect;
    Vector2 centroid;
    bool hole;
    std::vector<Vector2> contour;    // the contour of the blob
    
    //----------------------------------------
    Blob() {
      area = 0.0f;
      length = 0.0f;
      hole = false;
    }

    //----------------------------------------
    void draw() {

      glLineWidth(2.0);
      glColor3f(0.5+0.4*cos(3.0/20*pe_time()), 
                0.5+0.4*cos(4.0/20*pe_time()), 
                0.5+0.4*cos(7.0/20*pe_time()));
      glBegin(GL_LINE_STRIP);
      for (unsigned i = 0; i < contour.size(); i++) {
        glVertex2f( contour[i].x(), contour[i].y() );
      }
      glEnd();
    }
  };


  class TrackedBlob : public pe::vision::Blob {
    
  public:

    int id;
    Vector2 smoothedCentroid;
    Vector2 deltaLoc;
    Vector2 deltaLocTotal;
    Vector2 predictedPos;
    float deltaArea;

    // Used only by BlobTracker
    //
    bool markedForDeletion;
    int framesLeft;
    std::vector<float> error;
    std::vector<int> closest;  // ids of the closest points, sorted    

    TrackedBlob();
    TrackedBlob( Blob const& b );
    
    int getLowesterror();
  };
  
}} // namespace pe::vision

#endif // __PE_VISION_BLOB_H__

