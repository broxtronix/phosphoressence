// __BEGIN_LICENSE__
//
// PhosphorEssence
// An open framework for the visual exploration of mathematics
//
//  Copyright (C) 2009 Michael J. Broxton
//
// Note: This file was adapted from the OpenFrameworks open source
// project, and may be subject to additional licensing restrictions.
// 
//    http://www.openframeworks.cc/
//
// __END_LICENSE__

#ifndef __PE_GRAPHICS_TEXTURE_H__
#define __PE_GRAPHICS_TEXTURE_H__

#include <vw/Math/Vector.h>

#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#else // Linux
#include <GL/gl.h>
#include <GL/glu.h>
#endif 

namespace pe {
namespace graphics {
  
  class Drawable {
  public:
    virtual ~Drawable(){}
    virtual void draw(float x,float y)=0;
    virtual void draw(float x,float y,float w, float h)=0;
    virtual float getHeight()=0;
    virtual float getWidth()=0;
    
    virtual void setAnchorPercent(float xPct, float yPct){};
    virtual void setAnchorPoint(float x, float y){};
    virtual void resetAnchor(){};
  };


  typedef struct{

    bool bAllocated;
    int glType;
    int glTypeInternal;
    int textureTarget;
    int pixelType;  // MEMO: added this (GL_FLOAT, GL_UNSIGNED_BYTE etc.
    float tex_t;
    float tex_u;
    float tex_w;
    float tex_h;
    float width;
    float height;
    bool bFlipTexture;
    unsigned int textureID;
  } TextureData;

  //enable / disable the slight fset we add to Texture's texture
  //coords to compensate for bad edge artifiacts enabled by default
  void EnableTextureEdgeHack();
  void DisableTextureEdgeHack();

  class Texture : public Drawable {

  public :

    Texture();
    virtual ~Texture();

    // -----------------------------------------------------------------------
    // we allow pass by copy and assignment operator
    // it does a straight copy but you are getting the textureID  mom's texture
    // so this means that your texture and mom's texture are the same thing
    // so in other words be careful! calling clear on your texture will trash mom's
    // texture and vice versa.
    Texture(const Texture& mom);
    Texture& operator=(const Texture& mom);
    // -----------------------------------------------------------------------

    //uses the currently set PE texture type - default ARB texture
    void allocate(int w, int h, int internalGlDataType); 
    void clear();

    void loadData(void * data, int w, int h, int format, int type);

    void loadScreenData(int x, int y, int w, int h);

    //the anchor is the point the image is drawn around.
    //this can be useful if you want to rotate an image around a particular point.
    void setAnchorPercent(float xPct, float yPct); //set the anchor as a percentage of the image width/height ( 0.0-1.0 range )
    void setAnchorPoint(float x, float y); //set the anchor point in pixels
    void resetAnchor(); //resets the anchor to (0, 0)

    void draw(float x, float y, float w, float h);
    void draw(float x, float y);

    //for the advanced user who wants to draw textures in their own way
    void bind();
    void unbind();
	
    // these are helpers to allow you to get points for the texture ala "glTexCoordf" 
    // but are texture type independent. 
    // use them for immediate or non immediate mode
    vw::Vector2 getCoordFromPoint(float xPos, float yPos);		
    vw::Vector2 getCoordFromPercent(float xPts, float yPts);		
	
    void setTextureWrap(GLint wrapModeHorizontal, GLint wrapModeVertical);
    void setTextureMinMagFilter(GLint minFilter, GLint maxFilter);

    bool bAllocated();

    TextureData getTextureData();

    float getHeight();
    float getWidth();

    TextureData texData;
  protected:
    int nextPow2(int a);

    vw::Vector2 anchor;
    bool bAnchorIsPct;


  };

}} // namespace pe::graphics

#endif
