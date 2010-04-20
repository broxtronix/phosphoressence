/*
 *  ofxQTKitVideoGrabber.cpp
 *
 *  Created by James George on 3/9/10.
 *  
 *
 */

// #include <vw/Core/Log.h>
// using namespace vw;

#include "QtKitVideoGrabber.h"
#import "Cocoa/Cocoa.h"
#import "QTKit/QTKit.h"

static inline void argb_to_rgb(unsigned char* src, unsigned char* dst, int numPix) {
  for(int i = 0; i < numPix; i++){
    memcpy(dst, src+1, 3);
    src+=4;
    dst+=3;
  }	
}

@interface QTKitVideoGrabber : QTCaptureVideoPreviewOutput {
  QTCaptureSession *session;
  QTCaptureDeviceInput *videoDeviceInput;
  NSInteger width, height;
  
  CVImageBufferRef cvFrame;
  //  ofTexture* texture;
  unsigned char* pixels;	

  BOOL isRunning;
  BOOL hasNewFrame;
  BOOL isFrameNew;
  
  BOOL verbose;
}

@property(nonatomic, readonly) NSInteger height;
@property(nonatomic, readonly) NSInteger width;
@property(nonatomic, retain) QTCaptureSession* session;
@property(nonatomic, retain) QTCaptureDeviceInput* videoDeviceInput;
@property(nonatomic, readonly) BOOL isRunning;
@property(readonly) unsigned char* pixels;
//@property(readonly) ofTexture* texture;
@property(readonly) BOOL isFrameNew;
@property(nonatomic, readwrite) BOOL verbose;

- (id) initWithWidth:(NSInteger)width 
	      height:(NSInteger)height 
	      device:(NSInteger)deviceID;

- (void) outputVideoFrame:(CVImageBufferRef)videoFrame 
	 withSampleBuffer:(QTSampleBuffer *)sampleBuffer 
	   fromConnection:(QTCaptureConnection *)connection;

- (void) update;

- (void) stop;

- (void) listDevices;


@end


@implementation QTKitVideoGrabber
@synthesize width, height;
@synthesize session;
@synthesize videoDeviceInput;
@synthesize pixels;
//@synthesize texture;
@synthesize isFrameNew;
@synthesize verbose;

- (id) initWithWidth:(NSInteger)_width height:(NSInteger)_height device:(NSInteger)deviceID {
  if(self = [super init]){
    //configure self
    width = _width;
    height = _height;		
    [self setPixelBufferAttributes: [NSDictionary dictionaryWithObjectsAndKeys: 
						    [NSNumber numberWithInt: kCVPixelFormatType_32ARGB], kCVPixelBufferPixelFormatTypeKey,
						  [NSNumber numberWithInt:width], kCVPixelBufferWidthKey, 
						  [NSNumber numberWithInt:height], kCVPixelBufferHeightKey, 
						  [NSNumber numberWithBool:YES], kCVPixelBufferOpenGLCompatibilityKey,
						  nil]];	
    
    //instance variables
    cvFrame = NULL;
    hasNewFrame = false;
    // texture = new ofTexture();
    // texture->allocate(_width, _height, GL_RGB);
    pixels = (unsigned char*)calloc(sizeof(char), _width*_height*3);
    
    //set up device
    NSArray* videoDevices = [[QTCaptureDevice inputDevicesWithMediaType:QTMediaTypeVideo] 
			      arrayByAddingObjectsFromArray:[QTCaptureDevice inputDevicesWithMediaType:QTMediaTypeMuxed]];
    
    // if(verbose) {
    //   std::string list = [[videoDevices description] stdString];
    //   vw_out(DebugMessage) << "ofxQTKitVideoGrabber -- Device List: " << list << "\n";
    // }
    
    NSError *error = nil;
    BOOL success;
    
    //start the session
    self.session = [[QTCaptureSession alloc] init];
    success = [self.session addOutput:self error:&error];
    if( !success ) {
      //      vw_out(ErrorMessage) << "ofxQTKitVideoGrabber - ERROR - Error adding output";
      return nil;
    }
    
    // Try to open the new device
    if(deviceID >= videoDevices.count){
      //      vw_out(ErrorMessage) << "ofxQTKitVideoGrabber - ERROR - Error selected a nonexistent device";
      deviceID = videoDevices.count - 1;
    }
		
    QTCaptureDevice* selectedVideoDevice = [videoDevices objectAtIndex:deviceID];
    success = [selectedVideoDevice open:&error];
    if (selectedVideoDevice == nil || !success) {
      //      vw_out(ErrorMessage) << "ofxQTKitVideoGrabber - ERROR - Selected device not opened";
      return nil;
    } else { 
      // if(verbose) 
      // 	vw_out(DebugMessage) << "ofxQTKitVideoGrabber -- Attached camera " 
      // 			     << [[selectedVideoDevice description] cString] << "\n";
			
      // Add the selected device to the session
      videoDeviceInput = [[QTCaptureDeviceInput alloc] initWithDevice:selectedVideoDevice];
      success = [session addInput:videoDeviceInput error:&error];
      //      if(!success) 
	//	vw_out(ErrorMessage) << "ofxQTKitVideoGrabber - ERROR - Error adding device to session";	

      //start the session
      [session startRunning];
    }
  }
  return self;
}

