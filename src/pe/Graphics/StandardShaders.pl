#!/usr/local/bin/perl
# __BEGIN_LICENSE__
# Copyright (C) 2006, 2007 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__


#File Names
$pwd = `pwd`;
chomp($pwd);
$output_filename = $pwd . "/StandardShaders.cc";

#Get Input File List
`rm -f $output_filename`;
@files = `find ./shaders -maxdepth 2 -type f \! -path "*.svn*"`;

# Create Output File
open(OUT, ">$output_filename");

# Print Initial Code
print OUT "\#include <vw/Core/Thread.h>\n";
print OUT "\#include <StandardShaders.h>\n\n";
print OUT "\#include <iostream>\n\n";

print OUT "static std::map<std::string, const char*> standard_shaders_map;\n\n";
print OUT "namespace {\n";
print OUT "  vw::RunOnce standard_shaders_once = VW_RUNONCE_INIT;\n";
print OUT "  void init_standard_shaders() {\n";

#Iterate Through Input Files, printing map insert functions
foreach $filename (@files) {
  chomp($filename);
  $filename =~ /\.\/StandardShaders\/(.*)/;
  $mapname = $1;
  open(IN, $filename);
  print OUT "standard_shaders_map[\"", $mapname, "\"] = \" \\n\"\n";
  while ($line = <IN>) {
    chomp($line);
    print OUT "\"", $line, " \\n\"\n";
  }
  print OUT ";\n\n";
}

# Print End Code
print OUT "  }\n";
print OUT "}\n\n";

print OUT "std::string vw::graphics::find_standard_shader(std::string path) {\n";
print OUT "  standard_shaders_once.run( init_standard_shaders );\n\n";

print OUT "  std::map<std::string, const char*>::iterator iter_map = standard_shaders_map.find((path).c_str());\n";
print OUT "  if(iter_map != standard_shaders_map.end()) {\n";
print OUT "    return (*iter_map).second;\n";
print OUT "  } else {\n";
print OUT "    std::cout << \"ERROR: Could not find requested shader: \" << path << \"\\n\";";
print OUT "    exit(0);";
print OUT "  } \n";
print OUT "}\n";
