#include <pe/Vision/Blob.h>

pe::vision::TrackedBlob::TrackedBlob() {
  id = -1;
  area = 0.0f;
  length = 0.0f;
  deltaArea = 0.0f;
  markedForDeletion = false;
  framesLeft = 0;
}

pe::vision::TrackedBlob::TrackedBlob( pe::vision::Blob const& b ) {
  area = b.area;
  length = b.length;
  boundingRect = b.boundingRect;
  centroid = b.centroid;
  smoothedCentroid = b.centroid;
  hole = b.hole;
  contour = b.contour;
  
  id = -1;
  deltaArea = 0.0f;
  markedForDeletion = false;
  framesLeft = 0;
}
    
int pe::vision::TrackedBlob::getLowesterror() {
  int best=-1;
  float best_v=99999.0f;
  for( unsigned int i=0; i<error.size(); i++ ) {
    if( error[i] < best_v ) {
      best = i;
      best_v = error[i];
    }
  }
  return best;
}

