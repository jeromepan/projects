/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 2.0.11
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.truenorth.wrappers;

public class YacuDecu_swigJNI {
  public final static native long new_float_array(int jarg1);
  public final static native void delete_float_array(long jarg1);
  public final static native float float_array_getitem(long jarg1, int jarg2);
  public final static native void float_array_setitem(long jarg1, int jarg2, float jarg3);
  public final static native int deconv_device(long jarg1, long jarg2, long jarg3, long jarg4, float[] jarg5, float[] jarg6, float[] jarg7);
}