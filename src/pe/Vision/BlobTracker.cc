#include <pe/Vision/BlobTracker.h>
#include <pe/Graphics/BitmapFont.h>

pe::vision::BlobTracker::BlobTracker() {
  listener = NULL;
  currentID = 1;
  extraIDs = 0;
  reject_distance_threshold = 150;
  minimumDisplacementThreshold = 0.02f;
  ghost_frames = 2;
}


void pe::vision::BlobTracker::setListener( BlobListener* _listener ) {
  listener = _listener;
}


int pe::vision::BlobTracker::findOrder( int id ) {
  // This is a bit inefficient but ok when
  // assuming low numbers of blobs
  // a better way would be to use a hash table
  int count = 0;
  for( unsigned i=0; i<blobs.size(); i++ ) {
    if( blobs[i].id < id ) {
      count++;
    }
  }
  return count;
}


pe::vision::TrackedBlob&  pe::vision::BlobTracker::getById( int id ) {

  if (blobs.size() == 0) 
    pe_throw(LogicErr() << "TrackedBlob::getById failed.  blobs.size() == 0\n");

  // This is a bit inefficient but ok when assuming low numbers of
  // blobs a better way would be to use a hash table
  TrackedBlob &bestfit = blobs[0];
  for( unsigned i=0; i<blobs.size(); i++ ) {
    if( blobs[i].id == id ) {
      bestfit = blobs[i];
    }
  }

  pe_throw(LogicErr() << "TrackedBlob::getById failed.  There is no blob with id " << id << "\n");
  return bestfit;
}



void pe::vision::BlobTracker::draw() {
  glEnable(GL_BLEND);
  glColor4f(1.0, 1.0, 1.0, 1.0);
  for( int i=0; i<blobs.size(); i++ ) {
    std::ostringstream docstring;
    docstring << blobs[i].id << "\n"; 
    pe::graphics::drawBitmapString( docstring.str(),
                                    blobs[i].smoothedCentroid.x(), 
                                    blobs[i].smoothedCentroid.y() );
  }
}


