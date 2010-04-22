// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

/// \file PeUtils.h
///
/// Some handy utilities for inter-thread communication, and other
/// tasks.
#ifndef __PE_UTILS__
#define __PE_UTILS__

#include <pe/Core/Thread.h>

template <class T>
class RingBuffer {
  int m_size;
  T *m_data;
  int m_write_index;
  int m_read_index;
  T *m_write_ptr;
  T *m_read_ptr;
  pe::Mutex m_mutex;

public:
  RingBuffer(int size = 96000) {
    m_size = size;
    m_data = new T[size];

    m_read_index = 0;
    m_write_index = 0;
    m_write_ptr = &(m_data[0]);
    m_read_ptr = &(m_data[0]);
  }

  ~RingBuffer() {
    delete[] m_data;
  }

  int size() const { return m_size; }

  inline void append(T val) {
    pe::Mutex::Lock lock(m_mutex);

    *m_write_ptr++ = val;                                   

    // Reset the data pointer if we have reached the end of the
    // buffer.
    m_write_index++;
    if ( m_write_index >= m_size ) {
      m_write_index = 0;
      m_write_ptr = &(m_data[0]);
    }
  }  
  
  inline T pop() { 
    pe::Mutex::Lock lock(m_mutex);

    if (m_read_index != m_write_index) {
      T result = *(m_read_ptr);

      // Go to next frame
      m_read_index++;
      m_read_ptr++;
      if ( m_read_index >= m_size ) {
        m_read_index = 0;
        m_read_ptr = &(m_data[0]);
      }
      return result;
    } 
    return T();  // Return an empty value if the buffer is empty.
  }

  bool empty() {
    pe::Mutex::Lock lock(m_mutex);
    return m_read_index == m_write_index;
  }

};


#endif // __PE_UTILS__
