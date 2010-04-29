/*
* ofxCvContourFinder.h
*
* Finds white blobs in binary images and identifies
* centroid, bounding box, area, length and polygonal contour
* The result is placed in a vector of ofxCvBlob objects.
*
*/

#ifndef __PE_VISION_CONTOURFINDER_H__
#define __PE_VISION_CONTOURFINDER_H__

#include <pe/Vision/Blob.h>
#include <pe/Math/Matrix.h>
#include <vector>
#include "cv.h"

namespace pe {
namespace vision {

  class ContourFinder {

    std::vector<Blob> m_blobs;
    pe::Matrix3x3 m_calibration_matrix;

  public:

    ContourFinder() {
      m_calibration_matrix.set_identity();
    }

    void setCalibration(Matrix3x3 const& M) {
      m_calibration_matrix = M;
    }
    
    void findContours( cv::Mat const& input_image,
                       int minArea,
                       int maxArea,
                       int nConsidered,
                       bool bFindHoles,
                       bool bUseApproximation);

    std::vector<Blob>& blobs() { return m_blobs; }

    void draw();

  protected:

  };

}} // namespace pe::vision

#endif // __PE_VISION_CONTOURFINDER_H__
