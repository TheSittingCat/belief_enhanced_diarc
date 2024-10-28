package edu.tufts.hrilab.config.projectConfigs;

import edu.tufts.hrilab.llm.LLMComponent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import edu.tufts.hrilab.diarc.DiarcConfiguration;
import edu.tufts.hrilab.slug.parsing.llm.BeliefParserComponent;
import edu.tufts.hrilab.slug.listen.ListenerComponent;
import edu.tufts.hrilab.simspeech.SimSpeechRecognitionComponent;
import edu.tufts.hrilab.action.GoalManagerComponent;
import edu.tufts.hrilab.simspeech.SimSpeechProductionComponent;

public class projConfig extends DiarcConfiguration {
    protected static final Logger LOG = LoggerFactory.getLogger(projConfig.class);

    @Override
    public void runConfiguration() {
        LOG.info("Running the LLM Model Test");
        String args = "-service GetDirectLLM";
        
        createInstance(SimSpeechRecognitionComponent.class, "-config Belief_Sim/belief_sim.simspeech -speaker kaveh -addressee roboshopper");
        createInstance(SimSpeechProductionComponent.class);
        createInstance(ListenerComponent.class);

        String goal_args = "-beliefinitfile demos.pl agents/agents.pl " + "-asl dialogue/nlu.asl " + "-goal listen(self)";
        createInstance(LLMComponent.class, "-service openai -model gpt-4o-mini");
        createInstance(BeliefParserComponent.class, args);
        createInstance(edu.tufts.hrilab.action.GoalManagerComponent.class, goal_args);
    }
}
