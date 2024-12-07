package edu.tufts.hrilab.config.hw1;

import edu.tufts.hrilab.diarc.DiarcConfiguration;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class projectConfig extends DiarcConfiguration {
  // for logging
  protected static Logger log = LoggerFactory.getLogger(projectConfig.class);

  @Override
  public void runConfiguration() {
    createInstance(edu.tufts.hrilab.llm.LLMComponent.class, "-endpoint http://vm-llama.eecs.tufts.edu:8080");
    createInstance(edu.tufts.hrilab.slug.parsing.llm.BeliefParserComponent.class, "-endpoint http://vm-llama.eecs.tufts.edu:8080") // not sure what arguments
    createInstance(edu.tufts.hrilab.action.GoalManagerComponent.class, "-goal llmProj(self) -beliefinitfile demos.pl agents/agents.pl -asl domains/llm/proj.asl");
  }
  
  // start the configuration
  public static void main(String[] args) {
    projectConfig config = new projectConfig();
    config.runConfiguration();
  }
}