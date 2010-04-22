// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


/// \file Math/Functors.h
///
/// Mathematical functors.
///
/// This file provides polymorphic functor versions of the standard
/// mathematical functions defined in e.g. math.h.
///
#ifndef __PE_MATH_FUNCTORS_H__
#define __PE_MATH_FUNCTORS_H__

#include <cstdlib>
#include <limits>
#include <complex>
#include <vector>
#include <algorithm>

#include <pe/config.h>
#include <pe/Core/CompoundTypes.h>
#include <pe/Core/TypeDeduction.h>
#include <pe/Core/Functors.h>
#include <pe/Core/Exception.h>
#include <pe/config.h>

// The math.h header in FreeBSD (and possibly other platforms) does not
// include routines for manipulating long doubles.  We disable long
// double PE math routines here for certain platforms.
#if defined(__FreeBSD__) || defined(_WIN32)
#define __PE_MATH_DISABLE_LONG_DOUBLE_ARITHMETIC
#endif

namespace pe {
namespace math {

  template <class T> struct StdMathType { typedef double type; };
  template <> struct StdMathType<float> { typedef float type; };
  template <> struct StdMathType<long double> { typedef long double type; };
  template <class T1, class T2> struct StdMathType2 {
    typedef typename StdMathType<typename PromoteType<T1,T2>::type>::type type;
  };

  template <class FuncT, class ArgT, bool ArgIsCompound>
  struct ArgUnaryFunctorTypeHelper : public StdMathType<ArgT> {};

  template <class FuncT, class ArgT>
  struct ArgUnaryFunctorTypeHelper<FuncT,ArgT,true> {
    typedef typename CompoundChannelType<ArgT>::type channel_type;
    typedef typename ArgUnaryFunctorTypeHelper<FuncT,channel_type,IsCompound<channel_type>::value>::type result_channel_type;
    typedef typename CompoundChannelCast<ArgT,result_channel_type>::type type;
  };

  template <class F, class T>
  struct ArgUnaryFunctorType : public ArgUnaryFunctorTypeHelper<F,T,IsCompound<T>::value> {};


  template <class FuncT, class Arg1T, class Arg2T, bool Arg1IsCompound, bool Arg2IsCompound>
  struct BinaryFunctorTypeHelper : public StdMathType2<Arg1T,Arg2T> {};

  template <class FuncT, class Arg1T, class Arg2T>
  struct BinaryFunctorTypeHelper<FuncT,Arg1T,Arg2T,true,false> {
    typedef typename CompoundChannelType<Arg1T>::type channel_type;
    typedef typename BinaryFunctorTypeHelper<FuncT,channel_type,Arg2T,IsCompound<channel_type>::value,false>::type result_channel_type;
    typedef typename CompoundChannelCast<Arg1T,result_channel_type>::type type;
  };

  template <class FuncT, class Arg1T, class Arg2T>
  struct BinaryFunctorTypeHelper<FuncT,Arg1T,Arg2T,false,true> {
    typedef typename CompoundChannelType<Arg2T>::type channel_type;
    typedef typename BinaryFunctorTypeHelper<FuncT,Arg1T,channel_type,false,IsCompound<channel_type>::value>::type result_channel_type;
    typedef typename CompoundChannelCast<Arg2T,result_channel_type>::type type;
  };

  template <class FuncT, class Arg1T, class Arg2T>
  struct BinaryFunctorTypeHelper<FuncT,Arg1T,Arg2T,true,true> {
    typedef typename CompoundChannelType<Arg1T>::type channel1_type;
    typedef typename CompoundChannelType<Arg2T>::type channel2_type;
    typedef typename BinaryFunctorTypeHelper<FuncT,channel1_type,channel2_type,IsCompound<channel1_type>::value,IsCompound<channel2_type>::value>::type result_channel_type;
    typedef typename boost::mpl::if_<CompoundIsCompatible<Arg1T,Arg2T>, typename CompoundChannelCast<Arg1T,result_channel_type>::type, TypeDeductionError<BinaryFunctorTypeHelper> >::type type;
  };

