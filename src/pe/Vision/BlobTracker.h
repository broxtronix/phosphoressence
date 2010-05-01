
// NOTE: Based on ofxCvBlobTracker.  Notes from original below."

/*
* ofxCvBlobTracker.h
* by stefanix
* Thanks to touchlib for the best fit algorithm!
*
* This class tracks blobs between frames.
* Most importantly it assignes persistent id to new blobs, correlates
* them between frames and removes them as blobs dissappear. It also
* compensates for ghost frames in which blobs momentarily dissappear.
*
* Based on the trackning it fires events when blobs come into existence,
* move around, and disappear. The object which receives the callbacks
* can be specified with setListener().
*
*/


#ifndef __PE_VISION_BLOBTRACKER_H__
#define __PE_VISION_BLOBTRACKER_H__

#include <pe/Vision/Blob.h>

namespace pe {
namespace vision {

  class BlobTracker {


  public:

    std::vector<TrackedBlob>  blobs;

    BlobTracker();
    void setListener( BlobListener* _listener );
    void trackBlobs( const std::vector<pe::vision::Blob>& blobs );
    int findOrder( int id );  // order by which the present
                              // blobs came into existence
    TrackedBlob& getById( int id );  // returns a reference to the
    // corresponding blob in blobs vector
    void draw();

    float minimumDisplacementThreshold;

  protected:

    int currentID;
    int extraIDs;
    int numcheck;

    BlobListener* listener;

    int reject_distance_threshold;
    int ghost_frames;

    std::vector<std::vector<int> > matrix;
    std::vector<int> ids;
    std::vector<std::vector<TrackedBlob> > history;


    void doBlobOn( const TrackedBlob& b );
    void doBlobMoved( const TrackedBlob& b );
    void doBlobOff( const TrackedBlob& b );

    inline void permute( int k );
    inline bool checkValid( int start );
    inline bool checkValidNew( int start );
  };

}} // __PE_VISION_BLOBTRACKER_H__

#endif  // __PE_VISION_BLOBTRACKER_H__