/**
* Assign ids to blobs and fire blob events.
* This method tracks by proximity and best fit.
*/
void pe::vision::BlobTracker::trackBlobs( const std::vector<pe::vision::Blob>& _blobs ) {
  int i, j, k;

  // Push to history, clear
  history.push_back( blobs );
  if( history.size() > 4 ) {
    history.erase( history.begin() );
  }
  blobs.clear();
  
  // Load new blobs
  for( i=0; i<_blobs.size(); i++ ) {
    blobs.push_back( TrackedBlob(_blobs[i]) );
  }
  
  std::vector<TrackedBlob> *prev = &history[history.size()-1];
  
  int cursize = blobs.size();
  int prevsize = (*prev).size();
  
  // now figure out the 'error' (distance) to all blobs in the previous
  // frame. We are optimizing for the least change in distance.
  // While this works really well we could also optimize for lowest
  // deviation from predicted position, change in size etc...
  
  for( i=0; i<cursize; i++ ) {
    blobs[i].error.clear();
    blobs[i].closest.clear();

    for( j=0; j<prevsize; j++ ) {
      //calc error - distance to blob in prev frame
      float deviationX = blobs[i].centroid.x() - (*prev)[j].centroid.x();
      float deviationY = blobs[i].centroid.y() - (*prev)[j].centroid.y();
      float error = (float)sqrt( deviationX*deviationX
                                 + deviationY*deviationY );

      blobs[i].error.push_back( error );
      blobs[i].closest.push_back( j );
    }
  }

  // sort so we can make a list of the closest blobs in the previous frame..
  for( i=0; i<cursize; i++ ) {
    // Bubble sort closest.
    for( j=0; j<prevsize; j++ )	{
      for( k=0; k<prevsize-1-j; k++ )	{
        // ugly as hell, I know.
        if( blobs[i].error[blobs[i].closest[k+1]]
            < blobs[i].error[blobs[i].closest[k]] ) {

          int tmp = blobs[i].closest[k];  // swap
          blobs[i].closest[k] = blobs[i].closest[k+1];
          blobs[i].closest[k+1] = tmp;
        }
      }
    }
  }


  // Generate a matrix of all the possible choices.
  // Then we will calculate the errors for every possible match
  // and pick the matrix that has the lowest error.
  // This is an NP complete approach and exponentially increases in complexity
  // with the number of blobs. To remedy for each blob we will only
  // consider the 4 closest blobs of the previous frame.

  ids.clear();

  
  // collect id's..
  for( i=0; i<cursize; i++ ) {
    ids.push_back( -1 );
  }
  
  extraIDs = cursize - prevsize;
  if( extraIDs < 0 ) {
    extraIDs = 0;
  }
  matrix.clear();
        

  // FIXME: we could scale numcheck depending on how many blobs there are
  // if we are tracking a lot of blobs, we could check less..
  if( cursize <= 4 ) {
    numcheck = 4;
  } else if( cursize <= 6 ) {
    numcheck = 3;
  } else if( cursize <= 10 ) {
    numcheck = 2;
  } else {
    numcheck = 1;
  }
  
  if( prevsize < numcheck ) {
    numcheck = prevsize;
  }
  
  if( blobs.size() > 0 ) {
    permute(0);
  }
  
  unsigned int num_results = matrix.size();
  
  
  // loop through all the potential
  // ID configurations and find one with lowest error
  
  float best_error = 99999, error;
  int best_error_ndx = -1;
  
  for( j=0; j<num_results; j++ ) {
    error = 0;

    // get the error for each blob and sum
    for( i=0; i<cursize; i++ ) {
      if( matrix[j][i] != -1 ) {
        error += blobs[i].error[matrix[j][i]];
      }
    }

    if( error < best_error )	{
      best_error = error;
      best_error_ndx = j;
    }
  }
  
  // now that we know the optimal configuration,
  // set the IDs and calculate some things..
  
  if( best_error_ndx != -1 ) {
    for( i=0; i<cursize; i++ ) {
      if( matrix[best_error_ndx][i] != -1 ) {
        blobs[i].id = (*prev)[matrix[best_error_ndx][i]].id;
      } else {
        blobs[i].id = -1;
      }

      if( blobs[i].id != -1 ) {
        TrackedBlob *oldblob = &(*prev)[matrix[best_error_ndx][i]];

        // IIR filter produces smoothed centroid location
        blobs[i].smoothedCentroid.x() = 0.1*blobs[i].centroid.x() + 0.9 * oldblob->smoothedCentroid.x();
        blobs[i].smoothedCentroid.y() = 0.1*blobs[i].centroid.y() + 0.9 * oldblob->smoothedCentroid.y();

        // Compute delta locations based on smooth data
        blobs[i].deltaLoc.x() = (blobs[i].smoothedCentroid.x() - oldblob->smoothedCentroid.x());
        blobs[i].deltaLoc.y() = (blobs[i].smoothedCentroid.y() - oldblob->smoothedCentroid.y());


        blobs[i].deltaArea = blobs[i].area - oldblob->area;

        blobs[i].predictedPos.x() = blobs[i].smoothedCentroid.x() + blobs[i].smoothedCentroid.x();
        blobs[i].predictedPos.y() = blobs[i].smoothedCentroid.y() + blobs[i].smoothedCentroid.y();

        blobs[i].deltaLocTotal.x() = oldblob->deltaLocTotal.x() + blobs[i].deltaLoc.x();
        blobs[i].deltaLocTotal.y() = oldblob->deltaLocTotal.y() + blobs[i].deltaLoc.y();
      } else {
        blobs[i].deltaLoc = Vector2( 0.0f, 0.0f );
        blobs[i].deltaArea = 0;
        blobs[i].predictedPos = blobs[i].centroid;
        blobs[i].deltaLocTotal = Vector2( 0.0f, 0.0f );
      }
    }
  }


  // fire events
  //

  // assign ID's for any blobs that are new this frame (ones that didn't get
  // matched up with a blob from the previous frame).
  for( i=0; i<cursize; i++ ) {
    if(blobs[i].id == -1)	{
      blobs[i].id = currentID;
      currentID ++;
      if( currentID >= 65535 ) {
        currentID = 0;
      }

      //doTouchEvent(blobs[i].getTouchData());
      doBlobOn( blobs[i] );
    } else {
      float totalLength =
        (float)sqrt( blobs[i].deltaLocTotal.x()*blobs[i].deltaLocTotal.x()
                     + blobs[i].deltaLocTotal.y()*blobs[i].deltaLocTotal.y() );
      if( totalLength >= minimumDisplacementThreshold ) {
        //doUpdateEvent( blobs[i].getTouchData() );
        doBlobMoved( blobs[i] );
        blobs[i].deltaLocTotal = Vector2( 0.0f, 0.0f );
      }
    }
  }

  // if a blob disappeared this frame, send a blob off event
  // for each one in the last frame, see if it still exists in the new frame.
  for( i=0; i<prevsize; i++ ) {
    bool found = false;
    for( j=0; j<cursize; j++ ) {
      if( blobs[j].id == (*prev)[i].id ) {
        found = true;
        break;
      }
    }

    if( !found ) {
      if( ghost_frames == 0 )	{
        //doUntouchEvent((*prev)[i].getTouchData());
        doBlobOff( (*prev)[i] );

      } else if( (*prev)[i].markedForDeletion ) {
        (*prev)[i].framesLeft -= 1;
        if( (*prev)[i].framesLeft <= 0 ) {
          //doUntouchEvent( (*prev)[i].getTouchData() );
          doBlobOff( (*prev)[i] );
        } else {
          blobs.push_back( (*prev)[i] );  // keep it around
          // until framesleft = 0
        }
      } else {
        (*prev)[i].markedForDeletion = true;
        (*prev)[i].framesLeft = ghost_frames;
        blobs.push_back( (*prev)[i] );  // keep it around
        // until framesleft = 0
      }
    }
  }
}