  template <class FuncT, class Arg1T, class Arg2T>
  struct BinaryFunctorType : public BinaryFunctorTypeHelper<FuncT,Arg1T,Arg2T,IsCompound<Arg1T>::value,IsCompound<Arg2T>::value> {};

  // ********************************************************************
  // Standard Mathematical Functors
  // ********************************************************************

#if !defined(__PE_MATH_DISABLE_LONG_DOUBLE_ARITHMETIC)
  // This will actually create a specialization for long doubles
  #define __PE_MATH_UNARY_LONG_DOUBLE_IMPL(func)                         \
      long double operator()( long double arg ) const {                  \
        return func##l(arg);                                             \
      }
  #define __PE_MATH_BINARY_LONG_DOUBLE_IMPL(func)                        \
    long double operator()( long double arg1, long double arg2 ) const { \
      return func##l(arg1,arg2);                                         \
    }
#else
  // This is basically a no-op
  #define __PE_MATH_UNARY_LONG_DOUBLE_IMPL(func)
  #define __PE_MATH_BINARY_LONG_DOUBLE_IMPL(func)
#endif

#define __PE_UNARY_MATH_FUNCTOR(name,func)                              \
  struct Arg##name##Functor                                             \
    : UnaryReturnBinaryTemplateBind1st<ArgUnaryFunctorType,Arg##name##Functor> { \
    template <class ValT>                                               \
    typename ArgUnaryFunctorType<Arg##name##Functor,ValT>::type         \
    operator()( ValT arg ) const {                                      \
      return func(arg);                                                 \
    }                                                                   \
    float operator()( float arg ) const {                               \
      return func##f(arg);                                              \
    }                                                                   \
    __PE_MATH_UNARY_LONG_DOUBLE_IMPL(func)                              \
  };                                                                    \
  using ::func;

#define __PE_BINARY_MATH_FUNCTOR(name,func)                             \
  struct ArgArg##name##Functor                                          \
    : BinaryReturnTernaryTemplateBind1st<BinaryFunctorType,ArgArg##name##Functor> { \
    float operator()( float arg1, float arg2 ) const {                  \
      return func##f(arg1,arg2);                                        \
   }                                                                    \
    __PE_MATH_BINARY_LONG_DOUBLE_IMPL(func)                             \
    template <class Arg1T, class Arg2T>                                 \
    typename BinaryFunctorType<ArgArg##name##Functor,Arg1T,Arg2T>::type \
    inline operator()( Arg1T const& arg1, Arg2T const& arg2 ) const {   \
      return func( arg1, arg2 );                                        \
    }                                                                   \
  };                                                                    \
  template <class ValT>                                                 \
  struct ArgVal##name##Functor                                          \
    : UnaryReturnTernaryTemplateBind1st3rd<BinaryFunctorType,ArgArg##name##Functor,ValT> { \
    ValT m_val;                                                         \
    ArgVal##name##Functor(ValT val) : m_val(val) {}                     \
    template <class ArgT>                                               \
    typename BinaryFunctorType<ArgArg##name##Functor,ArgT,ValT>::type   \
    inline operator()( ArgT const& arg ) const {                        \
      return ArgArg##name##Functor()( arg, m_val );                     \
    }                                                                   \
  };                                                                    \
  template <class ValT>                                                 \
  struct ValArg##name##Functor                                          \
    : UnaryReturnTernaryTemplateBind1st2nd<BinaryFunctorType,ArgArg##name##Functor,ValT> { \
    ValT m_val;                                                         \
    ValArg##name##Functor(ValT val) : m_val(val) {}                     \
    template <class ArgT>                                               \
    typename BinaryFunctorType<ArgArg##name##Functor,ValT,ArgT>::type   \
    inline operator()( ArgT const& arg ) const {                        \
      return ArgArg##name##Functor()( m_val, arg );                     \
    }                                                                   \
  };                                                                    \
  using ::func;

  __PE_UNARY_MATH_FUNCTOR( Fabs, fabs )
  __PE_UNARY_MATH_FUNCTOR( Acos, acos )
  __PE_UNARY_MATH_FUNCTOR( Asin, asin )
  __PE_UNARY_MATH_FUNCTOR( Atan, atan )
  __PE_UNARY_MATH_FUNCTOR( Cos, cos )
  __PE_UNARY_MATH_FUNCTOR( Sin, sin )
  __PE_UNARY_MATH_FUNCTOR( Tan, tan )
  __PE_UNARY_MATH_FUNCTOR( Cosh, cosh )
  __PE_UNARY_MATH_FUNCTOR( Sinh, sinh )
  __PE_UNARY_MATH_FUNCTOR( Tanh, tanh )
  __PE_UNARY_MATH_FUNCTOR( Exp, exp )
  __PE_UNARY_MATH_FUNCTOR( Log, log )
  __PE_UNARY_MATH_FUNCTOR( Log10, log10 )
  __PE_UNARY_MATH_FUNCTOR( Sqrt, sqrt )
  __PE_UNARY_MATH_FUNCTOR( Ceil, ceil )
  __PE_UNARY_MATH_FUNCTOR( Floor, floor )

  __PE_BINARY_MATH_FUNCTOR( Atan2, atan2 )
  __PE_BINARY_MATH_FUNCTOR( Pow, pow )
  __PE_BINARY_MATH_FUNCTOR( Hypot, hypot )

