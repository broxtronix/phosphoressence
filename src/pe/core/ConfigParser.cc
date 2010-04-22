// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


#include <iostream>
#include <fstream>
#include <istream>

#include <boost/shared_ptr.hpp>
#include <boost/program_options.hpp>
namespace po = boost::program_options;


#include <pe/core/FundamentalTypes.h>
#include <pe/core/Log.h>
#include <pe/core/Exception.h>
#include <pe/core/Settings.h>
#include <pe/core/ConfigParser.h>

using boost::shared_ptr;
using namespace pe;

namespace {
  int32 name2level(std::string name) {
    typedef std::map<std::string, MessageLevel> MapType;
    static MapType name_map;

    if (name_map.empty()) {
      name_map["InfoMessage"]         = InfoMessage;
      name_map["ErrorMessage"]        = ErrorMessage;
      name_map["WarningMessage"]      = WarningMessage;
      name_map["DebugMessage"]        = DebugMessage;
      name_map["VerboseDebugMessage"] = VerboseDebugMessage;
      name_map["EveryMessage"]        = EveryMessage;
      name_map["*"]                   = EveryMessage;
    }
    MapType::const_iterator level = name_map.find(name);
    if (level != name_map.end())
      return level->second;

    return boost::lexical_cast<int32>(name);
  }
}

void pe::parse_config_file(const char* fn, pe::Settings& settings) {
  std::ifstream file(fn);

  if (!file.is_open())
    pe_throw(IOErr() <<  "Could not open logfile: " << fn);

  parse_config(file, settings);
}

void pe::parse_config(std::basic_istream<char>& stream, 
		      pe::Settings& settings) {

  // DO NOT try to log with pe_log! It will cause a deadlock because we're
  // holding locks inside reload_config, and the loggers will call
  // reload_config first.
  po::parsed_options opts(0);

  po::options_description desc("All options");
  desc.add_options()("*", "All");

  try {
    opts = po::parse_config_file( stream, desc );
  } catch (const po::invalid_syntax& e) {
    std::cerr << "Could not parse config file. Ignoring. (" 
	      << e.what() << ")" << std::endl;
  } catch (const boost::program_options::unknown_option& /*e*/) {
      // Swallow this one. We don't care about unknown options.
      pe_throw(LogicErr() << "We should be accepting all options. This shouldn't happen.");
  }

  shared_ptr<LogInstance> current_log;
  std::string current_logname = "console";

  typedef std::vector<po::option> OptionVec;

  for (OptionVec::const_iterator i=opts.options.begin(), end=opts.options.end(); i != end; ++i) {
    const po::option& o = *i;

    //cerr << "Looking at " << o.string_key << endl;

    try {
      if (o.string_key == "general.default_num_threads")
        settings.set_default_num_threads(boost::lexical_cast<int>(o.value[0]));
      else if (o.string_key == "general.system_cache_size")
        settings.set_system_cache_size(boost::lexical_cast<size_t>(o.value[0]));
      else if (o.string_key == "general.default_tile_size")
	settings.set_default_tile_size(boost::lexical_cast<int>(o.value[0]));
      else if (o.string_key == "general.tmp_directory")
	settings.set_tmp_directory(o.value[0]);
      else if (o.string_key.compare(0, 8, "logfile ") == 0) {
        size_t sep = o.string_key.find_last_of('.');
        assert(sep != std::string::npos);

	std::string logname = o.string_key.substr(8, sep-8);
	std::string level_s = o.string_key.substr(sep+1);
	std::string domain  = o.value[0];

        //cerr << "Logname[" << logname << "] level_s[" << level_s << "] domain[" << domain << "]" << endl;

        if (logname.empty() || level_s.empty() || domain.empty())
          continue;

        if (logname != current_logname) {
          current_logname = logname;
          if (current_logname == "console")
            current_log.reset();
          else {
            current_log = shared_ptr<LogInstance>( new LogInstance(logname) );
            pe_log().add(current_log);
          }
        }

        int32 level = name2level(level_s);

        //cerr << "Adding rule: " << level << " " << domain << "\n";
        if (current_log)
          current_log->rule_set().add_rule(level, domain);
        else
          pe_log().console_log().rule_set().add_rule(level, domain);
      }
      else {
        //cerr  << "Skipping " << o.string_key << endl;
        continue;
      }
    } catch (const boost::bad_lexical_cast& /*e*/) {
      std::cerr << "Could not parse line in config file near " 
		<< o.string_key << ". skipping." << std::endl;
    }
  }

}
