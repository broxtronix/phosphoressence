// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


/// \file Core/Cache.cc
/// 
/// Types and functions to assist cacheing regeneratable data.
///
#include <pe/Core/Cache.h>
#include <pe/Core/Debugging.h>
#include <pe/Core/Settings.h>

namespace {
  pe::RunOnce system_cache_once = PE_RUNONCE_INIT;
  pe::Cache *system_cache_ptr = 0;
  void init_system_cache() {
    system_cache_ptr = new pe::Cache( pe::pe_settings().system_cache_size() );
  }
}

pe::Cache& pe::pe_system_cache() {
  system_cache_once.run( init_system_cache );
  return *system_cache_ptr;
}

void pe::Cache::allocate( size_t size ) {
  while( m_size+size > m_max_size ) {
    if( ! m_last_valid ) {
      pe_out(WarningMessage, "console") << "Warning: Cached object (" << size << ") larger than requested maximum cache size (" << m_max_size << "). Current Size = " << m_size << "\n";
      pe_out(WarningMessage, "cache") << "Warning: Cached object (" << size << ") larger than requested maximum cache size (" << m_max_size << "). Current Size = " << m_size << "\n";
      break;
    }
    m_last_valid->invalidate();
  }
  m_size += size;
  PE_CACHE_DEBUG( pe_out(DebugMessage, "cache") << "Cache allocated " << size << " bytes (" << m_size << " / " << m_max_size << " used)" << "\n"; )
}

void pe::Cache::resize( size_t size ) {
  Mutex::Lock lock(m_mutex);
  m_max_size = size;
  while( m_size > m_max_size ) {
    PE_ASSERT( m_last_valid, LogicErr() << "Cache is empty but has nonzero size!" );
    m_last_valid->invalidate();
  }
}

void pe::Cache::deallocate( size_t size ) {
  m_size -= size;
  PE_CACHE_DEBUG( pe_out(DebugMessage, "cache") << "Cache deallocated " << size << " bytes (" << m_size << " / " << m_max_size << " used)" << "\n"; )
}

// Move the cache line to the top of the valid list.
void pe::Cache::validate( CacheLineBase *line ) {
  if( line == m_first_valid ) return;
  if( line == m_last_valid ) m_last_valid = line->m_prev;
  if( line == m_first_invalid ) m_first_invalid = line->m_next;
  if( line->m_next ) line->m_next->m_prev = line->m_prev;
  if( line->m_prev ) line->m_prev->m_next = line->m_next;
  line->m_next = m_first_valid;
  line->m_prev = 0;
  if( m_first_valid ) m_first_valid->m_prev = line;
  m_first_valid = line;
  if( ! m_last_valid ) m_last_valid = line;
}

// Move the cache line to the top of the invalid list.
void pe::Cache::invalidate( CacheLineBase *line ) {
  if( line == m_first_valid ) m_first_valid = line->m_next;
  if( line == m_last_valid ) m_last_valid = line->m_prev;
  if( line->m_next ) line->m_next->m_prev = line->m_prev;
  if( line->m_prev ) line->m_prev->m_next = line->m_next;
  line->m_next = m_first_invalid;
  line->m_prev = 0;
  if( m_first_invalid ) m_first_invalid->m_prev = line;
  m_first_invalid = line;
}

// Remove the cache line from the cache lists.
void pe::Cache::remove( CacheLineBase *line ) {
  if( line == m_first_valid ) m_first_valid = line->m_next;
  if( line == m_last_valid ) m_last_valid = line->m_prev;
  if( line == m_first_invalid ) m_first_invalid = line->m_next;
  if( line->m_next ) line->m_next->m_prev = line->m_prev;
  if( line->m_prev ) line->m_prev->m_next = line->m_next;
  line->m_next = line->m_prev = 0;
}

// Move the cache line to the bottom of the valid list.
void pe::Cache::deprioritize( CacheLineBase *line ) {
  if( line == m_last_valid ) return;
  if( line == m_first_valid ) m_first_valid = line->m_next;
  if( line->m_next ) line->m_next->m_prev = line->m_prev;
  if( line->m_prev ) line->m_prev->m_next = line->m_next;
  line->m_prev = m_last_valid;
  line->m_next = 0;
  m_last_valid->m_next = line;
  m_last_valid = line;
}