// Delegate to Callbacks
//
//
void pe::vision::BlobTracker::doBlobOn( const pe::vision::TrackedBlob& b ) {
  if( listener != NULL ) {
    listener->blobOn( b.smoothedCentroid.x(), b.smoothedCentroid.y(), b.id, findOrder(b.id) );
  } else {
    //    std::cout << "doBlobOn() event for blob: " << b.id << std::endl;
  }
}
void pe::vision::BlobTracker::doBlobMoved( const pe::vision::TrackedBlob& b ) {
  if( listener != NULL ) {
    listener->blobMoved( b.smoothedCentroid.x(), b.smoothedCentroid.y(), b.id, findOrder(b.id) );
  } else {
    //    std::cout << "doBlobMoved() event for blob: " << b.id << std::endl;
  }
}
void pe::vision::BlobTracker::doBlobOff( const pe::vision::TrackedBlob& b ) {
  if( listener != NULL ) {
    listener->blobOff( b.smoothedCentroid.x(), b.smoothedCentroid.y(), b.id, findOrder(b.id) );
  } else {
    //    std::cout << "doBlobOff() event for blob: " << b.id << std::endl;
  }
}





// Helper Methods
//
//
inline void pe::vision::BlobTracker::permute( int start ) {
  if( start == int(ids.size()) ) {
        //for( int i=0; i<start; i++)
        //{
        //printf("%d, ", ids[i]);
        //}
        //printf("--------\n");
        matrix.push_back( ids );

    } else {
        int numchecked = 0;

        for( unsigned i=0; i<blobs[start].closest.size(); i++ ) {
            if( blobs[start].error[blobs[start].closest[i]]
                > reject_distance_threshold ) {

                break;
            }

            ids[start] = blobs[start].closest[i];
            if( checkValid(start) ) {
                permute( start+1 );
                numchecked++;
            }

            if( numchecked >= numcheck ) {
                break;
            }
        }

        if( extraIDs > 0 ) {
            ids[start] = -1;		// new ID
            if( checkValidNew(start) ) {
                permute(start+1);
            }
        }
    }
}

inline bool pe::vision::BlobTracker::checkValidNew( int start ) {
	int newidcount = 0;
	newidcount ++;
	for( int i=0; i<start; i++ ) {
        if(ids[i] == -1) {
            newidcount ++;
        }
	}

	if( newidcount > extraIDs ) {
        return false;
    }

	return true;
}

inline bool pe::vision::BlobTracker::checkValid( int start ) {
	for(int i=0; i<start; i++) {
        // check to see whether this ID exists already
        if(ids[i] == ids[start]) {
            return false;
        }
	}

    return true;
}