//Frame from the camera
//this tends to be fired on a different thread, so keep the work really minimal
- (void) outputVideoFrame:(CVImageBufferRef)videoFrame 
	 withSampleBuffer:(QTSampleBuffer *)sampleBuffer 
	   fromConnection:(QTCaptureConnection *)connection {

  CVImageBufferRef toRelease = cvFrame;
  CVBufferRetain(videoFrame);
  @synchronized(self){
    cvFrame = videoFrame;
    hasNewFrame = YES;
  }	
  if(toRelease != NULL){
    CVBufferRelease(toRelease);
  }
}

- (void) update {
  @synchronized(self){
    if(hasNewFrame){
      CVPixelBufferLockBaseAddress(cvFrame, 0);
      unsigned char* src = (unsigned char*)CVPixelBufferGetBaseAddress(cvFrame);;
      
      //I wish this weren't necessary, but
      //in my tests the only performant & reliabile
      //pixel format for QTCapture is k32ARGBPixelFormat, 
      //to my knowledge there is only RGBA format
      //available to gl textures
      
      //convert pixels from ARGB to RGB			
      argb_to_rgb(src, pixels, width*height);
      //      texture->loadData(pixels, width, height, GL_RGB);
      CVPixelBufferUnlockBaseAddress(cvFrame, 0);
      hasNewFrame = NO;
      isFrameNew = YES;
    }
    else{
      isFrameNew = NO;
    }
  }	
}

- (void) stop {
  if(self.isRunning){
    [self.session stopRunning];
  }	
	
  self.session = nil;
  
  free(pixels);
  //  delete texture;
}


- (BOOL) isRunning {
  return self.session && self.session.isRunning;
}

- (void) listDevices { 
  NSLog(@"ofxQTKitVideoGrabber devices %@", 
	[[QTCaptureDevice inputDevicesWithMediaType:QTMediaTypeVideo] 
	  arrayByAddingObjectsFromArray:[QTCaptureDevice inputDevicesWithMediaType:QTMediaTypeMuxed]]);
  
}

@end




// -----------------------------------------------------------------------
//                           C++ Interface
// -----------------------------------------------------------------------


QtKitVideoGrabber::QtKitVideoGrabber() {
  deviceID = 0;
  grabber = NULL;
  isInited = false;
}

QtKitVideoGrabber::~QtKitVideoGrabber() {
  if(isInited){
    close();
  }
}

void QtKitVideoGrabber::setDeviceID(int _deviceID) {
  deviceID = _deviceID;
  if(isInited){
    //reinit if we are running...
    //should be able to hot swap, but this is easier for now.
    int width  = ((QTKitVideoGrabber*)grabber).width;
    int height = ((QTKitVideoGrabber*)grabber).height;
    
    close();
    
    initGrabber(width, height);
  }
}

void QtKitVideoGrabber::initGrabber(int w, int h) {
  NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
  grabber = [[QTKitVideoGrabber alloc] initWithWidth:w height:h device:deviceID];
  isInited = (grabber != nil);
  [pool release];	
}

void QtKitVideoGrabber::update() {  
  this->grabFrame(); 
}

void QtKitVideoGrabber::grabFrame() {
  if(confirmInit()){
    [(QTKitVideoGrabber*)grabber update];
  }
}

bool QtKitVideoGrabber::isFrameNew() {
  return isInited && [(QTKitVideoGrabber*)grabber isFrameNew];
}

void QtKitVideoGrabber::listDevices() {
  if(confirmInit()){
    [(QTKitVideoGrabber*)grabber listDevices];
  }
}

void QtKitVideoGrabber::close() {
  [(QTKitVideoGrabber*)grabber stop];
  [(QTKitVideoGrabber*)grabber release];
  isInited = false;	
}

unsigned char* QtKitVideoGrabber::getPixels() {
  if(confirmInit()){
    return [(QTKitVideoGrabber*)grabber pixels];
  }
  return NULL;
}

// ofTexture &	QtKitVideoGrabber::getTextureReference() {
//   if(confirmInit()){
//     return *[(QTKitVideoGrabber*)grabber texture];
//   }
// }

void QtKitVideoGrabber::setVerbose(bool bTalkToMe) {
  if(confirmInit()){
    ((QTKitVideoGrabber*)grabber).verbose = bTalkToMe;
  }
}

// void QtKitVideoGrabber::draw(float x, float y, float w, float h) {
//   if(confirmInit()){
//     [(QTKitVideoGrabber*)grabber texture]->draw(x, y, w, h);
//   }
// }

// void QtKitVideoGrabber::draw(float x, float y) {
//   if(confirmInit()){
//     [(QTKitVideoGrabber*)grabber texture]->draw(x, y);
//   }
// }

float QtKitVideoGrabber::getHeight() {
  if(confirmInit()){
    return (float)((QTKitVideoGrabber*)grabber).height;
  }
  return 0;
}

float QtKitVideoGrabber::getWidth() {
  if(confirmInit()){
    return (float)((QTKitVideoGrabber*)grabber).width;
  }
  return 0;
}
		  
bool QtKitVideoGrabber::confirmInit() {
  if(!isInited){
    //    vw_out(ErrorMessage) << "QtKitVideoGrabber -- ERROR -- Calling method on non intialized video grabber";
  }
  return isInited;
}
