/*
 *  ofxQTKitVideoGrabber.cpp
 *
 *  Created by James George on 3/9/10.
 *  
 *
 */

#include <pe/video/QtKitVideoGrabber.h>
#include <pe/graphics/Texture.h>
using namespace pe::video;

#import "Cocoa/Cocoa.h"
#import "QTKit/QTKit.h"

#include <iostream>

static inline void argb_to_rgb(unsigned char* src, unsigned char* dst, int numPix) {
  for(int i = 0; i < numPix; i++){
    memcpy(dst, src+1, 3);
    src+=4;
    dst+=3;
  }	
}

@interface QtKitVideoGrabberImpl : QTCaptureVideoPreviewOutput {
  QTCaptureSession *session;
  QTCaptureDeviceInput *videoDeviceInput;
  NSInteger width, height;
  
  CVImageBufferRef cvFrame;
  pe::graphics::Texture* texture;
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
@property(readonly) pe::graphics::Texture* texture;
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


@implementation QtKitVideoGrabberImpl
@synthesize width, height;
@synthesize session;
@synthesize videoDeviceInput;
@synthesize pixels;
@synthesize texture;
@synthesize isFrameNew;
@synthesize verbose;

- (id) initWithWidth:(NSInteger)_width height:(NSInteger)_height device:(NSInteger)deviceID {
  if(self = [super init]){
    //configure self
    width = _width;
    height = _height;		
    [self setPixelBufferAttributes: [NSDictionary dictionaryWithObjectsAndKeys: 
	[NSNumber numberWithInt: kCVPixelFormatType_32BGRA], kCVPixelBufferPixelFormatTypeKey,
	[NSNumber numberWithInt:width], kCVPixelBufferWidthKey, 
	[NSNumber numberWithInt:height], kCVPixelBufferHeightKey, 
						  //	[NSNumber numberWithBool:YES], kCVPixelBufferOpenGLCompatibilityKey,
	nil]];	
    
    //instance variables
    cvFrame = NULL;
    hasNewFrame = false;
    texture = new pe::graphics::Texture();
    texture->allocate(_width, _height, GL_RGBA);
    pixels = (unsigned char*)calloc(sizeof(char), _width*_height*3);
    
    //set up device
    NSArray* videoDevices = [[QTCaptureDevice inputDevicesWithMediaType:QTMediaTypeVideo] 
			      arrayByAddingObjectsFromArray:[QTCaptureDevice inputDevicesWithMediaType:QTMediaTypeMuxed]];
    
    // std::string list = [[videoDevices description] cString];
    // std::cout << "QtKitVideoGrabberImpl -- Device List: " << list << "\n";
    
    NSError *error = nil;
    BOOL success;
    
    //start the session
    self.session = [[QTCaptureSession alloc] init];
    success = [self.session addOutput:self error:&error];
    if( !success ) {
      std::cout << "ERROR: QtKitVideoGrabberImpl - ERROR - Error adding output";
      return nil;
    }
    
    // Try to open the new device
    if(deviceID >= videoDevices.count){
      std::cout << "QtKitVideoGrabberImpl - ERROR - Error selected a nonexistent device";
      deviceID = videoDevices.count - 1;
    }
		
    QTCaptureDevice* selectedVideoDevice = [videoDevices objectAtIndex:deviceID];
    success = [selectedVideoDevice open:&error];
    if (selectedVideoDevice == nil || !success) {
      std::cout << "QtKitVideoGrabberImpl - ERROR - Selected device not opened";
      return nil;
    } else { 
      //      if(verbose) 
      std::cout << "\t--> QtKitVideoGrabber -- Using camera " 
		<< [[selectedVideoDevice description] cString] << "\n";
			
      // Add the selected device to the session
      videoDeviceInput = [[QTCaptureDeviceInput alloc] initWithDevice:selectedVideoDevice];
      success = [session addInput:videoDeviceInput error:&error];
      if(!success) 
	std::cout  << "QtKitVideoGrabberImpl - ERROR - Error adding device to session";	

//       // Create a decompressed video output stream for this session
//       [mCaptureDecompressedVideoOutput setPixelBufferAttributes:pixelBufferOptions]; 
		
// #if QTKIT_VERSION_MAX_ALLOWED >= QTKIT_VERSION_7_6_3
//       [mCaptureDecompressedVideoOutput setAutomaticallyDropsLateVideoFrames:YES]; 
// #endif
//       success = [mCaptureSession addOutput:mCaptureDecompressedVideoOutput error:&error];
//       if (!success) {
// 	cout << "QTKit failed to add Output to Capture Session" << endl; 
// 	[localpool drain]; 
// 	return 0;
//       }
		
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

  CVBufferRetain(videoFrame);

  CVImageBufferRef toRelease;
  @synchronized(self){
    toRelease = cvFrame;
    cvFrame = videoFrame;
    hasNewFrame = YES;
  }	
  if(toRelease != NULL){
    CVBufferRelease(toRelease);
  }
}

- (void) update {
  if(hasNewFrame){

    CVPixelBufferRef localFrame;


    @synchronized(self) {
      localFrame = CVBufferRetain(cvFrame);
      hasNewFrame = NO;
    }
   
    CVPixelBufferLockBaseAddress(localFrame, 0);
    unsigned char* baseaddress = (unsigned char*)CVPixelBufferGetBaseAddress(localFrame);
      
    size_t twidth = CVPixelBufferGetWidth(localFrame);
    size_t theight = CVPixelBufferGetHeight(localFrame);
    size_t trowBytes = CVPixelBufferGetBytesPerRow(localFrame);

    std::cout << "GOT A FRAME... " << twidth << " x " << theight << "  @  " << trowBytes << "\n";
    
    //convert pixels from BGRA to RGB			
    //      argb_to_rgb(src, pixels, width*height);
    texture->loadData(baseaddress, twidth, theight, GL_RGBA, GL_UNSIGNED_BYTE);
    CVPixelBufferUnlockBaseAddress(localFrame, 0);
    CVBufferRelease(localFrame);
    isFrameNew = YES;
  } else {
    isFrameNew = NO;
  }
}

- (void) stop {
  if(self.isRunning){
    [self.session stopRunning];
  }	
	
  self.session = nil;
  
  free(pixels);
  delete texture;
}


- (BOOL) isRunning {
  return self.session && self.session.isRunning;
}

- (void) listDevices { 
  NSLog(@"ofxQtKitVideoGrabberImpl devices %@", 
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
    int width  = ((QtKitVideoGrabberImpl*)grabber).width;
    int height = ((QtKitVideoGrabberImpl*)grabber).height;
    
    close();
    
    initGrabber(width, height);
  }
}

void QtKitVideoGrabber::initGrabber(int w, int h) {
  NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
  grabber = [[QtKitVideoGrabberImpl alloc] initWithWidth:w height:h device:deviceID];
  isInited = (grabber != nil);
  [pool release];	
}

void QtKitVideoGrabber::update() {  
  this->grabFrame(); 
}

void QtKitVideoGrabber::grabFrame() {
  if(confirmInit()){
    [(QtKitVideoGrabberImpl*)grabber update];
  }
}

bool QtKitVideoGrabber::isFrameNew() {
  return isInited && [(QtKitVideoGrabberImpl*)grabber isFrameNew];
}

void QtKitVideoGrabber::listDevices() {
  if(confirmInit()){
    [(QtKitVideoGrabberImpl*)grabber listDevices];
  }
}

void QtKitVideoGrabber::close() {
  [(QtKitVideoGrabberImpl*)grabber stop];
  [(QtKitVideoGrabberImpl*)grabber release];
  isInited = false;	
}

unsigned char* QtKitVideoGrabber::getPixels() {
  if(confirmInit()){
    return [(QtKitVideoGrabberImpl*)grabber pixels];
  }
  return NULL;
}

pe::graphics::Texture&	QtKitVideoGrabber::getTextureReference() {
  if(confirmInit()){
    return *[(QtKitVideoGrabberImpl*)grabber texture];
  }
}

void QtKitVideoGrabber::setVerbose(bool bTalkToMe) {
  if(confirmInit()){
    ((QtKitVideoGrabberImpl*)grabber).verbose = bTalkToMe;
  }
}

void QtKitVideoGrabber::draw(float x, float y, float w, float h) {
  if(confirmInit()){
    [(QtKitVideoGrabberImpl*)grabber texture]->draw(x, y, w, h);
  }
}

void QtKitVideoGrabber::draw(float x, float y) {
  if(confirmInit()){
    [(QtKitVideoGrabberImpl*)grabber texture]->draw(x, y);
  }
}

float QtKitVideoGrabber::getHeight() {
  if(confirmInit()){
    return (float)((QtKitVideoGrabberImpl*)grabber).height;
  }
  return 0;
}

float QtKitVideoGrabber::getWidth() {
  if(confirmInit()){
    return (float)((QtKitVideoGrabberImpl*)grabber).width;
  }
  return 0;
}
		  
bool QtKitVideoGrabber::confirmInit() {
  if(!isInited){
    std::cout << "QtKitVideoGrabber -- ERROR -- Calling method on non intialized video grabber";
  }
  return isInited;
}
