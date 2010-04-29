
#include <pe/Vision/ContourFinder.h>
using namespace pe::vision;

//--------------------------------------------------------------------------------
bool sort_carea_compare( const std::vector<cv::Point2f> a, const std::vector<cv::Point2f> b) {

  // use opencv to calc size, then sort based on size
  float areaa = fabs(cv::contourArea( cv::Mat(a) ));
  float areab = fabs(cv::contourArea( cv::Mat(b) ));
  return (areaa > areab);
}



//--------------------------------------------------------------------------------
void pe::vision::ContourFinder::findContours( cv::Mat const& input_image,
                                              int minArea,
                                              int maxArea,
                                              int nConsidered,
                                              bool bFindHoles,
                                              bool bUseApproximation) {

  std::vector<std::vector<cv::Point2f> > contours;
  std::vector<std::vector<cv::Point> > raw_contours;
  
  // OpenCV clobbers the contour image, so we make a copy of it here.
  cv::Mat contour_image = input_image;
  int mode = (bFindHoles) ? CV_RETR_LIST : CV_RETR_EXTERNAL;
  int method = bUseApproximation ? CV_CHAIN_APPROX_SIMPLE : CV_CHAIN_APPROX_NONE;
  
  // Run the contour finder
  cv::findContours(contour_image, raw_contours, mode, method);

  // put the contours from the linked list, into an array for sorting
  std::vector<std::vector<cv::Point> >::iterator iter = raw_contours.begin();

  while (iter != raw_contours.end()) {
    float area = cv::contourArea(cv::Mat(*iter));
    if( (area > minArea) && (area < maxArea) ) {

      // Apply calibration matrix to contours
      std::vector<cv::Point2f> contour_2f;
      std::vector<cv::Point>::iterator contour_iter = iter->begin();
      while(contour_iter != iter->end()) {
        // Do a simple similarity transform for now.  Save affine and
        // homographies for later...
        cv::Point2f p;
        p.x = m_calibration_matrix(0,0) * contour_iter->x + 
          m_calibration_matrix(0,1) * contour_iter->y + m_calibration_matrix(0,2);
        p.y = m_calibration_matrix(1,0) * contour_iter->x + 
          m_calibration_matrix(1,1) * contour_iter->y + m_calibration_matrix(1,2);
        contour_2f.push_back(p);
        ++contour_iter;
      }

      // And add it to the final contour list
      contours.push_back(contour_2f);
    }
    ++iter;
  }
  
  
  // sort the blobs based on size
  if( contours.size() > 1 ) {
    std::sort( contours.begin(), contours.end(), sort_carea_compare );
  }

  // now, we have m_blobs.size() contours, sorted by size in the array
  // m_blobs let's get the data out and into our structures that we like
  std::vector<Blob>  blobs;
  for( int i = 0; i < std::min(nConsidered, (int)contours.size()); ++i ) {
    cv::Mat contours_mat(contours[i]);

    blobs.push_back( pe::vision::Blob() );
    float area = contourArea( contours_mat );
    cv::Rect rect = boundingRect( contours_mat );
    cv::Moments moments = cv::moments( contours_mat );
    
    blobs[i].area = fabs(area);
    //    std::cout << "Are: " << blobs[i].area << "\n";
    blobs[i].hole = area < 0 ? true : false;
    blobs[i].length = cv::arcLength( contours_mat, true );
    blobs[i].boundingRect = BBox2i(rect.x, rect.y, rect.width, rect.height);
    blobs[i].centroid = Vector2(moments.m10 / moments.m00,
                                moments.m01 / moments.m00);
    //    std::cout << "Centroid: " << blobs[i].centroid << "\n";
    
    // get the points for the blob
    blobs[i].contour.resize(contours[i].size());
    for (unsigned j = 0; j < contours[i].size(); ++j) {
      blobs[i].contour[j] = Vector2(contours[i][j].x, contours[i][j].y);
    }
  }
  m_blobs = blobs;
}

//--------------------------------------------------------------------------------
void pe::vision::ContourFinder::draw() {

  for (unsigned i = 0; i < m_blobs.size(); ++i) {
    m_blobs[i].draw();
  }

}

