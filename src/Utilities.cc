// __BEGIN_LICENSE__
// Copyright (C) 2006, 2007 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


#include <Utilities.h>

#include <string>
#include <iostream>
#include <fstream>
using namespace std;

namespace vw { 
namespace GPU {

  // Class: TokenReplacer
  void TokenReplacer::AddVariable(string& variableName, string& variableValue) {
    stringMap[variableName] = variableValue;
  }
  
  void TokenReplacer::AddVariable(const char* variableName, const char*  variableValue) {
    stringMap[string(variableName)] = string(variableValue);
  }
  

  void TokenReplacer::Replace(const string& inText, string& outText) {
    int inLength = inText.size();
    outText.resize(0);
    outText.reserve((int) (inLength * 1.5));
    string tempToken;
    int i=0;
	
    while(i < inLength) {
      char cur = inText[i];
      if(cur == '$') {
        tempToken.resize(0);
        tempToken.reserve(32);
        i++;
        while(i < inLength) {
          cur = inText[i];
          if((cur > 47 && cur < 58) || (cur > 64 && cur < 91) || (cur > 96 && cur < 123) || cur == 95) {
            tempToken.push_back(cur);
            i++;
          }
          else {
            break;
          }
        }
        if(tempToken.size()) {
          map<string, string>::iterator iter = stringMap.find(tempToken);
          if(iter != stringMap.end()) {
            outText.append((*iter).second);  // OK to push string?
          }
        }
      }
      else {
        outText.push_back(cur);
        i++;
      }
    }
  }


  // File IO
  bool ReadFileAsString(const string& path, string& outString) {
    std::ifstream file(path.c_str());
    if(!file)
      return false;
    //while(file)
    //      outString << file;
        
    int length;
    file.seekg(0, std::ios::end);
    length = file.tellg();
    file.seekg(0, std::ios::beg);
    outString.resize(length);
    file.read((char*) outString.c_str(), length);

    return true;
  } 

 
}} // namespaces GPU, vw