#ifndef WIN32
  __PE_UNARY_MATH_FUNCTOR( Acosh, acosh )
  __PE_UNARY_MATH_FUNCTOR( Asinh, asinh )
  __PE_UNARY_MATH_FUNCTOR( Atanh, atanh )

#ifdef PE_HAVE_EXP2
  __PE_UNARY_MATH_FUNCTOR( Exp2, exp2 )
#endif
#ifdef PE_HAVE_LOG2
  __PE_UNARY_MATH_FUNCTOR( Log2, log2 )
#endif
#ifdef PE_HAVE_TGAMMA
  __PE_UNARY_MATH_FUNCTOR( Tgamma, tgamma )
#endif
  __PE_UNARY_MATH_FUNCTOR( Lgamma, lgamma )
  __PE_UNARY_MATH_FUNCTOR( Expm1, expm1 )
  __PE_UNARY_MATH_FUNCTOR( Log1p, log1p )
  __PE_UNARY_MATH_FUNCTOR( Cbrt, cbrt )
  __PE_UNARY_MATH_FUNCTOR( Erf, erf )
  __PE_UNARY_MATH_FUNCTOR( Erfc, erfc )
  __PE_UNARY_MATH_FUNCTOR( Round, round )
  __PE_UNARY_MATH_FUNCTOR( Trunc, trunc )

  __PE_BINARY_MATH_FUNCTOR( Copysign, copysign )
  __PE_BINARY_MATH_FUNCTOR( Fdim, fdim )
#endif

