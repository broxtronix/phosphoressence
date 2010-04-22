// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


/// \file Core/Exception.cc
/// 
/// Error / exception handling facilities.
///
/// See Core/Exception.h for documentation.
///
#include <pe/core/Exception.h>
#include <pe/config.h>

#include <cstdlib>

namespace {

  /// The default exception handler type and object, which throws
  /// the exceptions its given unless PE_ENABLE_EXCEPTIONS is 0, in
  /// which case it prints the message and calls abort().
  static class DefaultExceptionHandler : public pe::ExceptionHandler {
  public:
    virtual void handle( pe::Exception const& e ) const {
#if defined(PE_ENABLE_EXCEPTIONS) && (PE_ENABLE_EXCEPTIONS==1)
      e.default_throw();
#else
      pe::pe_out(pe::ErrorMessage) << "Fatal error: " << e.what() << std::endl;
      std::abort();
#endif
    }
    virtual ~DefaultExceptionHandler() {}
  } _pe_default_exception_handler;

  /// The application-wide exception handler pointer.
  static pe::ExceptionHandler const* _pe_exception_handler = &_pe_default_exception_handler;

};

void pe::set_exception_handler( pe::ExceptionHandler const* eh ) {
  if( eh ) _pe_exception_handler = eh;
  else _pe_exception_handler = &_pe_default_exception_handler;
}

void pe::pe_throw( pe::Exception const& e ) {
  _pe_exception_handler->handle( e );
  // We cannot return.
  std::abort();
}
