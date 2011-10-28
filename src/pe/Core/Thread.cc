// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__

#include <pe/Core/Thread.h>
#include <pe/config.h>

namespace pe { 
namespace thread {

  // These static variables are used to generate unique identifiers
  // for threads as identifiers are requested using the static
  // Thread::id() method.
  static int pe_thread_next_available_id = 0;
  static boost::thread_specific_ptr<int> pe_thread_id_ptr;

  // The destructor for this Mutex is never called. This is intentional, to
  // prevent static destruction. If Thread::id() is called from the destructor
  // of a static object, there is a race between static destruction of the
  // Mutex and the object whose destruction results in an id() call. The one I
  // found was ~PerThreadBufferedStreamBuf -> sync() -> id()
  static Mutex& pe_thread_id_mutex() {
    static Mutex* m = new Mutex();
    return *m;
  }

}} // namespace pe::thread


int pe::Thread::id() { 
  
  // If the thread ID has not been accessed before, we initialize
  // it with a unique ID.
  if (thread::pe_thread_id_ptr.get() == 0) {
    Mutex::Lock lock(thread::pe_thread_id_mutex());
    thread::pe_thread_id_ptr.reset(new int(thread::pe_thread_next_available_id++));
  }
  
  // Then we return the result.
  int* result = thread::pe_thread_id_ptr.get();   
  return *result;
}