#undef __PE_UNARY_MATH_FUNCTOR
#undef __PE_BINARY_MATH_FUNCTOR


  // Real part functor
  struct ArgRealFunctor : UnaryReturnTemplateType<MakeReal> {
    template <class ValT>
    ValT operator()( ValT const& val ) const {
      return val;
    }

    template <class ValT>
    ValT operator()( std::complex<ValT> const& val ) const {
      return std::real(val);
    }
  };


  // Imaginary part functor
  struct ArgImagFunctor : UnaryReturnTemplateType<MakeReal> {
    template <class ValT>
      ValT operator()( ValT const& /*val*/ ) const {
      return ValT();
    }

    template <class ValT>
    ValT operator()( std::complex<ValT> const& val ) const {
      return std::imag(val);
    }
  };


  // Absolute value functor
  // This one's tricky because we have a bunch of distinct cases
  // for integer types, floating-point types, and complex types.
  /// \cond INTERNAL
  // This is outside ArgAbsFunctor because explicit template
  // specialization doesn't work at class scope.
  template <bool IntegralN> struct DefaultAbsBehavior { template <class ValT> static inline int apply( ValT val ) { return std::abs(val); } };
  template <> struct DefaultAbsBehavior<false> { template <class ValT> static inline double apply( ValT val ) { return fabs(val); } };
  /// \endcond
  struct ArgAbsFunctor {
    template <class Args> struct result;

    template <class FuncT, class ValT>
    struct result<FuncT(ValT)> {
      typedef typename boost::mpl::if_c<std::numeric_limits<ValT>::is_integer, int, double>::type type;
    };

    template <class FuncT> struct result<FuncT(float)> { typedef float type; };
    template <class FuncT> struct result<FuncT(long double)> { typedef long double type; };
    template <class FuncT> struct result<FuncT(long)> { typedef long type; };
    template <class FuncT> struct result<FuncT(long long)> { typedef long long type; };
    template <class FuncT, class ValT> struct result<FuncT(std::complex<ValT>)> { typedef ValT type; };

    template <class ValT>
    typename result<ArgAbsFunctor(ValT)>::type
    inline operator()( ValT val ) const {
      return DefaultAbsBehavior<std::numeric_limits<ValT>::is_integer>::apply(val);
    }

    inline float operator()( float val ) const { return ::fabsf(val); }
    inline long operator()( long val ) const { return std::labs(val); }
#ifdef PE_HAVE_FABSL
    inline long double operator()( long double val ) const { return ::fabsl(val); }
#endif
#ifdef PE_HAVE_LLABS
    inline long long operator()( long long val ) const { return ::llabs(val); }
#endif

    template <class ValT>
    inline ValT operator()( std::complex<ValT> const& val ) const {
      return std::abs(val);
    }
  };


  // Complex conjugation functor
  struct ArgConjFunctor : UnaryReturnSameType {
    template <class ValT>
    ValT operator()( ValT const& val ) const {
      return val;
    }

    template <class ValT>
    std::complex<ValT> operator()( std::complex<ValT> const& val ) const {
      return std::conj(val);
    }
  };


  // General-purpose accumulation functor
  template <class AccumT, class FuncT = ArgArgInPlaceSumFunctor>
  struct Accumulator : ReturnFixedType<AccumT const&> {
  private:
    AccumT m_accum;
    FuncT m_func;
  public:
    typedef AccumT value_type;

    Accumulator() : m_accum(), m_func() {}
    Accumulator( FuncT const& func ) : m_accum(), m_func(func) {}
    Accumulator( AccumT const& accum ) : m_accum(accum), m_func() {}
    Accumulator( AccumT const& accum, FuncT const& func ) : m_accum(accum), m_func(func) {}

    template <class ArgT>
    inline AccumT const& operator()( ArgT const& arg ) {
      m_func(m_accum, arg);
      return m_accum;
    }

    inline AccumT const& value() const {
      return m_accum;
    }

    void reset( AccumT const& accum = AccumT() ) {
      m_accum = accum;
    }
  };


  // Computes minimum and maximum values
  template <class ValT>
  class MinMaxAccumulator : public ReturnFixedType<void> {
    ValT m_minval, m_maxval;
    bool m_valid;
  public:
    typedef std::pair<ValT,ValT> value_type;

    MinMaxAccumulator() : m_minval(0), m_maxval(0), m_valid(false) {}

    void operator()( ValT const& arg ) {
      if ( ! m_valid ) {
        m_minval = m_maxval = arg;
        m_valid = true;
      }
      else {
        if( arg < m_minval ) m_minval = arg;
        if( m_maxval < arg ) m_maxval = arg;
      }
    }

    ValT minimum() const {
      PE_ASSERT(m_valid, ArgumentErr() << "MinMaxAccumulator: no valid samples");
      return m_minval;
    }

    ValT maximum() const {
      PE_ASSERT(m_valid, ArgumentErr() << "MinMaxAccumulator: no valid samples");
      return m_maxval;
    }

    std::pair<ValT,ValT> value() const {
      PE_ASSERT(m_valid, ArgumentErr() << "MinMaxAccumulator: no valid samples");
      return std::make_pair(m_minval,m_maxval);
    }
  };


  // Computes the median of the values to which it is applied.
  template <class ValT>
  class MedianAccumulator : public ReturnFixedType<void> {
    std::vector<ValT> m_values;
  public:
    typedef ValT value_type;

    void operator()( ValT const& value ) {
      m_values.push_back( value );
    }

    ValT const& value() {
      PE_ASSERT(m_values.size(), ArgumentErr() << "MedianAccumulator: no valid samples");
      sort(m_values.begin(), m_values.end());
      return m_values[m_values.size()/2];
    }
  };


  // Computes the mean of the values to which it is applied.
  template <class ValT>
  class MeanAccumulator : public ReturnFixedType<void> {
    typedef typename CompoundChannelCast<ValT,double>::type accum_type;
    accum_type m_accum;
    double m_count;
  public:
    typedef accum_type value_type;

    MeanAccumulator() : m_accum(), m_count() {}

    void operator()( ValT const& value ) {
      m_accum += value;
      m_count += 1.0;
    }

    value_type value() const {
      PE_ASSERT(m_count, ArgumentErr() << "MeanAccumulator: no valid samples");
      return m_accum / m_count;
    }
  };


  // Computes the standard deviation of the values to which it is applied.
  template <class ValT>
  class StdDevAccumulator : public ReturnFixedType<void> {
    typedef typename CompoundChannelCast<ValT,double>::type accum_type;
    accum_type mom1_accum, mom2_accum;
    double num_samples;
  public:
    typedef accum_type value_type;

    StdDevAccumulator() : mom1_accum(), mom2_accum(), num_samples() {}

    void operator()( ValT const& arg ) {
      mom1_accum += arg;
      mom2_accum += (accum_type) arg * arg;
      num_samples += 1.0;
    }

    value_type value() const {
      PE_ASSERT(num_samples, ArgumentErr() << "StdDevAccumulator(): no valid samples.");
      return sqrt(mom2_accum/num_samples - (mom1_accum/num_samples)*(mom1_accum/num_samples));
    }
  };


  // CDF (Cumulative Distribution Function) Accumulator
  // Actually it's an approximation. It allows for a more memory efficient
  // calculation of any quantile. Probably most importantly the median.
  //
  // Taken from Numerical Recipes (3rd E) pg 435
  template <class ValT>
  class CDFAccumulator : public ReturnFixedType<void> {
    const int m_buffersize;
    int m_num_quantiles, m_buffer_idx;
    long m_num_samples; // nq, nd, nt
    std::vector<double> m_cdf, m_sample_buf, m_quantile;
    double m_q0, m_qm;  // quantile min and max;

    // Merge in Bundles
    void update (void ) {
      int jd=0, jq=1;
      double target, told=0, tnew=0, qold, qnew;
      std::vector<double> m_new_quantile(m_num_quantiles);
      std::sort( m_sample_buf.begin(),
                 m_sample_buf.begin()+m_buffer_idx ); // For partial updates
      // Setting to global min and max;
      qold = qnew = m_quantile[0] = m_new_quantile[0] = m_q0;
      m_quantile.back() = m_new_quantile.back() = m_qm;
      // .. then setting comparable probabilities
      m_cdf[0] = std::min(0.5/(m_buffer_idx+m_num_samples),
                          0.5*m_cdf[1]);
      m_cdf.back() = std::max(1-0.5/(m_buffer_idx+m_num_samples),
                              0.5*(1+m_cdf[m_num_quantiles-2]));
      // Looping over target probability values for interpolation
      for ( int iq = 1; iq < m_num_quantiles-1; iq++ ) {
        target = (m_num_samples+m_buffer_idx)*m_cdf[iq];
        if ( tnew < target )
          while (1) {
            // Locating a succession of abscissa-ordinate pairs
            // (qnew,tnew) that are the discontinuities of value or
            // slope, breaking to perform an interpolation as we cross
            // each target.
            if ( jq < m_num_quantiles &&
                 ( jd >= m_buffer_idx ||
                   m_quantile[jq] < m_sample_buf[jd] ) ) {
              // Found slope discontinuity from old CDF.
              qnew = m_quantile[jq];
              tnew = jd + m_num_samples*m_cdf[jq++];
              if ( tnew >= target ) break;
            } else {
              // Found value discontinuity from batch data CDF.
              qnew = m_sample_buf[jd];
              tnew = told;
              if ( m_quantile[jq] > m_quantile[jq-1] )
                tnew += m_num_samples*(m_cdf[jq]-m_cdf[jq-1])*
                  (qnew-qold)/(m_quantile[jq]-m_quantile[jq-1]);
              jd++;
              if ( tnew >= target ) break;
              told = tnew++;
              qold = qnew;
              if ( tnew >= target ) break;
            }
            told = tnew;
            qold = qnew;
          }
        // Performing new interpolation
        if ( tnew == told )
          m_new_quantile[iq] = 0.5*(qold+qnew);
        else
          m_new_quantile[iq] = qold + (qnew-qold)*(target-told)/(tnew-told);
        told = tnew;
        qold = qnew;
      }
      // Reset'n
      m_quantile = m_new_quantile;
      m_num_samples += m_buffer_idx;
      m_buffer_idx = 0;
    }

  public:
    CDFAccumulator( int const& buffersize = 1000,
                    int const& quantiles = 251) :
    m_buffersize(buffersize), m_num_quantiles(quantiles), m_buffer_idx(0), m_num_samples(0), m_cdf(quantiles), m_sample_buf(buffersize), m_quantile(quantiles), m_q0(1e99), m_qm(-1e99) {

      // Setting a general purpose cdf
      // TODO: HANDLE DIFFERENT SIZED QUANTILES
      for ( int j = 85; j <= 165; j++)
        m_cdf[j] = float((j-75))/100.0;
      for ( int j = 84; j >= 0; j-- ) {
        m_cdf[j] = 0.87191909*m_cdf[j+1];
        m_cdf[m_num_quantiles-j-1] = 1.0 - m_cdf[j];
      }
    }

    // User update function. (Bundles Data)
    void operator()( ValT const& arg ) {
      // Assimilate, We are the Borg, your data is my data!
      m_sample_buf[m_buffer_idx++] = arg;
      if ( arg < m_q0 ) { m_q0 = arg; } // stretch cdf?
      if ( arg > m_qm ) { m_qm = arg; }
      if ( m_buffer_idx == m_buffersize ) update(); // merge cdf?
    }

    // Extract a percentile
    ValT quantile( double const& arg ) const {
      double q;

      // if ( m_buffer_idx > 0 ) update();
      int jl=0,jh=m_num_quantiles-1,j;
      while ( jh - jl > 1 ) {
        j = (jh+jl)>>1;
        if ( arg > m_cdf[j] ) jl=j;
        else jh=j;
      }
      j = jl;
      q = m_quantile[j]+(m_quantile[j+1]-m_quantile[j])*(arg-m_cdf[j])/(m_cdf[j+1]-m_cdf[j]);

      // Keeping estimate in CDF
      return std::max(m_quantile[0],std::min(m_quantile.back(),q));
    }

    // Predefine functions
    ValT median( void ) const { return quantile(0.5); }
    ValT first_quartile( void ) const { return quantile(0.25); }
    ValT third_quartile( void ) const { return quantile(0.75); }
    ValT approximate_mean( void ) const {
      ValT mean = 0;
      for ( float i = 0.1; i <= 1.01; i+=0.1 ) {
        mean += ( quantile(i) + quantile(i-0.1) ) / 2.0;
      }
      return mean / 10.0;
    }
  };

} // namespace math

  // I'm not even really sure why the math namespace exists anymore.... -MDH
  using math::Accumulator;
  using math::MinMaxAccumulator;
  using math::MedianAccumulator;
  using math::MeanAccumulator;
  using math::StdDevAccumulator;

} // namespace pe

#endif  // __PE_MATH_FUNCTORS_H__
